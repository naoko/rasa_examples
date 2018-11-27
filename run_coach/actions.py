import logging
import enum

import requests

from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT

logger = logging.getLogger(__name__)


class DucklingDimension(enum.Enum):
    duration = "duration"
    distance = "distance"


def ask_duckling(value: str, dimension: DucklingDimension):
    payload = dict(locale="en_US", text=value)
    url = "http://0.0.0.0:8000/parse"
    r = requests.post(url=url, data=payload)
    logger.info(f"Duckling result: '{r.text}'")
    try:
        dim_index = next(i for i, data in enumerate(r.json()) if data['dim'] == dimension.value)
        return r.json()[dim_index]["value"]
    except StopIteration:
        return


class InformForm(FormAction):

    def name(self):
        return "inform_form"

    @staticmethod
    def required_slots(tracker):
        """A list of required slots that the form has to fill"""
        if tracker.get_slot('main_menu') == 'predicted':
            return ["distance", "finish_time", "next_race_distance"]
        if tracker.get_slot('main_menu') == 'target':
            return ["distance", "finish_time"]
        if tracker.get_slot('main_menu') == 'strategy':
            return ["distance"]
        return []

    def slot_mappings(self):
        return dict(
            next_race_distance=[
                self.from_entity(entity='distance'),
            ],
            distance=[
                self.from_entity(entity='distance'),
            ]
        )

    def validate(self, dispatcher, tracker, domain):
        """
        Validate extracted requested slot.
        If failed to extract, ask again.
        If extracted, format if specified.
        """

        # extract other slots that were not requested
        # but set by corresponding entity
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))

            if not slot_values:
                # Some slot was requested but nothing was extracted
                err_msg = f"Failed to validate slot {slot_to_fill} with action {self.name()}"
                logger.error(err_msg)
                # you can reject to execute the form action
                # by raising ActionExecutionRejection
                # it will allow other policies to predict another action
                raise ActionExecutionRejection(self.name(), err_msg)

            # we'll check when validation failed in order
            # to add appropriate utterances
            slot_values = self.format_and_validate(slot_values, dispatcher, tracker)

        # validation succeed, set slots to extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]

    @staticmethod
    def format_and_validate(slot_values, dispatcher, tracker):
        for slot, value in slot_values.items():
            if slot == 'finish_time':
                # format data to hh:mm:ss
                r = ask_duckling(value=value, dimension=DucklingDimension.duration)
                if r:
                    duration_in_sec = r['normalized']['value']
                    if duration_in_sec > 24 * 60 * 60:
                        dispatcher.messages('finish time should be less than 1 day')
                        slot_values[slot] = None
                    else:
                        from datetime import timedelta
                        slot_values[slot] = str(timedelta(seconds=duration_in_sec))
                else:
                    dispatcher.messages('Unable to parse the finish time')
                    # validation failed, set slot to None
                    slot_values[slot] = None

                return slot_values

            elif slot == 'distance':
                if value.isdigit():
                    return slot_values

                if "full" in value or "marathon" in value:
                    slot_values[slot] = "26.2"
                    return slot_values

                if "half" in value:
                    slot_values[slot] = "13.1"
                    return slot_values

                r = ask_duckling(value=value, dimension=DucklingDimension.distance)
                if r:
                    slot_values[slot] = r["value"]
                else:
                    # validation failed, set slot to None
                    dispatcher.utter_template('utter_unable_to_parse_distance', tracker)
                    slot_values[slot] = None
                return slot_values

    def submit(self, dispatcher, tracker, domain):
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_template('utter_submit', tracker)
        return []
