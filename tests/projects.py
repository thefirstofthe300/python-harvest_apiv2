
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

class TestProjects(unittest.TestCase):

    def setUp(self):
        personal_access_token = PersonalAccessToken('ACCOUNT_NUMBER', 'PERSONAL_ACCESS_TOKEN')
        self.harvest = harvest.Harvest('https://api.harvestapp.com/api/v2', personal_access_token)
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*") # There's a bug in httpretty ATM.
        httpretty.enable()

    def teardown(self):
        httpretty.reset()
        httpretty.disable()

    def test_project_user_assignments(self):
        user_assignment_130403297_dict = {
                "id":130403297,
                "is_project_manager":True,
                "is_active":True,
                "use_default_rates":False,
                "budget":None,
                "created_at":"2017-08-22T17:36:54Z",
                "updated_at":"2017-08-22T17:36:54Z",
                "hourly_rate":100.0,
                "project":{
                        "id":14808188,
                        "name":"Task Force",
                        "code":"TF"
                    },
                "user":{
                        "id":1782959,
                        "name":"Kim Allen"
                    }
            }

        user_assignment_130403296_dict = {
                "id":130403296,
                "is_project_manager":True,
                "is_active":True,
                "use_default_rates":True,
                "budget":None,
                "created_at":"2017-08-22T17:36:54Z",
                "updated_at":"2017-08-22T17:36:54Z",
                "hourly_rate":100.0,
                "project":{
                        "id":14808188,
                        "name":"Task Force",
                        "code":"TF"
                    },
                "user":{
                        "id":1795925,
                        "name":"Jason Dew"
                    }
            }

        user_assignment_125068554_dict = {
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
                "user":{
                        "id":1782959,
                        "name":"Kim Allen"
                    }
            }


        user_assignment_125068553_dict = {
                "id":125068553,
                "is_project_manager":True,
                "is_active":True,
                "use_default_rates":True,
                "budget":None,
                "created_at":"2017-06-26T22:32:52Z",
                "updated_at":"2017-06-26T22:32:52Z",
                "hourly_rate":100.0,
                "project":{
                        "id":14307913,
                        "name":"Marketing Website",
                        "code":"MW"
                    },
                "user":{
                        "id":1782959,
                        "name":"Kim Allen"
                    }
            }

        user_assignment_125066109_dict = {
                "id":125066109,
                "is_project_manager":True,
                "is_active":True,
                "use_default_rates":False,
                "budget":None,
                "created_at":"2017-06-26T21:52:18Z",
                "updated_at":"2017-06-26T21:52:18Z",
                "hourly_rate":100.0,
                "project":{
                        "id":14308069,
                        "name":"Online Store - Phase 1",
                        "code":"OS1"
                    },
                "user":{
                        "id":1782884,
                        "name":"Jeremy Israelsen"
                    }
            }

        user_assignment_125063975_dict = {
                "id":125063975,
                "is_project_manager":True,
                "is_active":True,
                "use_default_rates":True,
                "budget":None,
                "created_at":"2017-06-26T21:36:23Z",
                "updated_at":"2017-06-26T21:36:23Z",
                "hourly_rate":100.0,
                "project":{
                        "id":14307913,
                        "name":"Marketing Website",
                        "code":"MW"
                    },
                "user":{
                        "id":1782884,
                        "name":"Jeremy Israelsen"
                    }
            }

        user_assignment_125068758_dict = {
                "id":125068758,
                "is_project_manager":False,
                "is_active":True,
                "use_default_rates":False,
                "budget":None,
                "created_at":"2017-06-26T22:36:01Z",
                "updated_at":"2017-06-26T22:36:01Z",
                "hourly_rate":75.5,
                "project":{
                        "id":14308069,
                        "name":"Online Store - Phase 1",
                        "code":"OS1"
                    },
                "user":{
                        "id":1782974,
                        "name":"Jim Allen"
                    }
            }

        user_assignments_dict = {
                "user_assignments":[user_assignment_130403297_dict, user_assignment_130403296_dict, user_assignment_125068554_dict, user_assignment_125068553_dict, user_assignment_125066109_dict, user_assignment_125063975_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":6,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/user_assignments?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/user_assignments?page=1&per_page=100"
                    }
            }

        project_user_assignments_dict = {
                "user_assignments":[user_assignment_125068554_dict, user_assignment_125066109_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":2,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/projects/14308069/user_assignments?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/projects/14308069/user_assignments?page=1&per_page=100"
                    }
            }

        # user_assignments
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/user_assignments?page=1&per_page=100",
                body=json.dumps(user_assignments_dict),
                status=200
            )
        user_assignments = from_dict(data_class=UserAssignments, data=user_assignments_dict)
        requested_user_assignments = self.harvest.user_assignments()
        self.assertEqual(requested_user_assignments, user_assignments)

        # project_user_assignments
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/projects/14308069/user_assignments",
                body=json.dumps(project_user_assignments_dict),
                status=200
            )
        project_user_assignments = from_dict(data_class=UserAssignments, data=project_user_assignments_dict)
        requested_project_user_assignments = self.harvest.project_user_assignments(project_id= 14308069)
        self.assertEqual(requested_project_user_assignments, project_user_assignments)

        # get_user_assignment
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/projects/14308069/user_assignments/125068554",
                body=json.dumps(user_assignment_125068554_dict),
                status=200
            )
        user_assignment = from_dict(data_class=UserAssignment, data=user_assignment_125068554_dict)
        requested_user_assignment = self.harvest.get_user_assignment(project_id= 14308069, user_assignment_id= 125068554)
        self.assertEqual(requested_user_assignment, user_assignment)

        # create_user_assignment
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/projects/14308069/user_assignments",
                body=json.dumps(user_assignment_125068758_dict),
                status=201
            )
        created_user_assignment = from_dict(data_class=UserAssignment, data=user_assignment_125068758_dict)
        requested_created_user_assignment = self.harvest.create_user_assignment(project_id= 14308069, user_id= 1782974, use_default_rates= False, hourly_rate= 75.50)
        self.assertEqual(requested_created_user_assignment, created_user_assignment)

        # update_user_assignment
        user_assignment_125068758_dict['budget'] = 120.0 # TODO: this is supposed to be an int. Something isn't casting int to float.
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/projects/14308069/user_assignments/125068758",
                body=json.dumps(user_assignment_125068758_dict),
                status=200
            )
        updated_user_assignment = from_dict(data_class=UserAssignment, data=user_assignment_125068758_dict)
        requested_updated_user_assignment = self.harvest.update_user_assignment(project_id= 14308069, user_assignment_id= 125068758, budget= 120)
        self.assertEqual(requested_updated_user_assignment, updated_user_assignment)

        # delete_user_assignment
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/projects/14308069/user_assignments/125068758",
                status=200
            )
        requested_deleted_user_assignment = self.harvest.delete_user_assignment(project_id= 14308069, user_assignment_id= 125068758)
        self.assertEqual(requested_deleted_user_assignment, None)

        httpretty.reset()


    def test_project_task_assignments(self):
        task_assignment_160726647_dict = {
                "id":160726647,
                "billable":False,
                "is_active":True,
                "created_at":"2017-08-22T17:36:54Z",
                "updated_at":"2017-08-22T17:36:54Z",
                "hourly_rate":100.0,
                "budget":None,
                "project":{
                        "id":14808188,
                        "name":"Task Force",
                        "code":"TF"
                    },
                "task":{
                        "id":8083369,
                        "name":"Research"
                    }
            }

        task_assignment_160726646_dict = {
                "id":160726646,
                "billable":True,
                "is_active":True,
                "created_at":"2017-08-22T17:36:54Z",
                "updated_at":"2017-08-22T17:36:54Z",
                "hourly_rate":100.0,
                "budget":None,
                "project":{
                        "id":14808188,
                        "name":"Task Force",
                        "code":"TF"
                    },
                "task":{
                        "id":8083368,
                        "name":"Project Management"
                    }
            }

        task_assignment_160726645_dict = {
                "id":160726645,
                "billable":True,
                "is_active":True,
                "created_at":"2017-08-22T17:36:54Z",
                "updated_at":"2017-08-22T17:36:54Z",
                "hourly_rate":100.0,
                "budget":None,
                "project":{
                        "id":14808188,
                        "name":"Task Force",
                        "code":"TF"
                    },
                "task":{
                        "id":8083366,
                        "name":"Programming"
                    }
            }

        task_assignment_160726644_dict = {
                "id":160726644,
                "billable":True,
                "is_active":True,
                "created_at":"2017-08-22T17:36:54Z",
                "updated_at":"2017-08-22T17:36:54Z",
                "hourly_rate":100.0,
                "budget":None,
                "project":{
                        "id":14808188,
                        "name":"Task Force",
                        "code":"TF"
                    },
                "task":{
                        "id":8083365,
                        "name":"Graphic Design"
                    }
            }

        task_assignment_155505153_dict = {
                "id":155505153,
                "billable":False,
                "is_active":True,
                "created_at":"2017-06-26T21:53:20Z",
                "updated_at":"2017-06-26T21:54:31Z",
                "hourly_rate":100.0,
                "budget":None,
                "project":{
                        "id":14307913,
                        "name":"Marketing Website",
                        "code":"MW"
                    },
                "task":{
                        "id":8083369,
                        "name":"Research"
                    }
            }

        task_assignment_155505016_dict = {
                "id":155505016,
                "billable":False,
                "is_active":True,
                "created_at":"2017-06-26T21:52:18Z",
                "updated_at":"2017-06-26T21:54:06Z",
                "hourly_rate":100.0,
                "budget":None,
                "project":{
                        "id":14308069,
                        "name":"Online Store - Phase 1",
                        "code":"OS1"
                    },
                "task":{
                        "id":8083369,
                        "name":"Research"
                    }
            }

        task_assignment_155505015_dict = {
                "id":155505015,
                "billable":True,
                "is_active":True,
                "created_at":"2017-06-26T21:52:18Z",
                "updated_at":"2017-06-26T21:52:18Z",
                "hourly_rate":100.0,
                "budget":None,
                "project":{
                        "id":14308069,
                        "name":"Online Store - Phase 1",
                        "code":"OS1"
                    },
                "task":{
                        "id":8083368,
                        "name":"Project Management"
                    }
            }

        task_assignment_155505014_dict = {
                "id":155505014,
                "billable":True,
                "is_active":True,
                "created_at":"2017-06-26T21:52:18Z",
                "updated_at":"2017-06-26T21:52:18Z",
                "hourly_rate":100.0,
                "budget":None,
                "project":{
                    "id":14308069,
                    "name":"Online Store - Phase 1",
                    "code":"OS1"
                    },
                "task":{
                    "id":8083366,
                    "name":"Programming"
                    }
            }

        task_assignment_155505013_dict = {
                "id":155505013,
                "billable":True,
                "is_active":True,
                "created_at":"2017-06-26T21:52:18Z",
                "updated_at":"2017-06-26T21:52:18Z",
                "hourly_rate":100.0,
                "budget":None,
                "project":{
                        "id":14308069,
                        "name":"Online Store - Phase 1",
                        "code":"OS1"
                    },
                "task":{
                        "id":8083365,
                        "name":"Graphic Design"
                    }
            }

        task_assignment_155502711_dict = {
                "id":155502711,
                "billable":True,
                "is_active":True,
                "created_at":"2017-06-26T21:36:23Z",
                "updated_at":"2017-06-26T21:36:23Z",
                "hourly_rate":100.0,
                "budget":None,
                "project":{
                        "id":14307913,
                        "name":"Marketing Website",
                        "code":"MW"
                    },
                "task":{
                        "id":8083368,
                        "name":"Project Management"
                    }
            }

        task_assignment_155502710_dict = {
                "id":155502710,
                "billable":True,
                "is_active":True,
                "created_at":"2017-06-26T21:36:23Z",
                "updated_at":"2017-06-26T21:36:23Z",
                "hourly_rate":100.0,
                "budget":None,
                "project":{
                        "id":14307913,
                        "name":"Marketing Website",
                        "code":"MW"
                    },
                "task":{
                        "id":8083366,
                        "name":"Programming"
                    }
            }

        task_assignment_155502709_dict = {
                "id":155502709,
                "billable":True,
                "is_active":True,
                "created_at":"2017-06-26T21:36:23Z",
                "updated_at":"2017-06-26T21:36:23Z",
                "hourly_rate":100.0,
                "budget":None,
                "project":{
                        "id":14307913,
                        "name":"Marketing Website",
                        "code":"MW"
                    },
                "task":{
                        "id":8083365,
                        "name":"Graphic Design"
                    }
            }

        task_assignment_155506339_dict = {
                "id":155506339,
                "billable":True,
                "is_active":True,
                "created_at":"2017-06-26T22:10:43Z",
                "updated_at":"2017-06-26T22:10:43Z",
                "hourly_rate":75.5,
                "budget":None,
                "project":{
                        "id":14308069,
                        "name":"Online Store - Phase 1",
                        "code":"OS1"
                    },
                "task":{
                        "id":8083800,
                        "name":"Business Development"
                    }
            }

        task_assignments_dict = {
                "task_assignments": [task_assignment_160726647_dict, task_assignment_160726646_dict, task_assignment_160726645_dict, task_assignment_160726644_dict, task_assignment_155505153_dict, task_assignment_155505016_dict, task_assignment_155505015_dict, task_assignment_155505014_dict, task_assignment_155505013_dict, task_assignment_155502711_dict, task_assignment_155502710_dict, task_assignment_155502709_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":12,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/task_assignments?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/task_assignments?page=1&per_page=100"
                    }
            }

        task_assignments_project_14308069_dict = {
                "task_assignments":[task_assignment_155505016_dict, task_assignment_155505015_dict, task_assignment_155505014_dict, task_assignment_155505013_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":4,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/projects/14308069/task_assignments?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/projects/14308069/task_assignments?page=1&per_page=100"
                    }
            }

        # task_assignments
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/task_assignments?page=1&per_page=100",
                body=json.dumps(task_assignments_dict),
                status=200
            )
        task_assignments = from_dict(data_class=TaskAssignments, data=task_assignments_dict)
        requested_task_assignments = self.harvest.task_assignments()
        self.assertEqual(requested_task_assignments, task_assignments)

        # project_task_assignments
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/projects/14308069/task_assignments?page=1&per_page=100",
                body=json.dumps(task_assignments_project_14308069_dict),
                status=200
            )
        project_task_assignments = from_dict(data_class=TaskAssignments, data=task_assignments_project_14308069_dict)
        requested_project_task_assignments = self.harvest.project_task_assignments(project_id= 14308069)
        self.assertEqual(requested_project_task_assignments, project_task_assignments)

        # get_task_assignment
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/projects/14308069/task_assignments/155505016",
                body=json.dumps(task_assignment_155505016_dict),
                status=200
            )
        task_assignment = from_dict(data_class=TaskAssignment, data=task_assignment_155505016_dict)
        requested_task_assignment = self.harvest.get_task_assignment(project_id= 14308069, task_assignment_id= 155505016)
        self.assertEqual(requested_task_assignment, task_assignment)

        # create_task_assignment
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/projects/14308069/task_assignments",
                body=json.dumps(task_assignment_155506339_dict),
                status=201
            )
        new_task_assignment = from_dict(data_class=TaskAssignment, data=task_assignment_155506339_dict)
        requested_new_task_assignment = self.harvest.create_task_assignment(project_id= 14308069, task_id= 8083800, is_active= True, billable= True, hourly_rate= 75.50)
        self.assertEqual(requested_new_task_assignment, new_task_assignment)

        # update_task_assignment
        task_assignment_155506339_dict['budget'] = 120.0  # TODO: this is supposed to be an int. Something isn't casting int to float.
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/projects/14308069/task_assignments/155506339",
                body=json.dumps(task_assignment_155506339_dict),
                status=200
            )
        updated_task_assignment = from_dict(data_class=TaskAssignment, data=task_assignment_155506339_dict)
        requested_updated_task_assignment = self.harvest.update_task_assignment(project_id= 14308069, task_assignment_id= 155506339, budget= 120)
        self.assertEqual(requested_updated_task_assignment, updated_task_assignment)

        # delete_task_assignment
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/projects/14308069/task_assignments/155506339",
                status=200
            )
        requested_deleted_task_assignment = self.harvest.delete_task_assignment(project_id= 14308069, task_assignment_id= 155506339)
        self.assertEqual(requested_deleted_task_assignment, None)

        httpretty.reset()

    def test_projects(self):
        project_14308069_dict = {
                "id":14308069,
                "name":"Online Store - Phase 1",
                "code":"OS1",
                "is_active":True,
                "bill_by":"Project",
                "budget":200.0,
                "budget_by":"project",
                "budget_is_monthly":False,
                "notify_when_over_budget":True,
                "over_budget_notification_percentage":80.0,
                "over_budget_notification_date":None,
                "show_budget_to_all":False,
                "created_at":"2017-06-26T21:52:18Z",
                "updated_at":"2017-06-26T21:54:06Z",
                "starts_on":"2017-06-01",
                "ends_on":None,
                "is_billable":True,
                "is_fixed_fee":False,
                "notes":"",
                "client":{
                        "id":5735776,
                        "name":"123 Industries",
                        "currency":"EUR"
                    },
                "cost_budget":None,
                "cost_budget_include_expenses":False,
                "hourly_rate":100.0,
                "fee":None
            }

        project_14307913_dict = {
                "id":14307913,
                "name":"Marketing Website",
                "code":"MW",
                "is_active":True,
                "bill_by":"Project",
                "budget":50.0,
                "budget_by":"project",
                "budget_is_monthly":False,
                "notify_when_over_budget":True,
                "over_budget_notification_percentage":80.0,
                "over_budget_notification_date":None,
                "show_budget_to_all":False,
                "created_at":"2017-06-26T21:36:23Z",
                "updated_at":"2017-06-26T21:54:46Z",
                "starts_on":"2017-01-01",
                "ends_on":"2017-03-31",
                "is_billable":True,
                "is_fixed_fee":False,
                "notes":"",
                "client":{
                        "id":5735774,
                        "name":"ABC Corp",
                        "currency":"USD"
                    },
                "cost_budget":None,
                "cost_budget_include_expenses":False,
                "hourly_rate":100.0,
                "fee":None
            }

        project_14308112_dict = {
                "id":14308112,
                "name":"Your New Project",
                "code":None,
                "is_active":True,
                "bill_by":"Project",
                "budget":10000.0,
                "budget_by":"project",
                "budget_is_monthly":False,
                "notify_when_over_budget":False,
                "over_budget_notification_percentage":80.0,
                "over_budget_notification_date":None,
                "show_budget_to_all":False,
                "created_at":"2017-06-26T21:56:52Z",
                "updated_at":"2017-06-26T21:56:52Z",
                "starts_on":None,
                "ends_on":None,
                "is_billable":True,
                "is_fixed_fee":False,
                "notes":"",
                "client":{
                        "id":5735776,
                        "name":"123 Industries",
                        "currency":"EUR"
                    },
                "cost_budget":None,
                "cost_budget_include_expenses":False,
                "hourly_rate":100.0,
                "fee":None
            }

        project_dict = {
                "projects":[project_14308069_dict, project_14307913_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":2,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/projects?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/projects?page=1&per_page=100"
                    }
            }

        # projects
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/projects?page=1&per_page=100",
                body=json.dumps(project_dict),
                status=200
            )
        projects = from_dict(data_class=Projects, data=project_dict)
        requested_projects = self.harvest.projects()
        self.assertEqual(requested_projects, projects)

        # get_project
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/projects/14308069",
                body=json.dumps(project_14308069_dict),
                status=200
            )
        project = from_dict(data_class=Project, data=project_14308069_dict)
        requested_project = self.harvest.get_project(project_id= 14308069)
        self.assertEqual(requested_project, project)

        # create_project
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/projects",
                body=json.dumps(project_14308112_dict),
                status=201
            )
        new_project = from_dict(data_class=Project, data=project_14308112_dict)
        requested_new_project = self.harvest.create_project(client_id= 5735776, name= "Your New Project", is_billable= True, bill_by= "Project", hourly_rate= 100.0, budget_by= "project", budget= 10000)
        self.assertEqual(requested_new_project, new_project)

        # update_project
        project_14308112_dict["name"] = "New project name"
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/projects/14308112",
                body=json.dumps(project_14308112_dict),
                status=201
            )
        new_project = from_dict(data_class=Project, data=project_14308112_dict)
        requested_new_project = self.harvest.update_project(project_id= 14308112, name= "New project name")
        self.assertEqual(requested_new_project, new_project)

        # delete_project
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/projects/14308112",
                status=200
            )
        requested_deleted_project = self.harvest.delete_project(project_id= 14308112)
        self.assertEqual(requested_deleted_project, None)

        httpretty.reset()


if __name__ == '__main__':
    unittest.main()
