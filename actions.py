# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core_sdk import Tracker
from rasa_core_sdk.executor import CollectingDispatcher

from typing import Dict, Text, Any, List

import requests
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet, FollowupAction
from rasa_core_sdk.forms import FormAction

def _find_providers(location: Text, speciality: Text) -> List[Dict]:
    '''Returns json of facilities matching the search criteria.'''
    results = [
    {
      "provider_id": "154656",
      "provider_name": "Dr Jhon"
    },
    {
      "provider_id": "2345",
      "provider_name": "Dr Dileep"
    }
  ]

    return results

class SearchProvidersForm(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "search_providers_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        # work in progress to have the form work when the user provides entities in the first message
        # if not tracker.get_latest_entity_values():
        #     if tracker.get_latest_entity_values()
        return ["speciality", "location"]

    def slot_mappings(self) -> Dict[Text, Any]:
        return {
            "speciality": self.from_entity(entity="speciality",intent=["findadoctor","inform"]),
            "location": [self.from_entity(entity="zipcode",intent=["findadoctor","inform"]),
                        self.from_entity(entity="state",intent=["findadoctor","inform"]),
                        self.from_entity(entity="city",intent=["findadoctor","inform"])]}

    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict]:

        """Define what the form has to do after all required slots are filled"""

        location = tracker.get_slot('location')
        speciality = tracker.get_slot('speciality')
        results = _find_providers(location, speciality)
        buttons = []
        for r in results:
            provider_id = r.get("provider_id")
            provider_name = r.get("provider_name")
            payload = "/inform{\"provider_id\":\"" + provider_id + "\"}"
            buttons.append(
                {"title": "{}".format(provider_name.title()), "payload": payload})

        # limit number of buttons to 3 here for clear presentation purpose
        dispatcher.utter_button_message(
            "Here is a list of {} {} near you".format(len(buttons[:3]),"providers"),
            buttons[:3], button_type="vertical")
        # todo: note: button options are not working BUG in rasa_core

        # utter submit template
        dispatcher.utter_template('utter_submit', tracker)
        return []
