
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

class TestTasks(unittest.TestCase):

    def setUp(self):
        personal_access_token = PersonalAccessToken('ACCOUNT_NUMBER', 'PERSONAL_ACCESS_TOKEN')
        self.harvest = harvest.Harvest('https://api.harvestapp.com/api/v2', personal_access_token)
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*") # There's a bug in httpretty ATM.
        httpretty.enable()

    def teardown(self):
        httpretty.reset()
        httpretty.disable()


    def test_tasks(self):
        task_8083800_dict = {
                "id":8083800,
                "name":"Business Development",
                "billable_by_default":False,
                "default_hourly_rate":0.0,
                "is_default":False,
                "is_active":True,
                "created_at":"2017-06-26T22:08:25Z",
                "updated_at":"2017-06-26T22:08:25Z"
            }

        task_8083369_dict = {
                "id":8083369,
                "name":"Research",
                "billable_by_default":False,
                "default_hourly_rate":0.0,
                "is_default":True,
                "is_active":True,
                "created_at":"2017-06-26T20:41:00Z",
                "updated_at":"2017-06-26T21:53:34Z"
            }

        task_8083368_dict = {
                "id":8083368,
                "name":"Project Management",
                "billable_by_default":True,
                "default_hourly_rate":100.0,
                "is_default":True,
                "is_active":True,
                "created_at":"2017-06-26T20:41:00Z",
                "updated_at":"2017-06-26T21:14:10Z"
            }

        task_8083366_dict = {
                "id":8083366,
                "name":"Programming",
                "billable_by_default":True,
                "default_hourly_rate":100.0,
                "is_default":True,
                "is_active":True,
                "created_at":"2017-06-26T20:41:00Z",
                "updated_at":"2017-06-26T21:14:07Z"
            }

        task_8083365_dict = {
                "id":8083365,
                "name":"Graphic Design",
                "billable_by_default":True,
                "default_hourly_rate":100.0,
                "is_default":True,
                "is_active":True,
                "created_at":"2017-06-26T20:41:00Z",
                "updated_at":"2017-06-26T21:14:02Z"
            }

        task_8083782_dict = {
                "id":8083782,
                "name":"New Task Name",
                "billable_by_default":True,
                "default_hourly_rate":0.0, # TODO: this is supposed to be an int. Something isn't casting int to float.
                "is_default":False,
                "is_active":True,
                "created_at":"2017-06-26T22:04:31Z",
                "updated_at":"2017-06-26T22:04:31Z"
            }

        tasks_dict = {
                "tasks":[task_8083800_dict, task_8083369_dict, task_8083368_dict, task_8083366_dict, task_8083365_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":5,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/tasks?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/tasks?page=1&per_page=100"
                    }
            }

        # tasks
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/tasks?page=1&per_page=100",
                body=json.dumps(tasks_dict),
                status=200
            )
        tasks = from_dict(data_class=Tasks, data=tasks_dict)
        requested_tasks = self.harvest.tasks()
        self.assertEqual(requested_tasks, tasks)

        # get_task
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/tasks/8083800",
                body=json.dumps(task_8083800_dict),
                status=200
            )
        task = from_dict(data_class=Task, data=task_8083800_dict)
        requested_task = self.harvest.get_task(task_id= 8083800)
        self.assertEqual(requested_task, task)

        # create_task
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/tasks",
                body=json.dumps(task_8083782_dict),
                status=201
            )
        new_task = from_dict(data_class=Task, data=task_8083782_dict)
        requested_new_task = self.harvest.create_task(name= "New Task Name", default_hourly_rate= 120.0) # Harvest doco is wrong. they use hourly_rate not default_hourly_rate
        self.assertEqual(requested_new_task, new_task)

        # update_task
        task_8083782_dict["is_default"] = True
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/tasks/8083782",
                body=json.dumps(task_8083782_dict),
                status=200
            )
        updated_task = from_dict(data_class=Task, data=task_8083782_dict)
        requested_updated_task = self.harvest.update_task(task_id=8083782, is_default=True)
        self.assertEqual(requested_updated_task, updated_task)

        # delete_task
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/tasks/8083782",
                status=200
            )
        requested_deleted_task = self.harvest.delete_task(task_id=8083782)
        self.assertEqual(requested_deleted_task, None)

        httpretty.reset()




if __name__ == '__main__':
    unittest.main()
