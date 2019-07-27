from flask_testing import TestCase
from app.main.dynamodb import create_db_tables, drop_db_tables
from app import create_app as create_test_app
from flask import json

class BaseTestCase(TestCase):
    
    def create_app(self):
        app = create_test_app('test')
        return app

    def setUp(self):
        create_db_tables()

    def tearDown(self):
        drop_db_tables()

    def make_test_request(self, uri, method, data=None, custom_headers=None):
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        if custom_headers:
            for header_name in custom_headers:
                headers[header_name] = custom_headers[header_name]
        if data:
            return self.client.open(
                uri,
                method=method,
                data=json.dumps(data),
                headers=headers
            )
        # for get requests (e.g. no data)
        return self.client.open(
            uri,
            method=method,
            headers=headers
        )