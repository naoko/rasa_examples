import logging

from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT

logger = logging.getLogger(__name__)


class AuthForm(FormAction):

    def name(self):
        return "auth_form"

    @staticmethod
    def required_slots(tracker):
        return ["auth_email", "verification_code"]

    def slot_mappings(self):
        return dict(
            auth_email=[
                self.from_entity(entity='email'),
            ],
            verification_code=[
                self.from_entity(entity='verification_code')
            ]
        )

    def submit(self, dispatcher, tracker, domain):
        """Define what the form has to do
            after all required slots are filled"""

        return []

    def request_next_slot(self,
                          dispatcher,  # type: CollectingDispatcher
                          tracker,  # type: Tracker
                          domain  # type: Dict[Text, Any]
                          ):
        if tracker.get_slot('authenticated'):
            print(tracker.get_slot('authenticated'))
            return None
        else:
            for slot in self.required_slots(tracker):
                if self._should_request_slot(tracker, slot):
                    logger.debug("Request next slot '{}'".format(slot))
                    dispatcher.utter_template("utter_ask_{}".format(slot), tracker)
                    return [SlotSet(REQUESTED_SLOT, slot)]
        return None

    def validate(self, dispatcher, tracker, domain):
        """Validate extracted value of requested slot
            else reject execution of the form action

            Subclass this method to add custom validation and rejection logic
        """
        # extract other slots that were not requested
        # but set by corresponding entity
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher,
                                                           tracker, domain))
            if slot_to_fill == 'verification_code':
                if slot_values['verification_code'] == '1234':
                    slot_values.update(dict(authenticated=True))
                else:
                    dispatcher.utter_message(
                        "Incorrect verification code. Please enter again.")
                    return [SlotSet('verification_code', None)]

            if not slot_values:
                # reject to execute the form action
                # if some slot was requested but nothing was extracted
                # it will allow other policies to predict another action
                raise ActionExecutionRejection(self.name(),
                                               "Failed to validate slot {0} "
                                               "with action {1}"
                                               "".format(slot_to_fill,
                                                         self.name()))

        # validation succeed, set slots to extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]
