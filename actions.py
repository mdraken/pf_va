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

SEARCH_TYPES = {

    "hospital":
        {
            "name": "Find a Doctor",
            "resource": "FAD"
        },
    "nursing_home":
        {
            "name": "Choose your PCP",
            "resource": "PCP"
        },
    "home_health":
        {
            "name": "How are you feeling today?",
            "resource": "CUI"
        }
}
	
class FindSearchTypes(Action):
    '''This action class allows to display buttons for each facility type
    for the user to chose from to fill the facility_type entity slot.'''

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "find_search_types"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:

        buttons = []
        for t in SEARCH_TYPES:
            find_search_types = SEARCH_TYPES[t]
            payload = "/inform{\"find_search_types\": \"" + SEARCH_TYPES.get(
                "resource") + "\"}"

            buttons.append(
                {"title": "{}".format(find_search_types.get("name").title()),
                 "payload": payload})

        dispatcher.utter_button_template("utter_greet", buttons, tracker,
                                         button_type="custom")
        return []

def _find_facilities(location: Text, resource: Text) -> List[Dict]:
    '''Returns json of facilities matching the search criteria.'''

    if str.isdigit(location):
        full_path = _create_path(ENDPOINTS["base"], resource,
                                 ENDPOINTS[resource]["zip_code_query"],
                                 location)
    else:
        full_path = _create_path(ENDPOINTS["base"], resource,
                                 ENDPOINTS[resource]["city_query"],
                                 location.upper())

    results = requests.get(full_path).json()
    return results


def _resolve_name(facility_types, resource) ->Text:
    for key, value in facility_types.items():
        if value.get("resource") == resource:
            return value.get("name")
    return ""

	
class SearchProvider(Action):
    '''This action class retrieves a list of all facilities matching
    the supplied search criteria and displays buttons of random search
    results to the user to pick from.'''

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "find_facilities"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:

        location = tracker.get_slot('location')
        facility_type = tracker.get_slot('speciality')

        results = _find_facilities(location, speciality)
        button_name = _resolve_name(FACILITY_TYPES, facility_type)
        if len(results) == 0:
            dispatcher.utter_message(
                "Sorry, we could not find a {} in {}.".format(button_name,
                                                              location))
            return []

        buttons = []
        print("found {} facilities".format(len(results)))
        for r in results:
            if facility_type == FACILITY_TYPES["hospital"]["resource"]:
                facility_id = r.get("provider_id")
                name = r["hospital_name"]
            elif facility_type == FACILITY_TYPES["nursing_home"]["resource"]:
                facility_id = r["federal_provider_number"]
                name = r["provider_name"]
            else:
                facility_id = r["provider_number"]
                name = r["provider_name"]

            payload = "/inform{\"facility_id\":\"" + facility_id + "\"}"
            buttons.append(
                {"title": "{}".format(name.title()), "payload": payload})

        # limit number of buttons to 3 here for clear presentation purpose
        dispatcher.utter_button_message(
            "Here is a list of {} {}s near you".format(len(buttons[:3]),
                                                       button_name),
            buttons[:3], button_type="vertical")
        # todo: note: button options are not working BUG in rasa_core

        return []


class SearchProviderForm(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "searchprovider_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["speciality", "location"]

    def slot_mappings(self) -> Dict[Text, Any]:
        return {
            "speciality": self.from_entity(entity="speciality",
                                              intent=["inform",
                                                      "search_provider"]),
            "location": self.from_entity(entity="location",
                                         intent=["inform",
                                                 "search_provider"])}

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:

        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_template('utter_submit', tracker)
        return [FollowupAction('find_providers')]

