from app.tests.base import BaseTestCase
from app.main.services import token_service
from flask import json

class TestTokenService(BaseTestCase):
    eml = 'test@unit.com'
    pwd = '1234abcdA'

    def test_extract_token(self):
        _, token = token_service.encode_token(user_id='5d3aa2fc5234fc0fe9093bd8')
        bearer_string = "bearer %s" % token
        token_string = "token %s" % token
        test_token = token_service.extract_token(token_string)
        test_bearer = token_service.extract_token(bearer_string)
        self.assertEqual(token, test_token)
        self.assertEqual(token, test_bearer)



