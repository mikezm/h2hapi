from app.tests.base import BaseTestCase
from app.main.services import user_service, auth_service
from app.main.database.models.user import Users 
from bson.objectid import ObjectId

class TestUserService(BaseTestCase):
    eml = 'test@unittest.com'
    pwd = '12345678'

    def test_create_user(self):
        my_id = user_service.create_user(email=self.eml, password=self.pwd)
        fetched_user = Users.objects(public_id=my_id['id']).first()
        # user is created. not yet active or deactivated
        self.assertFalse(fetched_user.deactivated)
        self.assertFalse(fetched_user.active)
        self.assertEqual(my_id['id'], fetched_user.public_id)
        dup_user = user_service.create_user(email=self.eml, password=self.pwd)
        self.assertFalse(dup_user)

    def test_activate_user(self):
        my_id = user_service.create_user(email=self.eml, password=self.pwd)
        test_us = user_service.activate_user(my_id['id'])
        fetched_user = Users.objects(public_id=my_id['id']).first()
        # user is activated now
        self.assertTrue(test_us)
        self.assertTrue(fetched_user.active)
        self.assertFalse(fetched_user.deactivated)
        # set user to deactivated
        fetched_user.update(deactivated=True, active=False)
        fail_test_us = user_service.activate_user(my_id['id'])
        fetched_fail_user = Users.objects(public_id=my_id['id']).first()
        # activation should fail now
        self.assertFalse(fail_test_us)
        self.assertFalse(fetched_fail_user.active)

    def test_deactivate_user(self):
        my_id = user_service.create_user(email=self.eml, password=self.pwd)
        test_us = user_service.deactivate_user(my_id['id'])
        fetched_user = Users.objects(public_id=my_id['id']).first()
        # should inactive and deactivated
        self.assertTrue(test_us)
        self.assertFalse(fetched_user.active)
        self.assertTrue(fetched_user.deactivated)

    def test_login_user(self):
        my_id = user_service.create_user(email=self.eml, password=self.pwd)
        test_res = user_service.login_user(email=self.eml, password=self.pwd)
        # should login without issue
        self.assertEqual(self.eml, test_res['email'])
        self.assertEqual(str(my_id['id']), test_res['id'])
        # test for deactivated account login attempt
        user_service.deactivate_user(my_id['id'])
        fail_res = user_service.login_user(email=self.eml, password=self.pwd)
        # assert failure to login
        self.assertIsNone(fail_res)

