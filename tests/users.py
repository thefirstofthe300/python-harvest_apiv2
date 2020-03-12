
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

class TestUsers(unittest.TestCase):

    def setUp(self):
        personal_access_token = PersonalAccessToken('ACCOUNT_NUMBER', 'PERSONAL_ACCESS_TOKEN')
        self.harvest = harvest.Harvest('https://api.harvestapp.com/api/v2', personal_access_token)
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*") # There's a bug in httpretty ATM.
        httpretty.enable()

    def teardown(self):
        httpretty.reset()
        httpretty.disable()


    def test_billable_rates(self):
        billable_rate_125068554_dict = {
                "id":125068554,
                "amount":75.0,
                "start_date":None,
                "end_date":"2016-12-31",
                "created_at":"2019-06-26T22:32:52Z",
                "updated_at":"2019-06-26T22:32:52Z"
            }

        billable_rate_125066109_dict = {
                "id":125066109,
                "amount":100.0,
                "start_date":"2017-01-01",
                "end_date":"2017-12-31",
                "created_at":"2019-06-26T21:52:18Z",
                "updated_at":"2019-06-26T21:52:18Z"
            }

        billable_rate_125066110_dict = {
                "id":125066110,
                "amount":125.0,
                "start_date":"2018-01-01",
                "end_date":None,
                "created_at":"2019-06-26T21:52:18Z",
                "updated_at":"2019-06-26T21:52:18Z"
            }

        billable_rate_125068758_dict = {
                "id":125068758,
                "amount":150.0,
                "start_date":"2019-01-01",
                "end_date":None,
                "created_at":"2019-01-06T22:36:01Z",
                "updated_at":"2019-01-06T22:36:01Z"
            }

        billable_rates_dict = {
                "billable_rates":[billable_rate_125068554_dict, billable_rate_125066109_dict, billable_rate_125066110_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":3,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/users/1782974/billable_rates?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/users/1782974/billable_rates?page=1&per_page=100"
                    }
            }

        # billable_rates
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/users/1782974/billable_rates?page=1&per_page=100",
                body=json.dumps(billable_rates_dict),
                status=200
            )
        billable_rates = from_dict(data_class=BillableRates, data=billable_rates_dict)
        requested_billable_rates = self.harvest.billable_rates(user_id= 1782974)
        self.assertEqual(requested_billable_rates, billable_rates)

        # get_billable_rate
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/users/1782974/billable_rates/125068554",
                body=json.dumps(billable_rate_125068554_dict),
                status=200
            )
        billable_rate = from_dict(data_class=BillableRate, data=billable_rate_125068554_dict)
        requested_billable_rate = self.harvest.get_billable_rate(user_id= 1782974, billable_rate_id= 125068554)
        self.assertEqual(requested_billable_rate, billable_rate)

        # create_billable_rate
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/users/1782974/billable_rates",
                body=json.dumps(billable_rate_125068758_dict),
                status=201
            )
        created_billable_rate = from_dict(data_class=BillableRate, data=billable_rate_125068758_dict)
        requested_created_billable_rate = self.harvest.create_billable_rate(user_id= 1782974, amount= 150.0, start_date= "2019-01-01")
        self.assertEqual(requested_created_billable_rate, created_billable_rate)

        httpretty.reset()

    def test_user_cost_rates(self):
        cost_rate_125068554_dict = {
                "id":125068554,
                "amount":75.0,
                "start_date":None,
                "end_date":"2016-12-31",
                "created_at":"2019-06-26T22:32:52Z",
                "updated_at":"2019-06-26T22:32:52Z"
            }

        cost_rate_125066109_dict = {
                "id":125066109,
                "amount":100.0,
                "start_date":"2017-01-01",
                "end_date":"2017-12-31",
                "created_at":"2019-06-26T21:52:18Z",
                "updated_at":"2019-06-26T21:52:18Z"
            }

        cost_rate_125066110_dict = {
                "id":125066110,
                "amount":125.0,
                "start_date":"2018-01-01",
                "end_date":None,
                "created_at":"2019-06-26T21:52:18Z",
                "updated_at":"2019-06-26T21:52:18Z"
            }

        cost_rate_125068758_dict = {
                "id":125068758,
                "amount":150.0,
                "start_date":"2019-01-01",
                "end_date":None,
                "created_at":"2019-01-06T22:36:01Z",
                "updated_at":"2019-01-06T22:36:01Z"
            }

        cost_rates_dict = {
                "cost_rates":[cost_rate_125068554_dict, cost_rate_125066109_dict, cost_rate_125066110_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":3,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/users/1782974/cost_rates?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/users/1782974/cost_rates?page=1&per_page=100"
                    }
            }

        # user_cost_rates
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/users/1782974/cost_rates?page=1&per_page=100",
                body=json.dumps(cost_rates_dict),
                status=200
            )
        user_cost_rates = from_dict(data_class=UserCostRates, data=cost_rates_dict)
        requested_user_cost_rates = self.harvest.user_cost_rates(user_id= 1782974)
        self.assertEqual(requested_user_cost_rates, user_cost_rates)

        # get_user_cost_rate
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/users/1782974/cost_rates/125068554",
                body=json.dumps(cost_rate_125068554_dict),
                status=200
            )
        user_cost_rate = from_dict(data_class=CostRate, data=cost_rate_125068554_dict)
        requested_user_cost_rate = self.harvest.get_user_cost_rate(user_id= 1782974, cost_rate_id= 125068554)
        self.assertEqual(requested_user_cost_rate, user_cost_rate)

        # create_user_cost_rate
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/users/1782974/cost_rates",
                body=json.dumps(cost_rate_125068758_dict),
                status=201
            )
        created_user_cost_rate = from_dict(data_class=CostRate, data=cost_rate_125068758_dict)
        requested_created_user_cost_rate = self.harvest.create_user_cost_rate(user_id= 1782974, amount= 150.0, start_date= "2019-01-01")
        self.assertEqual(requested_created_user_cost_rate, created_user_cost_rate)

        httpretty.reset()

    def test_project_assignments(self):
        project_assignment_125068554_dict = {
                "id":125068554,
                "is_project_manager":True,
                "is_active":True,
                "use_default_rates":True,
                "budget":None,
                "created_at":"2017-06-26T22:32:52Z",
                "updated_at":"2017-06-26T22:32:52Z",
                "hourly_rate":100.0,
                "project":{
                "id":14308069,
                "name":"Online Store - Phase 1",
                "code":"OS1"
                },
                "client":{
                "id":5735776,
                "name":"123 Industries"
                },
                "task_assignments":[
                    {
                        "id":155505013,
                        "billable":True,
                        "is_active":True,
                        "created_at":"2017-06-26T21:52:18Z",
                        "updated_at":"2017-06-26T21:52:18Z",
                        "hourly_rate":100.0,
                        "budget":None,
                        "task":{
                                "id":8083365,
                                "name":"Graphic Design"
                            }
                    },
                    {
                        "id":155505014,
                        "billable":True,
                        "is_active":True,
                        "created_at":"2017-06-26T21:52:18Z",
                        "updated_at":"2017-06-26T21:52:18Z",
                        "hourly_rate":100.0,
                        "budget":None,
                        "task":{
                                "id":8083366,
                                "name":"Programming"
                            }
                    },
                    {
                        "id":155505015,
                        "billable":True,
                        "is_active":True,
                        "created_at":"2017-06-26T21:52:18Z",
                        "updated_at":"2017-06-26T21:52:18Z",
                        "hourly_rate":100.0,
                        "budget":None,
                        "task":{
                                "id":8083368,
                                "name":"Project Management"
                            }
                    },
                    {
                        "id":155505016,
                        "billable":False,
                        "is_active":True,
                        "created_at":"2017-06-26T21:52:18Z",
                        "updated_at":"2017-06-26T21:54:06Z",
                        "hourly_rate":100.0,
                        "budget":None,
                        "task":{
                                "id":8083369,
                                "name":"Research"
                            }
                    }
                ]
            }

        project_assignment_125068553_dict = {
                "id":125068553,
                "is_project_manager":True,
                "is_active":True,
                "use_default_rates":False,
                "budget":None,
                "created_at":"2017-06-26T22:32:52Z",
                "updated_at":"2017-06-26T22:32:52Z",
                "hourly_rate":100.0,
                "project":{
                        "id":14307913,
                        "name":"Marketing Website",
                        "code":"MW"
                    },
                "client":{
                        "id":5735774,
                        "name":"ABC Corp"
                    },
                "task_assignments":[
                        {
                            "id":155502709,
                            "billable":True,
                            "is_active":True,
                            "created_at":"2017-06-26T21:36:23Z",
                            "updated_at":"2017-06-26T21:36:23Z",
                            "hourly_rate":100.0,
                            "budget":None,
                            "task":{
                                    "id":8083365,
                                    "name":"Graphic Design"
                                }
                        },
                        {
                            "id":155502710,
                            "billable":True,
                            "is_active":True,
                            "created_at":"2017-06-26T21:36:23Z",
                            "updated_at":"2017-06-26T21:36:23Z",
                            "hourly_rate":100.0,
                            "budget":None,
                            "task":{
                                    "id":8083366,
                                    "name":"Programming"
                                }
                        },
                        {
                            "id":155502711,
                            "billable":True,
                            "is_active":True,
                            "created_at":"2017-06-26T21:36:23Z",
                            "updated_at":"2017-06-26T21:36:23Z",
                            "hourly_rate":100.0,
                            "budget":None,
                            "task":{
                                    "id":8083368,
                                    "name":"Project Management"
                                }
                        },
                        {
                            "id":155505153,
                            "billable":False,
                            "is_active":True,
                            "created_at":"2017-06-26T21:53:20Z",
                            "updated_at":"2017-06-26T21:54:31Z",
                            "hourly_rate":100.0,
                            "budget":None,
                            "task":{
                                    "id":8083369,
                                    "name":"Research"
                                }
                        }
                    ]
            }

        project_assignment_125066109_dict = {
            "id":125066109,
            "is_project_manager":True,
            "is_active":True,
            "use_default_rates":True,
            "budget":None,
            "created_at":"2017-06-26T21:52:18Z",
            "updated_at":"2017-06-26T21:52:18Z",
            "hourly_rate":100.0,
            "project":{
                    "id":14308069,
                    "name":"Online Store - Phase 1",
                    "code":"OS1"
                },
            "client":{
                    "id":5735776,
                    "name":"123 Industries"
                },
            "task_assignments":[
                {
                    "id":155505013,
                    "billable":True,
                    "is_active":True,
                    "created_at":"2017-06-26T21:52:18Z",
                    "updated_at":"2017-06-26T21:52:18Z",
                    "hourly_rate":100.0,
                    "budget":None,
                    "task":{
                            "id":8083365,
                            "name":"Graphic Design"
                        }
                },
                {
                    "id":155505014,
                    "billable":True,
                    "is_active":True,
                    "created_at":"2017-06-26T21:52:18Z",
                    "updated_at":"2017-06-26T21:52:18Z",
                    "hourly_rate":100.0,
                    "budget":None,
                    "task":{
                            "id":8083366,
                            "name":"Programming"
                        }
                },
                    {
                        "id":155505015,
                        "billable":True,
                        "is_active":True,
                        "created_at":"2017-06-26T21:52:18Z",
                        "updated_at":"2017-06-26T21:52:18Z",
                        "hourly_rate":100.0,
                        "budget":None,
                        "task":{
                                "id":8083368,
                                "name":"Project Management"
                            }
                },
                    {
                        "id":155505016,
                        "billable":False,
                        "is_active":True,
                        "created_at":"2017-06-26T21:52:18Z",
                        "updated_at":"2017-06-26T21:54:06Z",
                        "hourly_rate":100.0,
                        "budget":None,
                        "task":{
                                "id":8083369,
                                "name":"Research"
                            }
                    }
                ]
            }



        project_assignment_125063975_dict = {
                "id":125063975,
                "is_project_manager":True,
                "is_active":True,
                "use_default_rates":False,
                "budget":None,
                "created_at":"2017-06-26T21:36:23Z",
                "updated_at":"2017-06-26T21:36:23Z",
                "hourly_rate":100.0,
                "project":{
                        "id":14307913,
                        "name":"Marketing Website",
                        "code":"MW"
                    },
                "client":{
                        "id":5735774,
                        "name":"ABC Corp"
                    },
                "task_assignments":[
                    {
                        "id":155502709,
                        "billable":True,
                        "is_active":True,
                        "created_at":"2017-06-26T21:36:23Z",
                        "updated_at":"2017-06-26T21:36:23Z",
                        "hourly_rate":100.0,
                        "budget":None,
                        "task":{
                                "id":8083365,
                                "name":"Graphic Design"
                            }
                    },
                    {
                        "id":155502710,
                        "billable":True,
                        "is_active":True,
                        "created_at":"2017-06-26T21:36:23Z",
                        "updated_at":"2017-06-26T21:36:23Z",
                        "hourly_rate":100.0,
                        "budget":None,
                        "task":{
                                "id":8083366,
                                "name":"Programming"
                            }
                    },
                    {
                        "id":155502711,
                        "billable":True,
                        "is_active":True,
                        "created_at":"2017-06-26T21:36:23Z",
                        "updated_at":"2017-06-26T21:36:23Z",
                        "hourly_rate":100.0,
                        "budget":None,
                        "task":{
                                "id":8083368,
                                "name":"Project Management"
                            }
                    },
                    {
                        "id":155505153,
                        "billable":False,
                        "is_active":True,
                        "created_at":"2017-06-26T21:53:20Z",
                        "updated_at":"2017-06-26T21:54:31Z",
                        "hourly_rate":100.0,
                        "budget":None,
                        "task":{
                                "id":8083369,
                                "name":"Research"
                            }
                    }
                ]
            }

        project_assignments_dict = {
                "project_assignments":[project_assignment_125068554_dict, project_assignment_125068553_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":2,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/users/1782959/project_assignments?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/users/1782959/project_assignments?page=1&per_page=100"
                    }
            }

        my_project_assignments_dict = {
                "project_assignments":[project_assignment_125066109_dict, project_assignment_125063975_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":2,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/users/1782884/project_assignments?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/users/1782884/project_assignments?page=1&per_page=100"
                    }
            }

        # project_assignments
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/users/1782959/project_assignments?page=1&per_page=100",
                body=json.dumps(project_assignments_dict),
                status=200
            )
        project_assignments = from_dict(data_class=ProjectAssignments, data=project_assignments_dict)
        requested_project_assignments = self.harvest.project_assignments(user_id= 1782959)
        self.assertEqual(requested_project_assignments, project_assignments)

        # my_project_assignments
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/users/me/project_assignments?page=1&per_page=100",
                body=json.dumps(my_project_assignments_dict),
                status=200
            )
        my_project_assignments = from_dict(data_class=ProjectAssignments, data=my_project_assignments_dict)
        requested_my_project_assignments = self.harvest.my_project_assignments()
        self.assertEqual(requested_my_project_assignments, my_project_assignments)

        httpretty.reset()

    def test_users(self):

        user_1782974_dict = {
                "id":1782974,
                "first_name":"Jim",
                "last_name":"Allen",
                "email":"jimallen@example.com",
                "telephone":"",
                "timezone":"Mountain Time (US & Canada)",
                "has_access_to_all_future_projects":False,
                "is_contractor":False,
                "is_admin":False,
                "is_project_manager":False,
                "can_see_rates":False,
                "can_create_projects":False,
                "can_create_invoices":False,
                "is_active":True,
                "created_at":"2017-06-26T22:34:41Z",
                "updated_at":"2017-06-26T22:34:52Z",
                "weekly_capacity":126000,
                "default_hourly_rate":100.0,
                "cost_rate":50.0,
                "roles":["Developer"],
                "avatar_url":"https://cache.harvestapp.com/assets/profile_images/abraj_albait_towers.png?1498516481"
            }

        user_1782959_dict = {
                "id":1782959,
                "first_name":"Kim",
                "last_name":"Allen",
                "email":"kimallen@example.com",
                "telephone":"",
                "timezone":"Eastern Time (US & Canada)",
                "has_access_to_all_future_projects":True,
                "is_contractor":False,
                "is_admin":False,
                "is_project_manager":True,
                "can_see_rates":False,
                "can_create_projects":False,
                "can_create_invoices":False,
                "is_active":True,
                "created_at":"2017-06-26T22:15:45Z",
                "updated_at":"2017-06-26T22:32:52Z",
                "weekly_capacity":126000,
                "default_hourly_rate":100.0,
                "cost_rate":50.0,
                "roles":["Designer"],
                "avatar_url":"https://cache.harvestapp.com/assets/profile_images/cornell_clock_tower.png?1498515345"
            }

        user_1782884_dict = {
                "id":1782884,
                "first_name":"Bob",
                "last_name":"Powell",
                "email":"bobpowell@example.com",
                "telephone":"",
                "timezone":"Mountain Time (US & Canada)",
                "has_access_to_all_future_projects":False,
                "is_contractor":False,
                "is_admin":True,
                "is_project_manager":False,
                "can_see_rates":True,
                "can_create_projects":True,
                "can_create_invoices":True,
                "is_active":True,
                "created_at":"2017-06-26T20:41:00Z",
                "updated_at":"2017-06-26T20:42:25Z",
                "weekly_capacity":126000,
                "default_hourly_rate":100.0,
                "cost_rate":75.0,
                "roles":["Founder", "CEO"],
                "avatar_url":"https://cache.harvestapp.com/assets/profile_images/allen_bradley_clock_tower.png?1498509661"
            }

        user_3_dict = {
                "id": 3,
                "first_name": "George",
                "last_name": "Frank",
                "email": "george@example.com",
                "telephone": "",
                "timezone": "Eastern Time (US & Canada)",
                "has_access_to_all_future_projects": False,
                "is_contractor": False,
                "is_admin": False,
                "is_project_manager": True,
                "can_see_rates": False,
                "can_create_projects": False,
                "can_create_invoices": False,
                "is_active": True,
                "weekly_capacity":126000,
                "default_hourly_rate": 0.0, # TODO: this is supposed to be an int. Something isn't casting int to float.
                "cost_rate": 0.0, # TODO: this is supposed to be an int. Something isn't casting int to float.
                "roles": ["Project Manager"],
                "avatar_url": "https://{ACCOUNT_SUBDOMAIN}.harvestapp.com/assets/profile_images/big_ben.png?1485372046",
                "created_at": "2017-01-25T19:20:46Z",
                "updated_at": "2017-01-25T19:20:57Z"
            }

        user_2_dict = {
                "id": 2,
                "first_name": "Project",
                "last_name": "Manager",
                "email": "pm@example.com",
                "telephone": "888-555-1212",
                "timezone": "Eastern Time (US & Canada)",
                "has_access_to_all_future_projects": True,
                "is_contractor": False,
                "is_admin": False,
                "is_project_manager": True,
                "can_see_rates": True,
                "can_create_projects": True,
                "can_create_invoices": True,
                "is_active": True,
                "weekly_capacity":126000,
                "default_hourly_rate": 120.0, # TODO: this is supposed to be an int. Something isn't casting int to float.
                "cost_rate": 50.0, # TODO: this is supposed to be an int. Something isn't casting int to float.
                "roles": ["Project Manager"],
                "avatar_url": "https://{ACCOUNT_SUBDOMAIN}.harvestapp.com/assets/profile_images/big_ben.png?1485372046",
                "created_at": "2017-01-25T19:20:46Z",
                "updated_at": "2017-01-25T19:20:57Z"
            }

        users_dict = {
                "users":[user_1782974_dict, user_1782959_dict, user_1782884_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":3,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/users?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/users?page=1&per_page=100"
                    }
            }

        # users
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/users?page=1&per_page=100",
                body=json.dumps(users_dict),
                status=200
            )
        users = from_dict(data_class=Users, data=users_dict)
        requested_users = self.harvest.users()
        self.assertEqual(requested_users, users)

        # get_currently_authenticated_user
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/users/me",
                body=json.dumps(user_1782884_dict),
                status=200
            )
        me = from_dict(data_class=User, data=user_1782884_dict)
        requested_me = self.harvest.get_currently_authenticated_user()
        self.assertEqual(requested_me, me)

        # get_user
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/users/1782974",
                body=json.dumps(user_1782974_dict),
                status=200
            )
        user = from_dict(data_class=User, data=user_1782974_dict)
        requested_user = self.harvest.get_user(user_id= 1782974)
        self.assertEqual(requested_user, user)

        # create_user
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/users",
                body=json.dumps(user_3_dict),
                status=201
            )
        created_user = from_dict(data_class=User, data=user_3_dict)
        requested_created_user = self.harvest.create_user(email= "george@example.com", first_name= "George", last_name= "Frank", is_project_manager= True)
        self.assertEqual(requested_created_user, created_user)

        # update_user
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/users/2",
                body=json.dumps(user_2_dict),
                status=200
            )
        updated_user = from_dict(data_class=User, data=user_2_dict)
        requested_updated_user = self.harvest.update_user(user_id= 2, telephone= "888-555-1212")
        self.assertEqual(requested_updated_user, updated_user)

        # delete_user
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/users/2",
                status=200
            )
        requested_deleted_user = self.harvest.delete_user(user_id= 2)
        self.assertEqual(requested_deleted_user, None)

if __name__ == '__main__':
    unittest.main()
