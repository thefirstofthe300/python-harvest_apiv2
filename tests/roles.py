
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

class TestRoles(unittest.TestCase):

    def setUp(self):
        personal_access_token = PersonalAccessToken('ACCOUNT_NUMBER', 'PERSONAL_ACCESS_TOKEN')
        self.harvest = harvest.Harvest('https://api.harvestapp.com/api/v2', personal_access_token)
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*") # There's a bug in httpretty ATM.
        httpretty.enable()

    def teardown(self):
        httpretty.reset()
        httpretty.disable()


    def test_roles(self):

        role_1782974_dict = {
                "id": 1782974,
                "name": "Founder",
                "user_ids": [8083365],
                "created_at": "2017-06-26T22:34:41Z",
                "updated_at": "2017-06-26T22:34:52Z"
            }

        role_1782959_dict = {
                "id": 1782959,
                "name": "Developer",
                "user_ids": [8083366],
                "created_at": "2017-06-26T22:15:45Z",
                "updated_at": "2017-06-26T22:32:52Z"
            }

        role_1782884_dict = {
                "id": 1782884,
                "name": "Designer",
                "user_ids": [8083367],
                "created_at": "2017-06-26T20:41:00Z",
                "updated_at": "2017-06-26T20:42:25Z"
            }

        role_2_dict = {
                "id": 2,
                "name": "Project Manager",
                "user_ids": [8083365, 8083366],
                "created_at": "2017-06-26T22:34:41Z",
                "updated_at": "2017-06-26T22:34:52Z"
            }

        roles_dict = {
                "roles": [role_1782974_dict, role_1782959_dict, role_1782884_dict],
                "per_page": 100,
                "total_pages": 1,
                "total_entries": 3,
                "next_page": None,
                "previous_page": None,
                "page": 1,
                "links": {
                        "first": "https://api.harvestapp.com/v2/roles?page=1&per_page=100",
                        "next": None,
                        "previous": None,
                        "last": "https://api.harvestapp.com/v2/roles?page=1&per_page=100"
                    }
            }

        # roles
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/roles?page=1&per_page=100",
                body=json.dumps(roles_dict),
                status=200
            )
        roles = from_dict(data_class=Roles, data=roles_dict)
        requested_roles = self.harvest.roles()
        self.assertEqual(requested_roles, roles)

        # get_role
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/roles/1782974",
                body=json.dumps(role_1782974_dict),
                status=200
            )
        role = from_dict(data_class=Role, data=role_1782974_dict)
        requested_role = self.harvest.get_role(role_id= 1782974)
        self.assertEqual(requested_role, role)

        # create_role
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/roles",
                body=json.dumps(role_2_dict),
                status=201
            )
        role = from_dict(data_class=Role, data=role_2_dict)
        requested_role = self.harvest.create_role(name= "Project Manager", user_ids= [8083365,8083366])
        self.assertEqual(requested_role, role)

        # update_role
        role_2_dict["name"] = "PM"
        role_2_dict["user_ids"] = [8083365,8083366,8083367]
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/roles/2",
                body=json.dumps(role_2_dict),
                status=200
            )
        new_role = from_dict(data_class=Role, data=role_2_dict)
        requested_new_role = self.harvest.update_role(role_id= 2, name= "PM", user_ids= [8083365,8083366,8083367])
        self.assertEqual(requested_new_role, new_role)

        # delete_project
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/roles/2",
                status=200
            )
        requested_deleted_role = self.harvest.delete_role(role_id= 2)
        self.assertEqual(requested_deleted_role, None)

        httpretty.reset()


if __name__ == '__main__':
    unittest.main()
