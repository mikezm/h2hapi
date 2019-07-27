from app.tests.base import BaseTestCase
from app.main.services import token_service
from app.main.dynamodb import tokens
from boto3.dynamodb.conditions import Key
from flask import json
from bson.objectid import ObjectId

class TestTokenService(BaseTestCase):
    eml = 'test@unit.com'
    pwd = '1234abcdA'
    user_id = '5d2b543e5138fc3350939144'

    def test_extract_token(self):
        _, token = token_service.encode_token(user_id=self.user_id)
        bearer_string = "bearer %s" % token
        token_string = "token %s" % token
        broken_string = "key %s " % token
        broken_two_string = " token %s " % token
        broken_three_string = "token "
        test_token = token_service.extract_token(token_string)
        test_bearer = token_service.extract_token(bearer_string)
        broken_test = token_service.extract_token(broken_string)
        broken_two_test = token_service.extract_token(broken_two_string)
        broken_three_test = token_service.extract_token(broken_three_string)
        self.assertEqual(token, test_token)
        self.assertEqual(token, test_bearer)
        self.assertFalse(broken_test)
        self.assertFalse(broken_two_test)
        self.assertFalse(broken_three_test)

    def test_encode_token(self):
        token_generated, _ = token_service.encode_token(user_id=self.user_id)
        self.assertTrue(token_generated)

    def test_decode_token(self):
        _, token = token_service.encode_token(user_id=self.user_id)
        token_decoded, decoded = token_service.decode_token(token)
        self.assertTrue(token_decoded)
        self.assertEqual(self.user_id, decoded['sub'])

    def test_blacklist_token(self):
        _, my_token = token_service.encode_token(user_id=self.user_id)
        logged_out = token_service.blacklist_token(my_token)
        res = tokens.query(Select='SPECIFIC_ATTRIBUTES', ProjectionExpression='auth_token', KeyConditionExpression=Key('auth_token').eq(my_token))
        bt = res['Items'][0]
        self.assertTrue(logged_out)
        self.assertIsNotNone(bt)
        self.assertIsNotNone(bt['auth_token'])
        self.assertEqual(bt['auth_token'], my_token)

    def test_is_token_blacklisted(self):
        _, my_token = token_service.encode_token(user_id=self.user_id)
        _, bl_token = token_service.encode_token(user_id=str(ObjectId()))
        token_service.blacklist_token(bl_token)
        test_clean = token_service.is_token_blacklisted(my_token)
        test_bl = token_service.is_token_blacklisted(bl_token)
        self.assertFalse(test_clean)
        self.assertTrue(test_bl)




