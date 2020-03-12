
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

class TestInvoices(unittest.TestCase):

    def setUp(self):
        personal_access_token = PersonalAccessToken('ACCOUNT_NUMBER', 'PERSONAL_ACCESS_TOKEN')
        self.harvest = harvest.Harvest('https://api.harvestapp.com/api/v2', personal_access_token)
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*") # There's a bug in httpretty ATM.
        httpretty.enable()

    def teardown(self):
        httpretty.reset()
        httpretty.disable()

    def test_invoice_messages(self):
        invoice_message_27835209_dict = {
                "id":27835209,
                "sent_by":"Bob Powell",
                "sent_by_email":"bobpowell@example.com",
                "sent_from":"Bob Powell",
                "sent_from_email":"bobpowell@example.com",
                "include_link_to_client_invoice":False,
                "send_me_a_copy":False,
                "thank_you":False,
                "reminder":False,
                "send_reminder_on":None,
                "created_at":"2017-08-23T22:15:06Z",
                "updated_at":"2017-08-23T22:15:06Z",
                "attach_pdf":True,
                "event_type":None,
                "recipients":[
                    {
                        "name":"Richard Roe",
                        "email":"richardroe@example.com"
                    }
                ],
                "subject":"Past due invoice reminder: #1001 from API Examples",
                "body":"Dear Customer,\r\n\r\nThis is a friendly reminder to let you know that Invoice 1001 is 144 days past due. If you have already sent the payment, please disregard this message. If not, we would appreciate your prompt attention to this matter.\r\n\r\nThank you for your business.\r\n\r\nCheers,\r\nAPI Examples"
            }

        invoice_message_27835207_dict = {
                "id":27835207,
                "sent_by":"Bob Powell",
                "sent_by_email":"bobpowell@example.com",
                "sent_from":"Bob Powell",
                "sent_from_email":"bobpowell@example.com",
                "include_link_to_client_invoice":False,
                "send_me_a_copy":True,
                "thank_you":False,
                "reminder":False,
                "send_reminder_on":None,
                "created_at":"2017-08-23T22:14:49Z",
                "updated_at":"2017-08-23T22:14:49Z",
                "attach_pdf":True,
                "event_type":None,
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
                "subject":"Invoice #1001 from API Examples",
                "body":"---------------------------------------------\r\nInvoice Summary\r\n---------------------------------------------\r\nInvoice ID: 1001\r\nIssue Date: 04/01/2017\r\nClient: 123 Industries\r\nP.O. Number: \r\nAmount: €288.90\r\nDue: 04/01/2017 (upon receipt)\r\n\r\nThe detailed invoice is attached as a PDF.\r\n\r\nThank you!\r\n---------------------------------------------"
            }

        invoice_message_27835324_dict = {
                "id":27835324,
                "sent_by":"Bob Powell",
                "sent_by_email":"bobpowell@example.com",
                "sent_from":"Bob Powell",
                "sent_from_email":"bobpowell@example.com",
                "include_link_to_client_invoice":False,
                "send_me_a_copy":True,
                "thank_you":False,
                "reminder":False,
                "send_reminder_on":None,
                "created_at":"2017-08-23T22:25:59Z",
                "updated_at":"2017-08-23T22:25:59Z",
                "attach_pdf":True,
                "event_type":None,
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
                "subject":"Invoice #1001",
                "body":"The invoice is attached below."
            }

        invoice_message_27835325_dict = {
                "id":27835325,
                "sent_by":"Bob Powell",
                "sent_by_email":"bobpowell@example.com",
                "sent_from":"Bob Powell",
                "sent_from_email":"bobpowell@example.com",
                "include_link_to_client_invoice":False,
                "send_me_a_copy":False,
                "thank_you":False,
                "reminder":False,
                "send_reminder_on":None,
                "created_at":"2017-08-23T22:25:59Z",
                "updated_at":"2017-08-23T22:25:59Z",
                "attach_pdf":False,
                "event_type":"send",
                "recipients":[],
                "subject":None,
                "body":None
            }

        invoice_message_27835326_dict = {
                "id":27835326,
                "sent_by":"Bob Powell",
                "sent_by_email":"bobpowell@example.com",
                "sent_from":"Bob Powell",
                "sent_from_email":"bobpowell@example.com",
                "include_link_to_client_invoice":False,
                "send_me_a_copy":False,
                "thank_you":False,
                "reminder":False,
                "send_reminder_on":None,
                "created_at":"2017-08-23T22:25:59Z",
                "updated_at":"2017-08-23T22:25:59Z",
                "attach_pdf":False,
                "event_type":"close",
                "recipients":[],
                "subject":None,
                "body":None
            }

        invoice_message_27835327_dict = {
                "id":27835327,
                "sent_by":"Bob Powell",
                "sent_by_email":"bobpowell@example.com",
                "sent_from":"Bob Powell",
                "sent_from_email":"bobpowell@example.com",
                "include_link_to_client_invoice":False,
                "send_me_a_copy":False,
                "thank_you":False,
                "reminder":False,
                "send_reminder_on":None,
                "created_at":"2017-08-23T22:25:59Z",
                "updated_at":"2017-08-23T22:25:59Z",
                "attach_pdf":False,
                "event_type":"re-open",
                "recipients":[],
                "subject":None,
                "body":None
            }

        invoice_message_27835328_dict = {
                "id":27835328,
                "sent_by":"Bob Powell",
                "sent_by_email":"bobpowell@example.com",
                "sent_from":"Bob Powell",
                "sent_from_email":"bobpowell@example.com",
                "include_link_to_client_invoice":False,
                "send_me_a_copy":False,
                "thank_you":False,
                "reminder":False,
                "send_reminder_on":None,
                "created_at":"2017-08-23T22:25:59Z",
                "updated_at":"2017-08-23T22:25:59Z",
                "attach_pdf":False,
                "event_type":"draft",
                "recipients":[],
                "subject":None,
                "body":None
            }

        invoice_messages_dict = {
                "invoice_messages":[invoice_message_27835209_dict, invoice_message_27835207_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":2,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                    "first":"https://api.harvestapp.com/api/v2/invoices/13150403/messages?page=1&per_page=100",
                    "next":None,
                    "previous":None,
                    "last":"https://api.harvestapp.com/v2/invoices/13150403/messages?page=1&per_page=100"
                }
            }

        # invoice_messages
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/invoices/13150403/messages?page=1&per_page=100",
                body=json.dumps(invoice_messages_dict),
                status=200
            )
        invoice_messages = from_dict(data_class=InvoiceMessages, data=invoice_messages_dict)
        requested_invoice_messages = self.harvest.invoice_messages(invoice_id= 13150403)
        self.assertEqual(requested_invoice_messages, invoice_messages)

        # create_invoice_message
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/invoices/27835324/messages",
                body=json.dumps(invoice_message_27835324_dict),
                status=201
            )
        created_invoice_message = from_dict(data_class=InvoiceMessage, data=invoice_message_27835324_dict)
        requested_created_invoice_message = self.harvest.create_invoice_message(invoice_id= 27835324, recipients= [{"name":"Richard Roe", "email":"richardroe@example.com"}], subject= "Invoice #1001", body= "The invoice is attached below.", attach_pdf= True, send_me_a_copy= True)
        self.assertEqual(requested_created_invoice_message, created_invoice_message)

        # delete_client
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/invoices/13150403/messages/27835324",
                status=200
            )
        requested_deleted_invoice_message = self.harvest.delete_invoice_message(invoice_id= 13150403, message_id= 27835324)
        self.assertEqual(requested_deleted_invoice_message, None)

        # mark_draft_invoice_as_sent
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/invoices/13150403/messages",
                body=json.dumps(invoice_message_27835325_dict),
                status=201
            )
        sent_invoice_message = from_dict(data_class=InvoiceMessage, data=invoice_message_27835325_dict)
        requested_sent_invoice_message = self.harvest.mark_draft_invoice(invoice_id= 13150403, event_type= "send")
        self.assertEqual(requested_sent_invoice_message, sent_invoice_message)

        # mark_open_invoice_as_closed
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/invoices/13150403/messages",
                body=json.dumps(invoice_message_27835326_dict),
                status=201
            )
        closed_invoice_message = from_dict(data_class=InvoiceMessage, data=invoice_message_27835326_dict)
        requested_closed_invoice_message = self.harvest.mark_draft_invoice(invoice_id= 13150403, event_type= "close")
        self.assertEqual(requested_closed_invoice_message, closed_invoice_message)

        # reopen_closed_invoice
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/invoices/13150403/messages",
                body=json.dumps(invoice_message_27835327_dict),
                status=201
            )
        reopened_invoice_message = from_dict(data_class=InvoiceMessage, data=invoice_message_27835327_dict)
        requested_reopened_invoice_message = self.harvest.mark_draft_invoice(invoice_id= 13150403, event_type= "re-open")
        self.assertEqual(requested_reopened_invoice_message, reopened_invoice_message)

        # mark_open_invoice_as_draft
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/invoices/13150403/messages",
                body=json.dumps(invoice_message_27835328_dict),
                status=201
            )
        draft_invoice_message = from_dict(data_class=InvoiceMessage, data=invoice_message_27835328_dict)
        requested_draft_invoice_message = self.harvest.mark_draft_invoice(invoice_id= 13150403, event_type= "draft")
        self.assertEqual(requested_draft_invoice_message, draft_invoice_message)

        httpretty.reset()


    def test_invoice_payments(self):
        invoice_payment_10112854_dict = {
                "id": 10112854,
                "amount": 10700.00, # TODO: this needs to be an int and have python-harvest cast it. For some reason dcite isn't listening to the cast in the constructor
                "paid_at": "2017-02-21T00:00:00Z",
                "paid_date": "2017-02-21",
                "recorded_by": "Alice Doe",
                "recorded_by_email": "alice@example.com",
                "notes": "Paid via check #4321",
                "transaction_id": None,
                "created_at": "2017-06-27T16:24:57Z",
                "updated_at": "2017-06-27T16:24:57Z",
                "payment_gateway": {
                        "id": 1234,
                        "name": "Linkpoint International"
                    }
            }

        invoice_payment_10336386_dict = {
                "id": 10336386,
                "amount": 1575.86,
                "paid_at": "2017-07-24T13:32:18Z",
                "paid_date": "2017-07-24",
                "recorded_by": "Jane Bar",
                "recorded_by_email": "jane@example.com",
                "notes": "Paid by phone",
                "transaction_id": None,
                "created_at": "2017-07-28T14:42:44Z",
                "updated_at": "2017-07-28T14:42:44Z",
                "payment_gateway": {
                        "id": None,
                        "name": None
                    }
            }

        invoice_payments_dict = {
        "invoice_payments": [invoice_payment_10112854_dict],
        "per_page": 100,
        "total_pages": 1,
        "total_entries": 1,
        "next_page": None,
        "previous_page": None,
        "page": 1,
        "links": {
                "first": "https://api.harvestapp.com/v2/invoices/13150378/payments?page=1&per_page=100",
                "next": None,
                "previous": None,
                "last": "https://api.harvestapp.com/v2/invoices/13150378/payments?page=1&per_page=100"
            }
        }

        # invoice_payments
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/invoices/13150403/payments?page=1&per_page=100",
                body=json.dumps(invoice_payments_dict),
                status=200
            )
        invoice_messages = from_dict(data_class=InvoicePayments, data=invoice_payments_dict)
        requested_invoice_messages = self.harvest.invoice_payments(invoice_id= 13150403)
        self.assertEqual(requested_invoice_messages, invoice_messages)

        # create_invoice_payment
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/invoices/13150378/payments",
                body=json.dumps(invoice_payment_10336386_dict),
                status=200
            )
        created_invoice_payment = from_dict(data_class=InvoicePayment, data=invoice_payment_10336386_dict)
        requested_created_invoice_payment = self.harvest.create_invoice_payment(invoice_id= 13150378, amount= 1575.86, paid_at= "2017-07-24T13:32:18Z", notes= "Paid by phone")
        self.assertEqual(requested_created_invoice_payment, created_invoice_payment)

        # delete_invoice_payment
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/invoices/13150403/payments/10336386",
                status=200
            )
        requested_deleted_invoice_message = self.harvest.delete_invoice_payment(invoice_id= 13150403, payment_id= 10336386)
        self.assertEqual(requested_deleted_invoice_message, None)

        httpretty.reset()


    def test_invoices(self):
        invoice_13150403_dict = {
                "id":13150403,
                "client_key":"21312da13d457947a217da6775477afee8c2eba8",
                "number":"1001",
                "purchase_order":"",
                "amount":288.9,
                "due_amount":288.9,
                "tax":5.0, # TODO: this is supposed to be an int. Something isn't casting int to float.
                "tax_amount":13.5,
                "tax2":2.0, # TODO: this is supposed to be an int. Something isn't casting int to float.
                "tax2_amount":5.4,
                "discount":10.0 , # TODO: this is supposed to be an int. Something isn't casting int to float.
                "discount_amount":30.0, # TODO: this is supposed to be an int. Something isn't casting int to float.
                "subject":"Online Store - Phase 1",
                "notes":"Some notes about the invoice.",
                "state":"open",
                "period_start":"2017-03-01",
                "period_end":"2017-03-01",
                "issue_date":"2017-04-01",
                "due_date":"2017-04-01",
                "payment_term":"upon receipt",
                "sent_at":"2017-08-23T22:25:59Z",
                "paid_at":None,
                "paid_date":None,
                "closed_at":None,
                "created_at":"2017-06-27T16:27:16Z",
                "updated_at":"2017-08-23T22:25:59Z",
                "currency":"EUR",
                "client":{
                        "id":5735776,
                        "name":"123 Industries"
                    },
                "estimate":None,
                "retainer":None,
                "creator":{
                        "id":1782884,
                        "name":"Bob Powell"
                    },
                "line_items":[
                    {
                        "id":53341602,
                        "kind":"Service",
                        "description":"03/01/2017 - Project Management: [9:00am - 11:00am] Planning meetings",
                        "quantity":2.0, # TODO: this is supposed to be an int. Something isn't casting int to float.
                        "unit_price":100.0, # TODO: this is supposed to be an int. Something isn't casting int to float.
                        "amount":200.0, # TODO: this is supposed to be an int. Something isn't casting int to float.
                        "taxed":True,
                        "taxed2":True,
                        "project":{
                                "id":14308069,
                                "name":"Online Store - Phase 1",
                                "code":"OS1"
                            }
                    },
                    {
                    "id":53341603,
                    "kind":"Service",
                    "description":"03/01/2017 - Programming: [1:00pm - 2:00pm] Importing products",
                    "quantity":1.0, # TODO: this is supposed to be an int. Something isn't casting int to float.
                    "unit_price":100.0, # TODO: this is supposed to be an int. Something isn't casting int to float.
                    "amount":100.0, # TODO: this is supposed to be an int. Something isn't casting int to float.
                    "taxed":True,
                    "taxed2":True,
                    "project":{
                            "id":14308069,
                            "name":"Online Store - Phase 1",
                            "code":"OS1"
                        }
                    }
                ]
            }

        invoice_13150378_dict = {
                "id":13150378,
                "client_key":"9e97f4a65c5b83b1fc02f54e5a41c9dc7d458542",
                "number":"1000",
                "purchase_order":"1234",
                "amount":10700.0,
                "due_amount":0.0,
                "tax":5.0,
                "tax_amount":500.0,
                "tax2":2.0,
                "tax2_amount":200.0,
                # "discount":None, # TODO: this is supposed to be a None. Something isn't casting int to float.
                "discount_amount":0.0,
                "subject":"Online Store - Phase 1",
                "notes":"Some notes about the invoice.",
                "state":"paid",
                "period_start":None,
                "period_end":None,
                "issue_date":"2017-02-01",
                "due_date":"2017-03-03",
                "payment_term":"custom",
                "sent_at":"2017-02-01T07:00:00Z",
                "paid_at":"2017-02-21T00:00:00Z",
                "paid_date":"2017-02-21",
                "closed_at":None,
                "created_at":"2017-06-27T16:24:30Z",
                "updated_at":"2017-06-27T16:24:57Z",
                "currency":"USD",
                "client":{
                        "id":5735776,
                        "name":"123 Industries"
                    },
                "estimate":{
                        "id":1439814
                    },
                "retainer":None,
                "creator":{
                        "id":1782884,
                        "name":"Bob Powell"
                    },
                "line_items":[
                    {
                        "id":53341450,
                        "kind":"Service",
                        "description":"50% of Phase 1 of the Online Store",
                        "quantity":100.0,
                        "unit_price":100.0,
                        "amount":10000.0,
                        "taxed":True,
                        "taxed2":True,
                        "project":{
                                "id":14308069,
                                "name":"Online Store - Phase 1",
                                "code":"OS1"
                            }
                    }
                ]
            }

        invoice_13150453_dict = {
                "id":13150453,
                "client_key":"8b86437630b6c260c1bfa289f0154960f83b606d",
                "number":"1002",
                "purchase_order":None,
                "amount":5000.0,
                "due_amount":5000.0,
                "tax":None,
                "tax_amount":0.0,
                "tax2":None,
                "tax2_amount":0.0,
                "discount":None,
                "discount_amount":0.0,
                "subject":"ABC Project Quote",
                "notes":None,
                "state":"draft",
                "period_start":None,
                "period_end":None,
                "issue_date":"2017-06-27",
                "due_date":"2017-07-27",
                "payment_term":"custom",
                "sent_at":None,
                "paid_at":None,
                "paid_date":None,
                "closed_at":None,
                "created_at":"2017-06-27T16:34:24Z",
                "updated_at":"2017-06-27T16:34:24Z",
                "currency":"USD",
                "client":{
                        "id":5735774,
                        "name":"ABC Corp"
                    },
                "estimate":None,
                "retainer":None,
                "creator":{
                        "id":1782884,
                        "name":"Bob Powell"
                    },
                "line_items":[
                    {
                        "id":53341928,
                        "kind":"Service",
                        "description":"ABC Project",
                        "quantity":1.0,
                        "unit_price":5000.0,
                        "amount":5000.0,
                        "taxed":False,
                        "taxed2":False,
                        "project":None
                    }
                ]
            }

        invoice_15340591_dict = {
                "id":15340591,
                "client_key":"16173155e0a01542b8c7f689888cb3eaeda0dc94",
                "number":"1002",
                "purchase_order":"",
                "amount":333.35,
                "due_amount":333.35,
                "tax":None,
                "tax_amount":0.0,
                "tax2":None,
                "tax2_amount":0.0,
                "discount":None,
                "discount_amount":0.0,
                "subject":"ABC Project Quote",
                "notes":"",
                "state":"draft",
                "period_start":"2017-03-01",
                "period_end":"2017-03-31",
                "issue_date":"2018-02-12",
                "due_date":"2018-02-12",
                "payment_term":"upon receipt",
                "sent_at":None,
                "paid_at":None,
                "closed_at":None,
                "created_at":"2018-02-12T21:02:37Z",
                "updated_at":"2018-02-12T21:02:37Z",
                "paid_date":None,
                "currency":"USD",
                "client":{
                        "id":5735774,
                        "name":"ABC Corp"
                    },
                "estimate":None,
                "retainer":None,
                "creator":{
                        "id":1782884,
                        "name":"Bob Powell"
                    },
                "line_items":[
                    {
                        "id":64957723,
                        "kind":"Service",
                        "description":"[MW] Marketing Website: Graphic Design (03/01/2017 - 03/31/2017)",
                        "quantity":2.0,
                        "unit_price":100.0,
                        "amount":200.0,
                        "taxed":False,
                        "taxed2":False,
                        "project":{
                                "id":14307913,
                                "name":"Marketing Website",
                                "code":"MW"
                            }
                    },
                        {
                        "id":64957724,
                        "kind":"Product",
                        "description":"[MW] Marketing Website: Meals ",
                        "quantity":1.0,
                        "unit_price":133.35,
                        "amount":133.35,
                        "taxed":False,
                        "taxed2":False,
                        "project":{
                                "id":14307913,
                                "name":"Marketing Website",
                                "code":"MW"
                            }
                    }
                ]
            }

        invoices_dict = {
                "invoices":[invoice_13150403_dict, invoice_13150378_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":2,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/invoices?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/invoices?page=1&per_page=100"
                    }
            }

        # invoices
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/invoices?page=1&per_page=100",
                body=json.dumps(invoices_dict),
                status=200
            )
        invoices = from_dict(data_class=Invoices, data=invoices_dict)
        requested_invoices = self.harvest.invoices()
        self.assertEqual(requested_invoices, invoices)

        # get_invoice
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/invoices/13150378",
                body=json.dumps(invoice_13150378_dict),
                status=200
            )
        invoice = from_dict(data_class=Invoice, data=invoice_13150378_dict)
        requested_invoice = self.harvest.get_invoice(invoice_id= 13150378)
        self.assertEqual(requested_invoice, invoice)

        # create_invoice
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/invoices",
                body=json.dumps(invoice_15340591_dict),
                status=200
            )
        created_invoice = from_dict(data_class=Invoice, data=invoice_15340591_dict)
        requested_created_invoice = self.harvest.create_invoice(client_id= 5735774, subject= "ABC Project Quote", due_date= "2017-07-27", line_items= [{"kind" : "Service", "description" : "ABC Project", "unit_price" : 5000.0}])
        self.assertEqual(requested_created_invoice, created_invoice)

        # update_invoice
        invoice_13150453_dict['purchase_order'] = "2345"
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/invoices/13150453",
                body=json.dumps(invoice_13150453_dict),
                status=200
            )
        updated_invoice = from_dict(data_class=Invoice, data=invoice_13150453_dict)
        requested_updated_invoice = self.harvest.update_invoice(invoice_id= 13150453, purchase_order="2345")
        self.assertEqual(requested_created_invoice, created_invoice)


        # create_invoice_line_item  invoice_13150453_dict
        # https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/ has an error in the doco...
        invoice_13150453_dict['line_items'].append(
                {
                    "id":53341929,
                    "kind":"Service",
                    "description":"DEF Project",
                    "quantity":1.0,
                    "unit_price":1000.0,
                    "amount":1000.0,
                    "taxed":False,
                    "taxed2":False,
                    "project":None
                }
            )
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/invoices/13150453",
                body=json.dumps(invoice_13150453_dict),
                status=200
            )
        updated_invoice = from_dict(data_class=Invoice, data=invoice_13150453_dict)
        requested_updated_invoice = self.harvest.create_invoice_line_item(invoice_id= 13150453, line_items = [{"kind" : "Service", "description" : "DEF Project"," unit_price" : 1000.0}])
        self.assertEqual(requested_created_invoice, created_invoice)

        # update_invoice_line_item  invoice_13150453_dict
        # https://help.getharvest.com/api-v2/invoices-api/invoices/invoices/ has an error in the doco...
        invoice_13150453_dict['line_items'][1]['description'] = "ABC Project Phase 2"
        invoice_13150453_dict['line_items'][1]['unit_price'] = 500.00
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/invoices/13150453",
                body=json.dumps(invoice_13150453_dict),
                status=200
            )
        updated_invoice = from_dict(data_class=Invoice, data=invoice_13150453_dict)
        requested_updated_invoice = self.harvest.update_invoice_line_item(invoice_id= 13150453, line_item = {"id":53341928,"description":"ABC Project Phase 2","unit_price":5000.0})
        self.assertEqual(requested_created_invoice, created_invoice)

        # delete_invoice_line_items
        del(invoice_13150453_dict['line_items'][1])
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/invoices/13150453",
                body=json.dumps(invoice_13150453_dict),
                status=200
            )
        deleted_invoice_line_items = from_dict(data_class=Invoice, data=invoice_13150453_dict)
        requested_deleted_invoice_line_items = self.harvest.delete_invoice_line_items(invoice_id= 13150453, line_items = [{"id" : 53341928, "_destroy" : True}])
        self.assertEqual(requested_deleted_invoice_line_items, deleted_invoice_line_items)

        # delete_invoice
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/invoices/13150453",
                status=200
            )
        requested_deleted_invoice = self.harvest.delete_invoice(invoice_id= 13150453)
        self.assertEqual(requested_deleted_invoice, None)

        httpretty.reset()


    def test_invoice_item_categories(self):
        invoice_item_category_1466293_dict = {
                "id":1466293,
                "name":"Product",
                "use_as_service":False,
                "use_as_expense":True,
                "created_at":"2017-06-26T20:41:00Z",
                "updated_at":"2017-06-26T20:41:00Z"
            }

        invoice_item_category_1466292_dict = {
                "id":1466292,
                "name":"Service",
                "use_as_service":True,
                "use_as_expense":False,
                "created_at":"2017-06-26T20:41:00Z",
                "updated_at":"2017-06-26T20:41:00Z"
            }

        invoice_item_category_1467098_dict = {
                "id":1467098,
                "name":"Hosting",
                "use_as_service":False,
                "use_as_expense":False,
                "created_at":"2017-06-27T16:20:59Z",
                "updated_at":"2017-06-27T16:20:59Z"
            }

        invoice_item_categories_dict = {
        "invoice_item_categories":[invoice_item_category_1466293_dict, invoice_item_category_1466292_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":2,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/invoice_item_categories?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/invoice_item_categories?page=1&per_page=100"
                    }
            }

        # invoice_categories
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/invoice_item_categories?page=1&per_page=100",
                body=json.dumps(invoice_item_categories_dict),
                status=200
            )
        invoice_item_categories = from_dict(data_class=InvoiceItemCategories, data=invoice_item_categories_dict)
        requested_invoice_item_categories = self.harvest.invoice_item_categories()
        self.assertEqual(invoice_item_categories, invoice_item_categories)

        # get_invoice_item_categories
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/invoice_item_categories/1466293",
                body=json.dumps(invoice_item_category_1466293_dict),
                status=200
            )
        invoice_item_categories = from_dict(data_class=InvoiceItemCategory, data=invoice_item_category_1466293_dict)
        requested_invoice_item_categories = self.harvest.get_invoice_item_category(category_id= 1466293)
        self.assertEqual(requested_invoice_item_categories, invoice_item_categories)

        # create_invoice_item_category
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/invoice_item_categories",
                body=json.dumps(invoice_item_category_1467098_dict),
                status=200
            )
        created_invoice_item_category = from_dict(data_class=InvoiceItemCategory, data=invoice_item_category_1467098_dict)
        requested_created_invoice_item_category = self.harvest.create_invoice_item_category(name= "Hosting")
        self.assertEqual(requested_created_invoice_item_category, created_invoice_item_category)

        # update_invoice_item_category
        invoice_item_category_1467098_dict['name'] = "Expense"
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/invoice_item_categories/1467098",
                body=json.dumps(invoice_item_category_1467098_dict),
                status=200
            )
        update_invoice_item_category = from_dict(data_class=InvoiceItemCategory, data=invoice_item_category_1467098_dict)
        requested_update_invoice_item_category = self.harvest.update_invoice_item_category(category_id= 1467098, name= "Expense")
        self.assertEqual(requested_update_invoice_item_category, update_invoice_item_category)

        # delete_invoice_item_category
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/invoice_item_categories/1467098",
                status=200
            )
        requested_deleted_invoice_item_category = self.harvest.delete_invoice_item_category(invoice_category_id= 1467098)
        self.assertEqual(requested_deleted_invoice_item_category, None)

        httpretty.reset()


if __name__ == '__main__':
    unittest.main()
