
# Copyright 2020 Bradbase
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, sys
import unittest
import configparser
from dataclasses import asdict
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient, WebApplicationClient
import httpretty
import warnings
from dacite import from_dict
import json

sys.path.insert(0, sys.path[0]+"/..")

import harvest
from harvest.harvestdataclasses import *

"""
There is a sample test config.

Copy it, name it test_config.ini and fill it out with your test details.

tests/test_config.ini is already in .gitignore

Just in case, the test config file looks like this:

[PERSONAL ACCESS TOKEN]
url = https://api.harvestapp.com/api/v2
put_auth_in_header = True
personal_token = Bearer 1234567.pt.somebunchoflettersandnumbers
account_id = 1234567

[OAuth2 Implicit Code Grant]
uri = https://api.harvestapp.com/api/v2
client_id = aclientid
auth_url = https://id.getharvest.com/oauth2/authorize

[OAuth2 Authorization Code Grant]
uri = https://api.harvestapp.com/api/v2
client_id = aclientid
client_secret = itsmysecret
auth_url = https://id.getharvest.com/oauth2/authorize
token_url = https://id.getharvest.com/api/v2/oauth2/token
account_id = 1234567
"""

"""
Those who tread this path:-

These tests currently really only test that the default URL has been formed
correctly and that the datatype that gets returned can be typed into the dataclass.
Probably enough but a long way from "comprehensive".
"""

