from app.tests.base import BaseTestCase
from app.main.database.models.auth import BlacklistedTokens
from flask import json
import base64

def register_user(self):
    new_user = dict(email=self.eml, password=self.pwd)
    return self.make_test_request(
        'api/user/create',
        'post', 
        data = new_user)

def token_request(self, uri, method):
    auth_string = 'Bearer ' + self.token
    return self.make_test_request(
        uri,
        method,
        custom_headers={'Authorization': auth_string}
    )

def login_user(self):
    auth_string = bytes(self.eml + ':' + self.pwd, 'utf-8')
    req_auth = 'Basic ' + base64.b64encode(auth_string).decode()
    headers = {'Authorization': req_auth}
    return self.make_test_request(
        'api/auth/login',
        'get',
        custom_headers=headers
    )

class TestUserController(BaseTestCase):
    eml = 'unit_testing@yomama.com'
    pwd = '123456'
    token = ''

    def test_user_registration(self):
        with self.client:
            res = register_user(self)
            data = res.json           
            self.assertTrue(data['message'] == 'User Created')
            self.assertEqual(res.status_code, 201)

    def test_user_login_unregistered(self):
        with self.client:
            res = login_user(self)
            data = res.json 
            self.assertTrue(data['message'] == 'Authentication Failed')
            self.assert401(res)

    def test_user_activate(self):
        with self.client:
            reg_res = register_user(self)
            reg_data = reg_res.json           
            self.assertTrue(reg_data['message'] == 'User Created')
            self.assertEqual(reg_res.status_code, 201)
            # login with new user to get token
            login_res = login_user(self)
            login_data = login_res.json 
            self.assertTrue(login_data['message'] == 'Welcome back')
            self.assertTrue(login_data['data'])
            self.assertTrue(login_data['data']['token'])
            self.assertTrue(login_data['data']['id'])
            self.assertTrue(login_data['data']['role'])
            self.assert200(login_res)
            self.token = login_data['data']['token']
            # fail auth prior to activation
            pre_act_res = token_request(self, 'api/auth/test', 'get')
            pre_act_data = pre_act_res.json
            self.assertTrue(pre_act_data['message'])
            self.assert401(pre_act_res)
            # activate user with auth token
            act_res = token_request(self, 'api/user/activate', 'put')
            act_data = act_res.json
            self.assertTrue(act_data['message'] == 'User Activated')
            self.assert200(act_res)
            # should pass auth test now
            post_act_res = token_request(self, 'api/auth/test', 'get')
            post_act_data = post_act_res.json
            self.assertTrue(post_act_data['message'])
            self.assertTrue(post_act_data['role'])
            self.assertTrue(post_act_data['role'] == login_data['data']['role'])
            self.assert200(post_act_res)
            # now log out (blacklist token)
            logout_res = token_request(self, 'api/auth/logout', 'get')
            logout_data = logout_res.json
            bt = BlacklistedTokens.objects(token=self.token).first()
            self.assertIsNotNone(bt)
            self.assertTrue(logout_data['message'] == 'logged out')
            self.assert200(logout_res)
            # should fail auth test
            post_logout_res = token_request(self, 'api/auth/test', 'get')
            post_logout_data = post_logout_res.json
            self.assert401(post_logout_res)
            self.assertEqual(post_logout_data['message'], 'Authentication Failed')
        

if __name__ == '__main__':
    unittest.main()