
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

class TestExpenses(unittest.TestCase):

    def setUp(self):
        personal_access_token = PersonalAccessToken('ACCOUNT_NUMBER', 'PERSONAL_ACCESS_TOKEN')
        self.harvest = harvest.Harvest('https://api.harvestapp.com/api/v2', personal_access_token)
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*") # There's a bug in httpretty ATM.
        httpretty.enable()

    def teardown(self):
        httpretty.reset()
        httpretty.disable()


    def test_expenses(self):
        expense_15296442_dict = {
                "id":15296442,
                "notes":"Lunch with client",
                "total_cost":33.35,
                "units":1.0,
                "is_closed":False,
                "is_locked":True,
                "is_billed":True,
                "locked_reason":"Expense is invoiced.",
                "spent_date":"2017-03-03",
                "created_at":"2017-06-27T15:09:54Z",
                "updated_at":"2017-06-27T16:47:14Z",
                "billable":True,
                "receipt":{
                        "url":"https://{ACCOUNT_SUBDOMAIN}.harvestapp.com/expenses/15296442/receipt",
                        "file_name":"lunch_receipt.gif",
                        "file_size":39410,
                        "content_type":"image/gif"
                    },
                "user":{
                        "id":1782959,
                        "name":"Kim Allen"
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
                "project":{
                        "id":14307913,
                        "name":"Marketing Website",
                        "code":"MW"
                    },
                "expense_category":{
                        "id":4195926,
                        "name":"Meals",
                        "unit_price":None,
                        "unit_name":None
                    },
                "client":{
                        "id":5735774,
                        "name":"ABC Corp",
                        "currency":"USD"
                    },
                "invoice":{
                        "id":13150403,
                        "number":"1001"
                    }
            }

        expense_15296423_dict = {
                "id":15296423,
                "notes":"Hotel stay for meeting",
                "total_cost":100.0,
                "units":1.0,
                "is_closed":True,
                "is_locked":True,
                "is_billed":False,
                "locked_reason":"The project is locked for this time period.",
                "spent_date":"2017-03-01",
                "created_at":"2017-06-27T15:09:17Z",
                "updated_at":"2017-06-27T16:47:14Z",
                "billable":True,
                "receipt":None,
                "user":{
                        "id":1782959,
                        "name":"Kim Allen"
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
                "project":{
                        "id":14308069,
                        "name":"Online Store - Phase 1",
                        "code":"OS1"
                    },
                "expense_category":{
                        "id":4197501,
                        "name":"Lodging",
                        "unit_price":None,
                        "unit_name":None
                    },
                "client":{
                        "id":5735776,
                        "name":"123 Industries",
                        "currency":"EUR"
                    },
                "invoice":None
            }

        expense_15297032_dict = {
                "id":15297032,
                "notes":None,
                "total_cost":13.59,
                "units":1.0,
                "is_closed":False,
                "is_locked":False,
                "is_billed":False,
                "locked_reason":None,
                "spent_date":"2017-03-01",
                "created_at":"2017-06-27T15:42:27Z",
                "updated_at":"2017-06-27T15:42:27Z",
                "billable":True,
                "receipt":None,
                "user":{
                        "id":1782959,
                        "name":"Kim Allen"
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
                "project":{
                        "id":14308069,
                        "name":"Online Store - Phase 1",
                        "code":"OS1"
                    },
                "expense_category":{
                        "id":4195926,
                        "name":"Meals",
                        "unit_price":None,
                        "unit_name":None
                    },
                "client":{
                    "id":5735776,
                        "name":"123 Industries",
                        "currency":"EUR"
                    },
                "invoice":None
            }

        expenses_dict = {
        "expenses":[expense_15296442_dict, expense_15296423_dict],
        "per_page":100,
        "total_pages":1,
        "total_entries":2,
        "next_page":None,
        "previous_page":None,
        "page":1,
        "links":{
                "first":"https://api.harvestapp.com/v2/expenses?page=1&per_page=100",
                "next":None,
                "previous":None,
                "last":"https://api.harvestapp.com/v2/expenses?page=1&per_page=100"
            }
        }

        # expenses
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/expenses?page=1&per_page=100",
                body=json.dumps(expenses_dict),
                status=200
            )
        expenses = from_dict(data_class=Expenses, data=expenses_dict)
        requested_expenses = self.harvest.expenses()
        self.assertEqual(requested_expenses, expenses)

        # get_expense
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/expenses/15296442",
                body=json.dumps(expense_15296442_dict),
                status=200
            )
        expense = from_dict(data_class=Expense, data=expense_15296442_dict)
        requested_expense = self.harvest.get_expense(expense_id=15296442)
        self.assertEqual(requested_expense, expense)

        # create_expense
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/expenses",
                body=json.dumps(expense_15297032_dict),
                status=201
            )
        new_expense = from_dict(data_class=Expense, data=expense_15297032_dict)
        requested_new_expense = self.harvest.create_expense(project_id= 14308069, expense_category_id= 4195926, spent_date= "2017-03-01", user_id= 1782959, total_cost= 13.59)
        self.assertEqual(requested_new_expense, new_expense)

        # update_expense
        receipt = {'file_name':'dinner_receipt.gif', 'content_type': 'image/gif', 'files': {'receipt': ('dinner_receipt.gif', 'open(filename, "rb")', 'image/png', {'Expires': '0'})}, "url": "https://{ACCOUNT_SUBDOMAIN}.harvestapp.com/expenses/15297032/receipt", "file_size": 39410 }
        expense_15297032_dict['notes'] = "Dinner"
        expense_15297032_dict['receipt'] = receipt
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/expenses/15297032",
                body=json.dumps(expense_15297032_dict),
                status=200
            )
        updated_expense = from_dict(data_class=Expense, data=expense_15297032_dict)
        requested_updated_expense = self.harvest.update_expense(expense_id= 15297032, notes= "Dinner", receipt= receipt)
        self.assertEqual(requested_updated_expense, updated_expense)

        # delete_expense
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/expenses/15297032",
                status=200
            )
        requested_deleted_expense = self.harvest.delete_expense(expense_id= 15297032)
        self.assertEqual(requested_deleted_expense, None)

        httpretty.reset()


    def test_expense_categories(self):
        expense_category_4197501_dict = {
                "id":4197501,
                "name":"Lodging",
                "unit_name":None,
                "unit_price":None,
                "is_active":True,
                "created_at":"2017-06-27T15:01:32Z",
                "updated_at":"2017-06-27T15:01:32Z"
            }

        expense_category_4195930_dict = {
                "id":4195930,
                "name":"Mileage",
                "unit_name":"mile",
                "unit_price":0.535,
                "is_active":True,
                "created_at":"2017-06-26T20:41:00Z",
                "updated_at":"2017-06-26T20:41:00Z"
            }

        expense_category_4195928_dict = {
                "id":4195928,
                "name":"Transportation",
                "unit_name":None,
                "unit_price":None,
                "is_active":True,
                "created_at":"2017-06-26T20:41:00Z",
                "updated_at":"2017-06-26T20:41:00Z"
            }

        expense_category_4195926_dict = {
                "id":4195926,
                "name":"Meals",
                "unit_name":None,
                "unit_price":None,
                "is_active":True,
                "created_at":"2017-06-26T20:41:00Z",
                "updated_at":"2017-06-26T20:41:00Z"
            }

        expense_category_4197514_dict = {
                "id":4197514,
                "name":"Other",
                "unit_name":None,
                "unit_price":None,
                "is_active":True,
                "created_at":"2017-06-27T15:04:23Z",
                "updated_at":"2017-06-27T15:04:23Z"
            }

        expense_categories_dict = {
                "expense_categories":[expense_category_4197501_dict, expense_category_4195930_dict, expense_category_4195928_dict, expense_category_4195926_dict],
                "per_page":100,
                "total_pages":1,
                "total_entries":4,
                "next_page":None,
                "previous_page":None,
                "page":1,
                "links":{
                        "first":"https://api.harvestapp.com/v2/expense_categories?page=1&per_page=100",
                        "next":None,
                        "previous":None,
                        "last":"https://api.harvestapp.com/v2/expense_categories?page=1&per_page=100"
                    }
            }

        # expense_categories
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/expense_categories?page=1&per_page=100",
                body=json.dumps(expense_categories_dict),
                status=200
            )
        expense_categories = from_dict(data_class=ExpenseCategories, data=expense_categories_dict)
        requested_expense_categories = self.harvest.expense_categories()
        self.assertEqual(requested_expense_categories, expense_categories)

        # get_expense_category
        httpretty.register_uri(httpretty.GET,
                "https://api.harvestapp.com/api/v2/expense_categories/4197501",
                body=json.dumps(expense_category_4197501_dict),
                status=200
            )
        expense_category = from_dict(data_class=ExpenseCategory, data=expense_category_4197501_dict)
        requested_expense_category = self.harvest.get_expense_category(expense_category_id= 4197501)
        self.assertEqual(requested_expense_category, expense_category)

        # create_expense_category
        httpretty.register_uri(httpretty.POST,
                "https://api.harvestapp.com/api/v2/expense_categories",
                body=json.dumps(expense_category_4197514_dict),
                status=201
            )
        new_expense_category = from_dict(data_class=ExpenseCategory, data=expense_category_4197514_dict)
        requested_new_expense_category = self.harvest.create_expense_category(name= "Other")
        self.assertEqual(requested_new_expense_category, new_expense_category)

        # update_expense_category
        httpretty.register_uri(httpretty.PATCH,
                "https://api.harvestapp.com/api/v2/expense_categories/4197514",
                body=json.dumps(expense_category_4197514_dict),
                status=201
            )
        updated_expense_category = from_dict(data_class=ExpenseCategory, data=expense_category_4197514_dict)
        requested_updated_expense_category = self.harvest.update_expense_category(expense_category_id= 4197514)
        self.assertEqual(requested_updated_expense_category, updated_expense_category)

        # delete_expense_category
        httpretty.register_uri(httpretty.DELETE,
                "https://api.harvestapp.com/api/v2/expense_categories/4197514",
                status=200
            )
        requested_deleted_expense_category = self.harvest.delete_expense_category(expense_category_id= 4197514)
        self.assertEqual(requested_deleted_expense_category, None)

        httpretty.reset()


if __name__ == '__main__':
    unittest.main()
