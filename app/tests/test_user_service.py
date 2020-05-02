from app.tests.base import BaseTestCase
from app.main.services import user_service
from app.main.dynamodb import users
from boto3.dynamodb.conditions import Key, Attr
from bson.objectid import ObjectId

class TestUserService(BaseTestCase):
    eml = 'test@unittest.com'
    pwd = '12345678'

    def test_create_user(self):
        my_id = user_service.create_user(email=self.eml, password=self.pwd)
        fetched_res = users.scan(Select='SPECIFIC_ATTRIBUTES', ProjectionExpression='active, deactivated, id', FilterExpression=Attr('id').eq(my_id['id']))
        fetched_user = fetched_res['Items'][0]
        # user is created. not yet active or deactivated
        self.assertFalse(fetched_user['deactivated'])
        self.assertFalse(fetched_user['active'])
        self.assertEqual(my_id['id'], fetched_user['id'])
        dup_user = user_service.create_user(email=self.eml, password=self.pwd)
        self.assertFalse(dup_user)

    def test_activate_user(self):
        my_id = user_service.create_user(email=self.eml, password=self.pwd)
        test_us = user_service.activate_user(my_id['id'])
        fetched_res = users.scan(Select='SPECIFIC_ATTRIBUTES', ProjectionExpression='active, deactivated', FilterExpression=Attr('id').eq(my_id['id']))
        fetched_user = fetched_res['Items'][0]
        # user is activated now
        self.assertTrue(test_us)
        self.assertTrue(fetched_user['active'])
        self.assertFalse(fetched_user['deactivated'])
        # set user to deactivated
        users.update_item(Key=dict(email=self.eml), UpdateExpression='SET active = :val1, deactivated = :val2', ExpressionAttributeValues={':val1': False, ':val2': True})
        fail_test_us = user_service.activate_user(my_id['id'])
        fetched_fail_res = users.scan(Select='SPECIFIC_ATTRIBUTES', ProjectionExpression='active', FilterExpression=Attr('id').eq(my_id['id']))
        fetched_fail_user = fetched_fail_res['Items'][0]
        # activation should fail now
        self.assertFalse(fail_test_us)
        self.assertFalse(fetched_fail_user['active'])

    def test_deactivate_user(self):
        my_id = user_service.create_user(email=self.eml, password=self.pwd)
        test_us = user_service.deactivate_user(my_id['id'])
        fetched_res = users.scan(Select='SPECIFIC_ATTRIBUTES', ProjectionExpression='active, deactivated', FilterExpression=Attr('id').eq(my_id['id']))
        fetched_user = fetched_res['Items'][0]
        # should inactive and deactivated
        self.assertTrue(test_us)
        self.assertFalse(fetched_user['active'])
        self.assertTrue(fetched_user['deactivated'])

    def test_login_user(self):
        my_id = user_service.create_user(email=self.eml, password=self.pwd)
        test_res = user_service.login_user(email=self.eml, password=self.pwd)
        # should login without issue
        self.assertIn('token', test_res.keys())
        self.assertIn('id', test_res.keys())
        self.assertIn('user_role', test_res.keys())
        self.assertIn('expires_in', test_res.keys())
        self.assertEqual(str(my_id['id']), test_res['id'])
        # test for deactivated account login attempt
        user_service.deactivate_user(my_id['id'])
        fail_res = user_service.login_user(email=self.eml, password=self.pwd)
        # assert failure to login
        self.assertIsNone(fail_res)

    def test_authorize_user(self):
        # set up test users in DB
        admin_id = user_service.create_user(email='admin'+self.eml, password=self.pwd, role='admin')
        editor_id = user_service.create_user(email='editor'+self.eml, password=self.pwd, role='editor')        
        reader_id = user_service.create_user(email='reader'+self.eml, password=self.pwd)        
        inactive_id = user_service.create_user(email='inactive'+self.eml, password=self.pwd)

        admin_activated = user_service.activate_user(admin_id['id'])
        editor_activated = user_service.activate_user(editor_id['id'])
        reader_activated = user_service.activate_user(reader_id['id'])

        self.assertTrue(admin_activated)
        self.assertTrue(editor_activated)
        self.assertTrue(reader_activated)

        # check authorizations for users
        admin_access_admin     = user_service.authorize_user(usr_id=admin_id['id'], access='admin')
        admin_access_editor    = user_service.authorize_user(usr_id=admin_id['id'], access='editor')
        admin_access_reader    = user_service.authorize_user(usr_id=admin_id['id'], access='reader')
        editor_access_admin    = user_service.authorize_user(usr_id=editor_id['id'], access='admin')
        editor_access_editor   = user_service.authorize_user(usr_id=editor_id['id'], access='editor')
        editor_access_reader   = user_service.authorize_user(usr_id=editor_id['id'], access='reader')
        reader_access_admin    = user_service.authorize_user(usr_id=reader_id['id'], access='admin')
        reader_access_editor   = user_service.authorize_user(usr_id=reader_id['id'], access='editor')
        reader_access_reader   = user_service.authorize_user(usr_id=reader_id['id'], access='reader')
        inactive_access_admin  = user_service.authorize_user(usr_id=inactive_id['id'], access='admin')
        inactive_access_editor = user_service.authorize_user(usr_id=inactive_id['id'], access='editor')
        inactive_access_reader = user_service.authorize_user(usr_id=inactive_id['id'], access='reader')
        # admin access assertions
        self.assertTrue(admin_access_admin)
        self.assertTrue(admin_access_editor)
        self.assertTrue(admin_access_reader)
        self.assertEqual(admin_access_admin, 'admin')
        self.assertEqual(admin_access_editor, 'admin')
        self.assertEqual(admin_access_reader, 'admin')
        # editor access assertions
        self.assertFalse(editor_access_admin)
        self.assertTrue(editor_access_editor)
        self.assertTrue(editor_access_reader)
        self.assertEqual(editor_access_editor, 'editor')
        self.assertEqual(editor_access_reader, 'editor')
        # reader access assertions
        self.assertFalse(reader_access_admin)
        self.assertFalse(reader_access_editor)
        self.assertTrue(reader_access_reader)
        self.assertEqual(reader_access_reader, 'reader')
        # inactive user access assertions
        self.assertFalse(inactive_access_admin)
        self.assertFalse(inactive_access_editor)
        self.assertFalse(inactive_access_reader)