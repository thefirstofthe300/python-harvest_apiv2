
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

class TestEstimates(unittest.TestCase):

    def setUp(self):
        personal_access_token = PersonalAccessToken('ACCOUNT_NUMBER', 'PERSONAL_ACCESS_TOKEN')
        self.harvest = harvest.Harvest('https://api.harvestapp.com/api/v2', personal_access_token)
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*") # There's a bug in httpretty ATM.
        httpretty.enable()

    def teardown(self):
        httpretty.reset()
        httpretty.disable()

    def test_estimate_messages(self):
        estimate_message_2666236_dict = {
                "id":2666236,
                "sent_by":"Bob Powell",
                "sent_by_email":"bobpowell@example.com",
                "sent_from":"Bob Powell",
                "sent_from_email":"bobpowell@example.com",
                "send_me_a_copy":True,
                "created_at":"2017-08-25T21:23:40Z",
                "updated_at":"2017-08-25T21:23:40Z",
                "recipients":[
                    {
                        "name":"Richard Roe",
                        "email":"richardroe@example.com"
                    },
                    {
                        "name":"Bob Powell",
                        "email":"bobpowell@example.com"
                    }
                ],
                "event_type":None,
                "subject":"Estimate #1001 from API Examples",
                "body":"---------------------------------------------\r\nEstimate Summary\r\n---------------------------------------------\r\nEstimate ID: 1001\r\nEstimate Date: 06/01/2017\r\nClient: 123 Industries\r\nP.O. Number: 5678\r\nAmount: $9,630.00\r\n\r\nYou can view the estimate here:\r\n\r\n%estimate_url%\r\n\r\nThank you!\r\n---------------------------------------------"
            }

        estimate_message_2666240_dict = {
                "id":2666240,
                "sent_by":"Bob Powell",
                "sent_by_email":"bobpowell@example.com",
                "sent_from":"Bob Powell",
                "sent_from_email":"bobpowell@example.com",
                "send_me_a_copy":True,
                "created_at":"2017-08-25T21:27:52Z",
                "updated_at":"2017-08-25T21:27:52Z",
                "recipients":[
                    {
                        "name":"Richard Roe",
                        "email":"richardroe@example.com"
                    },
                    {
                        "name":"Bob Powell",
                        "email":"bobpowell@example.com"
                    }
                ],
                "event_type":None,
                "subject":"Estimate #1001",
                "body":"Here is our estimate."
            }

        estimate_message_2666241_dict = {
                "id":2666241,
                "sent_by":"Bob Powell",
                "sent_by_email":"bobpowell@example.com",
                "sent_from":"Bob Powell",
                "sent_from_email":"bobpowell@example.com",
                "send_me_a_copy":False,
                "created_at":"2017-08-23T22:25:59Z",
                "updated_at":"2017-08-23T22:25:59Z",
                "event_type":"send",
                "recipients":[],
                "subject":None,
                "body":None
            }

        estimate_message_2666244_dict = {
                "id":2666244,
                "sent_by":"Bob Powell",
                "sent_by_email":"bobpowell@example.com",
                "sent_from":"Bob Powell",
                "sent_from_email":"bobpowell@example.com",
                "send_me_a_copy":False,
                "created_at":"2017-08-25T21:31:55Z",
                "updated_at":"2017-08-25T21:31:55Z",
                "recipients":[],
                "event_type":"accept",
                "subject":None,
                "body":None
            }

        estimate_message_2666245_dict = {
                "id":2666245,
                "sent_by":"Bob Powell",
                "sent_by_email":"bobpowell@example.com",
                "sent_from":"Bob Powell",
                "sent_from_email":"bobpowell@example.com",
                "send_me_a_copy":False,
                "created_at":"2017-08-25T21:31:55Z",
                "updated_at":"2017-08-25T21:31:55Z",
                "recipients":[],
                "event_type":"decline",
                "subject":None,
                "body":None
            }

        estimate_message_2666246_dict = {
                "id":2666246,
                "sent_by":"Bob Powell",
                "sent_by_email":"bobpowell@example.com",
                "sent_from":"Bob Powell",
                "sent_from_email":"bobpowell@example.com",
                "send_me_a_copy":False,
                "created_at":"2017-08-25T21:31:55Z",
                "updated_at":"2017-08-25T21:31:55Z",
                "recipients":[],
                "event_type":"re-open",
                "subject":None,
                "body":None
            }

        estimate_messages_dict = {
        "estimate_messages":[estimate_message_2666236_dict],
            "per_page":100,
            "total_pages":1,
            "total_entries":1,
            "next_page":None,
            "previous_page":None,
            "page":1,
            "links":{
                    "first":"https://api.harvestapp.com/v2/estimates/1439818/messages?page=1&per_page=100",
                    "next":None,
                    "previous":None,
                    "last":"https://api.harvestapp.com/v2/estimates/1439818/messages?page=1&per_page=100"
                }
        }

        # estimate_messages
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/estimates/1439818/messages?page=1&per_page=100",
                body=json.dumps(estimate_messages_dict),
                status=200
            )
        estimate_messages = from_dict(data_class=EstimateMessages, data=estimate_messages_dict)
        requested_estimate_messages = self.harvest.estimate_messages(estimate_id= 1439818)
        self.assertEqual(requested_estimate_messages, estimate_messages)

        # estimate_message
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/estimates/1439818/messages",
                body=json.dumps(estimate_message_2666240_dict),
                status=200
            )
        new_estimate_message = from_dict(data_class=EstimateMessage, data=estimate_message_2666240_dict)
        requested_new_estimate_message = self.harvest.create_estimate_message(estimate_id= 1439818, recipients= [{"name" : "Richard Roe", "email" : "richardroe@example.com"}], subject= "Estimate #1001", body= "Here is our estimate.", send_me_a_copy= True)
        self.assertEqual(requested_new_estimate_message, new_estimate_message)

        # mark estimate as sent
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/estimates/1439818/messages",
                body=json.dumps(estimate_message_2666241_dict),
                status=201
            )
        mark_draft_estimate = from_dict(data_class=EstimateMessage, data=estimate_message_2666241_dict)
        requested_mark_draft_estimate = self.harvest.mark_draft_estimate(estimate_id= 1439818, event_type= "send")
        self.assertEqual(requested_mark_draft_estimate, mark_draft_estimate)

        # mark estimate as accepted
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/estimates/1439818/messages",
                body=json.dumps(estimate_message_2666244_dict),
                status=201
            )
        mark_draft_estimate = from_dict(data_class=EstimateMessage, data=estimate_message_2666244_dict)
        requested_mark_draft_estimate = self.harvest.mark_draft_estimate(estimate_id= 1439818, event_type= "accept")
        self.assertEqual(requested_mark_draft_estimate, mark_draft_estimate)

        # mark estimate as declined
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/estimates/1439818/messages",
                body=json.dumps(estimate_message_2666245_dict),
                status=201
            )
        mark_draft_estimate = from_dict(data_class=EstimateMessage, data=estimate_message_2666245_dict)
        requested_mark_draft_estimate = self.harvest.mark_draft_estimate(estimate_id= 1439818, event_type= "decline")
        self.assertEqual(requested_mark_draft_estimate, mark_draft_estimate)

        # mark estimate as re-opened
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/estimates/1439818/messages",
                body=json.dumps(estimate_message_2666246_dict),
                status=201
            )
        mark_draft_estimate = from_dict(data_class=EstimateMessage, data=estimate_message_2666246_dict)
        requested_mark_draft_estimate = self.harvest.mark_draft_estimate(estimate_id= 1439818, event_type= "re-open")
        self.assertEqual(requested_mark_draft_estimate, mark_draft_estimate)

        httpretty.reset()


    def test_estimates(self):
        estimate_1439818_dict = {
                "id":1439818,
                "client_key":"13dc088aa7d51ec687f186b146730c3c75dc7423",
                "number":"1001",
                "purchase_order":"5678",
                "amount":9630.0,
                "tax":5.0,
                "tax_amount":450.0,
                "tax2":2.0,
                "tax2_amount":180.0,
                "discount":10.0,
                "discount_amount":1000.0,
                "subject":"Online Store - Phase 2",
                "notes":"Some notes about the estimate",
                "state":"sent",
                "issue_date":"2017-06-01",
                "sent_at":"2017-06-27T16:11:33Z",
                "created_at":"2017-06-27T16:11:24Z",
                "updated_at":"2017-06-27T16:13:56Z",
                "accepted_at":None,
                "declined_at":None,
                "currency":"USD",
                "client":{
                    "id":5735776,
                    "name":"123 Industries"
                    },
                "creator":{
                        "id":1782884,
                        "name":"Bob Powell"
                    },
                "line_items":[
                        {
                            "id":53334195,
                            "kind":"Service",
                            "description":"Phase 2 of the Online Store",
                            "quantity":100.00, # TODO: this is supposed to be an int. Something isn't casting int to float.
                            "unit_price":100.00, # TODO: this is supposed to be an int. Something isn't casting int to float.
                            "amount":10000.00, # TODO: this is supposed to be an int. Something isn't casting int to float.
                            "taxed":True,
                            "taxed2":True
                        }
                    ]
            }

        estimate_1439814_dict = {
                "id":1439814,
                "client_key":"a5ffaeb30c55776270fcd3992b70332d769f97e7",
                "number":"1000",
                "purchase_order":"1234",
                "amount":21000.0,
                "tax":5.0,
                "tax_amount":1000.0,
                "tax2":None,
                "tax2_amount":0.0,
                "discount":None,
                "discount_amount":0.0,
                "subject":"Online Store - Phase 1",
                "notes":"Some notes about the estimate",
                "state":"accepted",
                "issue_date":"2017-01-01",
                "sent_at":"2017-06-27T16:10:30Z",
                "created_at":"2017-06-27T16:09:33Z",
                "updated_at":"2017-06-27T16:12:00Z",
                "accepted_at":"2017-06-27T16:10:32Z",
                "declined_at":None,
                "currency":"USD",
                "client":{
                        "id":5735776,
                        "name":"123 Industries"
                    },
                "creator":{
                        "id":1782884,
                        "name":"Bob Powell"
                    },
                "line_items":[
                    {
                        "id":57531966,
                        "kind":"Service",
                        "description":"Phase 1 of the Online Store",
                        "quantity":1.00, # TODO: this is supposed to be an int. Something isn't casting int to float.
                        "unit_price":20000.00, # TODO: this is supposed to be an int. Something isn't casting int to float.
                        "amount":20000.00, # TODO: this is supposed to be an int. Something isn't casting int to float.
                        "taxed":True,
                        "taxed2":False
                    }
                ]
            }

        estimate_1439827_dict = {
                "id":1439827,
                "client_key":"ddd4504a68fb7339138d0c2ea89ba05a3cf12aa8",
                "number":"1002",
                "purchase_order":None,
                "amount":5000.0,
                "tax":None,
                "tax_amount":0.0,
                "tax2":None,
                "tax2_amount":0.0,
                "discount":None,
                "discount_amount":0.0,
                "subject":"Project Quote",
                "notes":None,
                "state":"draft",
                "issue_date":None,
                "sent_at":None,
                "created_at":"2017-06-27T16:16:24Z",
                "updated_at":"2017-06-27T16:16:24Z",
                "accepted_at":None,
                "declined_at":None,
                "currency":"USD",
                "client":{
                        "id":5735774,
                        "name":"ABC Corp"
                    },
                "creator":{
                        "id":1782884,
                        "name":"Bob Powell"
                    },
                "line_items":[
                        {
                            "id":53339199,
                            "kind":"Service",
                            "description":"Project Description",
                            "quantity":1.0,
                            "unit_price":5000.0,
                            "amount":5000.0,
                            "taxed":False,
                            "taxed2":False
                        }
                    ]
            }

        estimates_dict = {
                "estimates":[estimate_1439818_dict, estimate_1439814_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":2,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/estimates?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/estimates?page=1&per_page=100"
                    }
            }

        # estimates
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/estimates?page=1&per_page=100",
                body=json.dumps(estimates_dict),
                status=200
            )
        estimates = from_dict(data_class=Estimates, data=estimates_dict)
        requested_estimates = self.harvest.estimates()
        self.assertEqual(requested_estimates, estimates)

        # get_estimte
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/estimates/1439818",
                body=json.dumps(estimate_1439818_dict),
                status=200
            )
        estimate = from_dict(data_class=Estimate, data=estimate_1439818_dict)
        requested_estimate = self.harvest.get_estimte(estimate_id= 1439818)
        self.assertEqual(requested_estimate, estimate)

        # create_estimate
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/estimates",
                body=json.dumps(estimate_1439827_dict),
                status=201
            )
        new_estimate = from_dict(data_class=Estimate, data=estimate_1439827_dict)
        requested_new_estimate = self.harvest.create_estimate(client_id= 5735774, subject= "ABC Project Quote", line_items= [{"kind" : "Service", "description" : "ABC Project Quote", "unit_price" : 5000.0}])
        self.assertEqual(requested_new_estimate, new_estimate)

        # update_estimate
        estimate_1439827_dict["purchase_order"] = "2345"
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/estimates/1439827",
                body=json.dumps(estimate_1439827_dict),
                status=200
            )
        new_estimate = from_dict(data_class=Estimate, data=estimate_1439827_dict)
        requested_new_estimate = self.harvest.update_estimate(estimate_id= 1439827, purchase_order= "2345")
        self.assertEqual(requested_new_estimate, new_estimate)

        # create_estimate_line_item
        estimate_1439827_dict["line_items"].append(
                {
                    "id":53339200,
                    "kind":"Service",
                    "description":"Another Project",
                    "quantity":1.0,
                    "unit_price":1000.0,
                    "amount":1000.0,
                    "taxed":False,
                    "taxed2":False
                }
            )
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/estimates/1439827",
                body=json.dumps(estimate_1439827_dict),
                status=200
            )
        new_estimate_line_item = from_dict(data_class=Estimate, data=estimate_1439827_dict)
        requested_new_estimate_line_item = self.harvest.create_estimate_line_item(estimate_id= 1439827, line_items= [{"kind" : "Service", "description" : "Another Project", "unit_price" : 1000.0}])
        self.assertEqual(requested_new_estimate_line_item, new_estimate_line_item)

        # delete_estimate_line_items
        del(estimate_1439827_dict["line_items"][0])
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/estimates/1439827",
                body=json.dumps(estimate_1439827_dict),
                status=200
            )
        new_estimate_line_item = from_dict(data_class=Estimate, data=estimate_1439827_dict)
        requested_new_estimate_line_item = self.harvest.create_estimate_line_item(estimate_id= 1439827, line_items= [{"id" : 53339199, "_destroy" : True}])
        self.assertEqual(requested_new_estimate_line_item, new_estimate_line_item)

        # delete_estimate
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/estimates/1439827",
                status=200
            )
        requested_deleted_estimate = self.harvest.delete_estimate(estimate_id= 1439827)
        self.assertEqual(requested_deleted_estimate, None)

        httpretty.reset()


    def test_estimate_item_categories(self):
        estimate_item_category_1378704_dict = {
                "id":1378704,
                "name":"Product",
                "created_at":"2017-06-26T20:41:00Z",
                "updated_at":"2017-06-26T20:41:00Z"
            }

        estimate_item_category_1378703_dict = {
                "id":1378703,
                "name":"Service",
                "created_at":"2017-06-26T20:41:00Z",
                "updated_at":"2017-06-26T20:41:00Z"
            }

        estimate_item_category_1379244_dict = {
                "id":1379244,
                "name":"Hosting",
                "created_at":"2017-06-27T16:06:35Z",
                "updated_at":"2017-06-27T16:06:35Z"
            }

        estimate_item_categories_dict = {
                "estimate_item_categories":[estimate_item_category_1378704_dict, estimate_item_category_1378703_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":2,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/estimate_item_categories?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/estimate_item_categories?page=1&per_page=100"
                    }
            }

        # estimate_item_categories
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/estimate_item_categories?page=1&per_page=100",
                body=json.dumps(estimate_item_categories_dict),
                status=200
            )
        estimate_item_categories = from_dict(data_class=EstimateItemCategories, data=estimate_item_categories_dict)
        requested_estimate_item_categories = self.harvest.estimate_item_categories()
        self.assertEqual(requested_estimate_item_categories, estimate_item_categories)

        # get_estimate_item_category
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/estimate_item_categories/1378704",
                body=json.dumps(estimate_item_category_1378704_dict),
                status=200
            )
        estimate_item_category = from_dict(data_class=EstimateItemCategory, data=estimate_item_category_1378704_dict)
        requested_estimate_item_category = self.harvest.get_estimate_item_category(estimate_item_category_id=1378704)
        self.assertEqual(requested_estimate_item_category, estimate_item_category)

        # create_estimate_item_category
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/estimate_item_categories",
                body=json.dumps(estimate_item_category_1379244_dict),
                status=201
            )
        new_estimate_item_category = from_dict(data_class=EstimateItemCategory, data=estimate_item_category_1379244_dict)
        requested_new_estimate_item_category = self.harvest.create_estimate_item_category(name= "Hosting")
        self.assertEqual(requested_new_estimate_item_category, new_estimate_item_category)

        # update_estimate_item_category
        estimate_item_category_1379244_dict["name"] = "Transportation"
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/estimate_item_categories/1379244",
                body=json.dumps(estimate_item_category_1379244_dict),
                status=200
            )
        updated_estimate_item_category = from_dict(data_class=EstimateItemCategory, data=estimate_item_category_1379244_dict)
        requested_updated_estimate_item_category = self.harvest.update_estimate_item_category(estimate_item_category_id= 1379244, name= "Transportation")
        self.assertEqual(requested_updated_estimate_item_category, updated_estimate_item_category)

        # delete_estimate_item_category
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/estimate_item_categories/1379244",
                status=200
            )
        requested_deleted_estimate_item_category = self.harvest.delete_estimate_item_category(estimate_item_id= 1379244)
        self.assertEqual(requested_deleted_estimate_item_category, None)

        httpretty.reset()


if __name__ == '__main__':
    unittest.main()
