
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

class TestClients(unittest.TestCase):

    def setUp(self):
        personal_access_token = PersonalAccessToken('ACCOUNT_NUMBER', 'PERSONAL_ACCESS_TOKEN')
        self.harvest = harvest.Harvest('https://api.harvestapp.com/api/v2', personal_access_token)
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*") # There's a bug in httpretty ATM.
        httpretty.enable()

    def teardown(self):
        httpretty.reset()
        httpretty.disable()


    def test_client_contacts(self):
        contact_4706479_dict = {
                "id":4706479,
                "title":"Owner",
                "first_name":"Jane",
                "last_name":"Doe",
                "email":"janedoe@example.com",
                "phone_office":"(203) 697-8885",
                "phone_mobile":"(203) 697-8886",
                "fax":"(203) 697-8887",
                "created_at":"2017-06-26T21:20:07Z",
                "updated_at":"2017-06-26T21:27:07Z",
                "client":{
                        "id":5735774,
                        "name":"ABC Corp"
                    }
            }

        contact_4706453_dict = {
                "id":4706453,
                "title":"Manager",
                "first_name":"Richard",
                "last_name":"Roe",
                "email":"richardroe@example.com",
                "phone_office":"(318) 515-5905",
                "phone_mobile":"(318) 515-5906",
                "fax":"(318) 515-5907",
                "created_at":"2017-06-26T21:06:55Z",
                "updated_at":"2017-06-26T21:27:20Z",
                "client":{
                        "id":5735776,
                        "name":"123 Industries"
                    }
            }

        contact_4706510_dict = {
                "id":4706510,
                "title":None,
                "first_name":"George",
                "last_name":"Frank",
                "email":"georgefrank@example.com",
                "phone_office":"",
                "phone_mobile":"",
                "fax":"",
                "created_at":"2017-06-26T21:44:57Z",
                "updated_at":"2017-06-26T21:44:57Z",
                "client":{
                        "id":5735776,
                        "name":"123 Industries"
                    }
            }

        contacts_dict = {
                "contacts":[contact_4706479_dict, contact_4706453_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":2,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/contacts?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/contacts?page=1&per_page=100"
                    }
            }

        # client_contacts
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/contacts?page=1&per_page=100",
                body=json.dumps(contacts_dict),
                status=200
            )
        client_contacts = from_dict(data_class=ClientContacts, data=contacts_dict)
        requested_client_contacts = self.harvest.client_contacts()
        self.assertEqual(requested_client_contacts, client_contacts)

        # get_client_contact
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/contacts/4706479",
                body=json.dumps(contact_4706479_dict),
                status=200
            )
        client_contact = from_dict(data_class=ClientContact, data=contact_4706479_dict)
        requested_client_contact = self.harvest.get_client_contact(contact_id= 4706479)
        self.assertEqual(requested_client_contact, client_contact)

        # create_client_contact
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/contacts",
                body=json.dumps(contact_4706510_dict),
                status=200
            )
        new_client_contact = from_dict(data_class=ClientContact, data=contact_4706510_dict)
        requested_new_client_contact = self.harvest.create_client_contact(client_id= 5735776, first_name= "George", last_name= "Frank", email= "georgefrank@example.com")
        self.assertEqual(requested_new_client_contact, new_client_contact)

        # update_client_contact
        contact_4706510_dict["title"] = "Owner"
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/contacts/4706510",
                body=json.dumps(contact_4706510_dict),
                status=200
            )
        updated_client_contact = from_dict(data_class=ClientContact, data=contact_4706510_dict)
        requested_updated_client_contact = self.harvest.update_client_contact(contact_id=4706510, title= "Owner")
        self.assertEqual(requested_updated_client_contact, updated_client_contact)

        # delete_client_contact
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/contacts/4706510",
                status=200
            )
        requested_deleted_client_contact = self.harvest.delete_client_contact(contact_id=4706510)
        self.assertEqual(requested_deleted_client_contact, None)

        httpretty.reset()


    def test_clients(self):

        client_5735776_dict = {
                "id":5735776,
                "name":"123 Industries",
                "is_active":True,
                "address":"123 Main St.\r\nAnytown, LA 71223",
                "created_at":"2017-06-26T21:02:12Z",
                "updated_at":"2017-06-26T21:34:11Z",
                "currency":"EUR"
            }

        client_5735774_dict = {
                "id":5735774,
                "name":"ABC Corp",
                "is_active":True,
                "address":"456 Main St.\r\nAnytown, CT 06467",
                "created_at":"2017-06-26T21:01:52Z",
                "updated_at":"2017-06-26T21:27:07Z",
                "currency":"USD"
            }

        client_5737336_dict = {
                "id":5737336,
                "name":"Your New Client",
                "is_active":True,
                "address":None,
                "created_at":"2017-06-26T21:39:35Z",
                "updated_at":"2017-06-26T21:39:35Z",
                "currency":"EUR"
            }

        clients_dict = {
                "clients":[client_5735776_dict, client_5735774_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":2,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                    "first":"https://api.harvestapp.com/v2/clients?page=1&per_page=100",
                    "next":None,
                    "previous":None,
                    "last":"https://api.harvestapp.com/v2/clients?page=1&per_page=100"
                }
            }

        # clients
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/clients?page=1&per_page=100",
                body=json.dumps(clients_dict),
                status=200
            )
        clients = from_dict(data_class=Clients, data=clients_dict)
        requested_clients = self.harvest.clients()
        self.assertEqual(requested_clients, clients)

        # get_client
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/clients/5735776",
                body=json.dumps(client_5735776_dict),
                status=200
            )
        client = from_dict(data_class=Client, data=client_5735776_dict)
        requested_client = self.harvest.get_client(client_id= 5735776)
        self.assertEqual(requested_client, client)

        # create_client
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/clients",
                body=json.dumps(client_5737336_dict),
                status=200
            )
        new_client = from_dict(data_class=Client, data=client_5737336_dict)
        requested_new_client = self.harvest.create_client(name= "Your New Client", currency= "EUR")
        self.assertEqual(requested_new_client, new_client)

        # update_client
        client_5737336_dict["is_active"] = False
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/clients/5737336",
                body=json.dumps(client_5737336_dict),
                status=200
            )
        updated_client = from_dict(data_class=Client, data=client_5737336_dict)
        requested_updated_client = self.harvest.update_client(client_id= 5737336, is_active= False)
        self.assertEqual(requested_updated_client, updated_client)

        # delete_client
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/clients/5737336",
                status=200
            )
        requested_deleted_client = self.harvest.delete_client(client_id= 5737336)
        self.assertEqual(requested_deleted_client, None)


        httpretty.reset()


if __name__ == '__main__':
    unittest.main()
