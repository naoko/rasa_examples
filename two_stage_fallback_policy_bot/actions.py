import logging
from rasa_core_sdk.executor import Action

logger = logging.getLogger(__name__)


class ActionGetSolarProduction(Action):
    def name(self):
        return 'action_get_solar_production'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message('Today your system produced 8.4kw')
        return []


class ActionTurnLightsOn(Action):
    def name(self):
        return 'action_turn_lights_on'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message('Okay, turning lights on')
        return []
