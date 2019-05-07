from app.tests.base import BaseTestCase
from flask import json
import base64

base_uri='https://localhost:8888/'

def register_user(self):
    new_user = dict(email=self.eml, password=self.pwd)
    return self.make_test_request(
        'api/user/create',
        'post', 
        data = new_user)
            
def login_user(self):
    auth_string = bytes(self.eml + ':' + self.pwd, 'utf-8')
    req_auth = 'Basic ' + base64.b64encode(auth_string).decode()
    headers = {'Authorization': req_auth}
    return self.make_test_request(
        'api/auth/login',
        'get',
        custom_headers=headers
    )

def activate_user(self):
    auth_string = 'Bearer ' + self.token
    return self.make_test_request(
        'api/user/activate',
        'put',
        custom_headers={'Authorization': auth_string}
    )

def auth_token_test(self):
    auth_string = 'Bearer ' + self.token
    return self.make_test_request(
        'api/auth/test',
        'get',
        custom_headers={'Authorization': auth_string}
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
            self.assertEqual(res.status_code, 401)

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
            self.assertEqual(login_res.status_code, 200)
            self.token = login_data['data']['token']
            # fail auth prior to activation
            pre_act_res = auth_token_test(self)
            pre_act_data = pre_act_res.json
            self.assertTrue(pre_act_data['message'])
            self.assertEqual(pre_act_res.status_code, 401)
            # activate user with auth token
            act_res = activate_user(self)
            act_data = act_res.json
            self.assertTrue(act_data['message'] == 'User Activated')
            self.assertEqual(act_res.status_code, 200)
            # should pass auth test now
            post_act_res = auth_token_test(self)
            post_act_data = post_act_res.json
            self.assertTrue(post_act_data['message'])
            self.assertTrue(post_act_data['role'])
            self.assertTrue(post_act_data['role'] == login_data['data']['role'])
            self.assertEqual(post_act_res.status_code, 200)

if __name__ == '__main__':
    unittest.main()