class TestTimesheets(unittest.TestCase):

    def setUp(self):
        personal_access_token = PersonalAccessToken('ACCOUNT_NUMBER', 'PERSONAL_ACCESS_TOKEN')
        self.harvest = harvest.Harvest('https://api.harvestapp.com/api/v2', personal_access_token)
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*") # There's a bug in httpretty ATM.
        httpretty.enable()

    def teardown(self):
        httpretty.reset()
        httpretty.disable()


    def test_time_entries(self):
        time_entry_636709355_dict = {
                "id":636709355,
                "spent_date":"2017-03-02",
                "user":{
                        "id":1782959,
                        "name":"Kim Allen"
                    },
                "client":{
                        "id":5735774,
                        "name":"ABC Corp"
                    },
                "project":{
                        "id":14307913,
                        "name":"Marketing Website"
                    },
                "task":{
                        "id":8083365,
                        "name":"Graphic Design"
                    },
                "user_assignment":{
                        "id":125068553,
                        "is_project_manager":True,
                        "is_active":True,
                        "budget":None,
                        "created_at":"2017-06-26T22:32:52Z",
                        "updated_at":"2017-06-26T22:32:52Z",
                        "hourly_rate":100.0
                    },
                "task_assignment":{
                    "id":155502709,
                        "billable":True,
                        "is_active":True,
                        "created_at":"2017-06-26T21:36:23Z",
                        "updated_at":"2017-06-26T21:36:23Z",
                        "hourly_rate":100.0,
                        "budget":None
                    },
                "hours":2.0,
                "notes":"Adding CSS styling",
                "created_at":"2017-06-27T15:50:15Z",
                "updated_at":"2017-06-27T16:47:14Z",
                "is_locked":True,
                "locked_reason":"Item Approved and Locked for this Time Period",
                "is_closed":True,
                "is_billed":False,
                "timer_started_at":None,
                "started_time":"3:00pm",
                "ended_time":"5:00pm",
                "is_running":False,
                "invoice":None,
                "external_reference":None,
                "billable":True,
                "budgeted":True,
                "billable_rate":100.0,
                "cost_rate":50.0
            }

        time_entry_636708723_dict = {
                "id":636708723,
                "spent_date":"2017-03-01",
                "user":{
                        "id":1782959,
                        "name":"Kim Allen"
                    },
                "client":{
                        "id":5735776,
                        "name":"123 Industries"
                    },
                "project":{
                        "id":14308069,
                        "name":"Online Store - Phase 1"
                    },
                "task":{
                        "id":8083366,
                        "name":"Programming"
                    },
                "user_assignment":{
                        "id":125068554,
                        "is_project_manager":True,
                        "is_active":True,
                        "budget":None,
                        "created_at":"2017-06-26T22:32:52Z",
                        "updated_at":"2017-06-26T22:32:52Z",
                        "hourly_rate":100.0
                    },
                "task_assignment":{
                        "id":155505014,
                        "billable":True,
                        "is_active":True,
                        "created_at":"2017-06-26T21:52:18Z",
                        "updated_at":"2017-06-26T21:52:18Z",
                        "hourly_rate":100.0,
                        "budget":None
                    },
                "hours":1.0,
                "notes":"Importing products",
                "created_at":"2017-06-27T15:49:28Z",
                "updated_at":"2017-06-27T16:47:14Z",
                "is_locked":True,
                "locked_reason":"Item Invoiced and Approved and Locked for this Time Period",
                "is_closed":True,
                "is_billed":True,
                "timer_started_at":None,
                "started_time":"1:00pm",
                "ended_time":"2:00pm",
                "is_running":False,
                "invoice":{
                        "id":13150403,
                        "number":"1001"
                    },
                "external_reference":{
                        "id":"31356723",
                        "group_id":"Cyberdyne",
                        "permalink":"https://isengard.net/merry/and/pippin",
                        "service":"with_a_smile",
                        "service_icon_url":"https://isengard.net/saruman.jpg"
                    },
                "billable":True,
                "budgeted":True,
                "billable_rate":100.0,
                "cost_rate":50.0
            }

        time_entry_636708574_dict = {
                "id":636708574,
                "spent_date":"2017-03-01",
                "user":{
                        "id":1782959,
                        "name":"Kim Allen"
                    },
                "client":{
                        "id":5735776,
                        "name":"123 Industries"
                    },
                "project":{
                        "id":14308069,
                        "name":"Online Store - Phase 1"
                    },
                "task":{
                        "id":8083369,
                        "name":"Research"
                    },
                "user_assignment":{
                        "id":125068554,
                        "is_project_manager":True,
                        "is_active":True,
                        "budget":None,
                        "created_at":"2017-06-26T22:32:52Z",
                        "updated_at":"2017-06-26T22:32:52Z",
                        "hourly_rate":100.0
                    },
                "task_assignment":{
                        "id":155505016,
                        "billable":False,
                        "is_active":True,
                        "created_at":"2017-06-26T21:52:18Z",
                        "updated_at":"2017-06-26T21:54:06Z",
                        "hourly_rate":100.0,
                        "budget":None
                    },
                "hours":1.0,
                "notes":"Evaluating 3rd party libraries",
                "created_at":"2017-06-27T15:49:17Z",
                "updated_at":"2017-06-27T16:47:14Z",
                "is_locked":True,
                "locked_reason":"Item Approved and Locked for this Time Period",
                "is_closed":True,
                "is_billed":False,
                "timer_started_at":None,
                "started_time":"11:00am",
                "ended_time":"12:00pm",
                "is_running":False,
                "invoice":None,
                "external_reference":None,
                "billable":False,
                "budgeted":True,
                "billable_rate":None,
                "cost_rate":50.0
            }

        time_entry_636707831_dict = {
                "id":636707831,
                "spent_date":"2017-03-01",
                "user":{
                        "id":1782959,
                        "name":"Kim Allen"
                    },
                "client":{
                        "id":5735776,
                        "name":"123 Industries"
                    },
                "project":{
                        "id":14308069,
                        "name":"Online Store - Phase 1"
                    },
                "task":{
                        "id":8083368,
                        "name":"Project Management"
                    },
                "user_assignment":{
                        "id":125068554,
                        "is_project_manager":True,
                        "is_active":True,
                        "budget":None,
                        "created_at":"2017-06-26T22:32:52Z",
                        "updated_at":"2017-06-26T22:32:52Z",
                        "hourly_rate":100.0
                    },
                "task_assignment":{
                        "id":155505015,
                        "billable":True,
                        "is_active":True,
                        "created_at":"2017-06-26T21:52:18Z",
                        "updated_at":"2017-06-26T21:52:18Z",
                        "hourly_rate":100.0,
                        "budget":None
                    },
                "hours":2.0,
                "notes":"Planning meetings",
                "created_at":"2017-06-27T15:48:24Z",
                "updated_at":"2017-06-27T16:47:14Z",
                "is_locked":True,
                "locked_reason":"Item Invoiced and Approved and Locked for this Time Period",
                "is_closed":True,
                "is_billed":True,
                "timer_started_at":None,
                "started_time":"9:00am",
                "ended_time":"11:00am",
                "is_running":False,
                "invoice":{
                        "id":13150403,
                        "number":"1001"
                    },
                "external_reference":None,
                "billable":True,
                "budgeted":True,
                "billable_rate":100.0,
                "cost_rate":50.0
            }

        time_entry_636718192_dict = {
                "id":636718192,
                "spent_date":"2017-03-21",
                "user":{
                        "id":1782959,
                        "name":"Kim Allen"
                    },
                "client":{
                        "id":5735774,
                        "name":"ABC Corp"
                    },
                "project":{
                        "id":14307913,
                        "name":"Marketing Website"
                    },
                "task":{
                        "id":8083365,
                        "name":"Graphic Design"
                    },
                "user_assignment":{
                        "id":125068553,
                        "is_project_manager":True,
                        "is_active":True,
                        "budget":None,
                        "created_at":"2017-06-26T22:32:52Z",
                        "updated_at":"2017-06-26T22:32:52Z",
                        "hourly_rate":100.0
                    },
                "task_assignment":{
                        "id":155502709,
                        "billable":True,
                        "is_active":True,
                        "created_at":"2017-06-26T21:36:23Z",
                        "updated_at":"2017-06-26T21:36:23Z",
                        "hourly_rate":100.0,
                        "budget":None
                    },
                "hours":1.0,
                "notes":None,
                "created_at":"2017-06-27T16:01:23Z",
                "updated_at":"2017-06-27T16:01:23Z",
                "is_locked":False,
                "locked_reason":None,
                "is_closed":False,
                "is_billed":False,
                "timer_started_at":None,
                "started_time":None,
                "ended_time":None,
                "is_running":False,
                "invoice":None,
                "external_reference": None,
                "billable":True,
                "budgeted":True,
                "billable_rate":100.0,
                "cost_rate":50.0
            }

        time_entry_662204379_dict = {
                "id": 662204379,
                "spent_date": "2017-03-21",
                "user": {
                        "id": 1795925,
                        "name": "Jane Smith"
                    },
                "client": {
                        "id": 5735776,
                        "name": "123 Industries"
                    },
                "project": {
                        "id": 14808188,
                        "name": "Task Force"
                    },
                "task": {
                        "id": 8083366,
                        "name": "Programming"
                    },
                "user_assignment": {
                        "id": 130403296,
                        "is_project_manager": True,
                        "is_active": True,
                        "budget": None,
                        "created_at": "2017-08-22T17:36:54Z",
                        "updated_at": "2017-08-22T17:36:54Z",
                        "hourly_rate": 100.00 # TODO: this is supposed to be an int. Something isn't casting int to float.
                    },
                "task_assignment": {
                        "id": 160726645,
                        "billable": True,
                        "is_active": True,
                        "created_at": "2017-08-22T17:36:54Z",
                        "updated_at": "2017-08-22T17:36:54Z",
                        "hourly_rate": 100.00, # TODO: this is supposed to be an int. Something isn't casting int to float.
                        "budget": None
                    },
                "hours": 0.0, # TODO: this is supposed to be an int. Something isn't casting int to float.
                "notes": None,
                "created_at": "2017-08-22T17:40:24Z",
                "updated_at": "2017-08-22T17:40:24Z",
                "is_locked": False,
                "locked_reason": None,
                "is_closed": False,
                "is_billed": False,
                "timer_started_at": "2017-08-22T17:40:24Z",
                "started_time": "11:40am",
                "ended_time": None,
                "is_running": True,
                "invoice": None,
                "external_reference": None,
                "billable": True,
                "budgeted": False,
                "billable_rate": 100.00, # TODO: this is supposed to be an int. Something isn't casting int to float.
                "cost_rate": 75.00 # TODO: this is supposed to be an int. Something isn't casting int to float.
            }

        time_entry_662202797_dict = {
                "id": 662202797,
                "spent_date": "2017-03-21",
                "user": {
                        "id": 1795925,
                        "name": "Jane Smith"
                    },
                "client": {
                        "id": 5735776,
                        "name": "123 Industries"
                    },
                "project": {
                        "id": 14808188,
                        "name": "Task Force"
                    },
                "task": {
                        "id": 8083366,
                        "name": "Programming"
                    },
                "user_assignment": {
                        "id": 130403296,
                        "is_project_manager": True,
                        "is_active": True,
                        "budget": None,
                        "created_at": "2017-08-22T17:36:54Z",
                        "updated_at": "2017-08-22T17:36:54Z",
                        "hourly_rate": 100.00 # TODO: this is supposed to be an int. Something isn't casting int to float.
                    },
                "task_assignment": {
                        "id": 160726645,
                        "billable": True,
                        "is_active": True,
                        "created_at": "2017-08-22T17:36:54Z",
                        "updated_at": "2017-08-22T17:36:54Z",
                        "hourly_rate": 100.00, # TODO: this is supposed to be an int. Something isn't casting int to float.
                        "budget": None
                    },
                "hours": 0.02,
                "notes": None,
                "created_at": "2017-08-22T17:37:13Z",
                "updated_at": "2017-08-22T17:38:31Z",
                "is_locked": False,
                "locked_reason": None,
                "is_closed": False,
                "is_billed": False,
                "timer_started_at": None,
                "started_time": "11:37am",
                "ended_time": "11:38am",
                "is_running": False,
                "invoice": None,
                "external_reference": None,
                "billable": True,
                "budgeted": False,
                "billable_rate": 100.00, # TODO: this is supposed to be an int. Something isn't casting int to float.
                "cost_rate": None
            }

        time_entries_dict = {
                "time_entries":[time_entry_636709355_dict, time_entry_636708723_dict, time_entry_636708574_dict, time_entry_636707831_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":4,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/time_entries?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/time_entries?page=1&per_page=100"
                    }
            }

        company_dict = {
                "base_uri":"https://{ACCOUNT_SUBDOMAIN}.harvestapp.com",
                "full_domain":"{ACCOUNT_SUBDOMAIN}.harvestapp.com",
                "name":"API Examples",
                "is_active":False,
                "week_start_day":"Monday",
                "wants_timestamp_timers":False,
                "time_format":"hours_minutes",
                "plan_type":"sponsored",
                "expense_feature":True,
                "invoice_feature":True,
                "estimate_feature":True,
                "approval_required":True,
                "clock":"12h",
                "decimal_symbol":".",
                "thousands_separator":",",
                "color_scheme":"orange"
            }

        # time_entries
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/time_entries?page=1&per_page=100",
                body=json.dumps(time_entries_dict),
                status=200
            )
        time_entries = from_dict(data_class=TimeEntries, data=time_entries_dict)
        requested_time_entries = self.harvest.time_entries()
        self.assertEqual(requested_time_entries, time_entries)

        # get_time_entry
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/time_entries/636708723",
                body=json.dumps(time_entry_636708723_dict),
                status=200
            )
        time_entry = from_dict(data_class=TimeEntry, data=time_entry_636708723_dict)
        requested_time_entry = self.harvest.get_time_entry(time_entry_id=636708723)
        self.assertEqual(requested_time_entries, time_entries)

        # create_time_entry via duration
        company_dict['wants_timestamp_timers'] = False
        httpretty.register_uri(httpretty.GET, "https://api.harvestapp.com/api/v2/company", body=json.dumps(company_dict), status=200)
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/time_entries",
                body=json.dumps(time_entry_636718192_dict),
                status=201
            )
        new_time_entry0 = from_dict(data_class=TimeEntry, data=time_entry_636718192_dict)
        requested_new_time_entry0 = self.harvest.create_time_entry_via_duration(project_id= 14307913, task_id= 8083365, spent_date= "2017-03-21", user_id= 1782959, hours= 1.0)
        self.assertEqual(requested_new_time_entry0, new_time_entry0)

        # create_time_entry via start and end time
        company_dict['wants_timestamp_timers'] = True
        httpretty.register_uri(httpretty.GET, "https://api.harvestapp.com/api/v2/company", body=json.dumps(company_dict), status=200)
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/time_entries",
                body=json.dumps(time_entry_636718192_dict),
                status=201
            )
        new_time_entry1 = from_dict(data_class=TimeEntry, data=time_entry_636718192_dict)
        requested_new_time_entry1 = self.harvest.create_time_entry_via_start_and_end_time(project_id= 14307913, task_id= 8083365, spent_date= "2017-03-21", user_id= 1782959, started_time= "8:00am", ended_time= "9:00am")
        self.assertEqual(requested_new_time_entry1, new_time_entry1)

        # update_time_entry
        time_entry_636718192_dict['notes'] = "Updated notes"
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/time_entries/636718192",
                body=json.dumps(time_entry_636718192_dict),
                status=200
            )
        updated_time_entry = from_dict(data_class=TimeEntry, data=time_entry_636718192_dict)
        requested_updated_time_entry = self.harvest.update_time_entry(time_entry_id= 636718192, notes= "Updated notes")
        self.assertEqual(requested_updated_time_entry, updated_time_entry)

        # delete_time_entry_external_reference
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/time_entries/636718192/external_reference",
                status=200
            )
        requested_deleted_time_entry_external_reference = self.harvest.delete_time_entry_external_reference(time_entry_id= 636718192)
        self.assertEqual(requested_deleted_time_entry_external_reference, None)

        # delete_time_entry
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/time_entries/636718192",
                status=200
            )
        requested_deleted_time_entry = self.harvest.delete_time_entry(time_entry_id= 636718192)
        self.assertEqual(requested_deleted_time_entry, None)

        # restart_a_stopped_time_entry
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/time_entries/662204379/restart", # harvest have the wrong time entry id in their doco
                body=json.dumps(time_entry_662204379_dict),
                status=200
            )
        restarted_time_entry = from_dict(data_class=TimeEntry, data=time_entry_662204379_dict)
        requested_restarted_time_entry = self.harvest.restart_a_stopped_time_entry(time_entry_id= 662204379)
        self.assertEqual(requested_restarted_time_entry, restarted_time_entry)

        # stop_a_running_time_entry
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/time_entries/662202797/stop",
                body=json.dumps(time_entry_662202797_dict),
                status=200
            )
        stopped_time_entry = from_dict(data_class=TimeEntry, data=time_entry_662202797_dict)
        requested_stopped_time_entry = self.harvest.stop_a_running_time_entry(time_entry_id= 662202797)
        self.assertEqual(requested_stopped_time_entry, stopped_time_entry)


        httpretty.reset()


if __name__ == '__main__':
    unittest.main()
