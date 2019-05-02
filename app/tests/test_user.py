import unittest
from unittest import TestCase
from app.main.api.admin.business import create_user
from app.main.services import auth_service
from random import randint
from app.main.database.models import Users
from passlib.hash import sha256_crypt

class TestUserSignUp(TestCase):

    def test_hashing(self):
        pwd_one = '1234'
        pwd_two = '3456'
        hash_one = auth_service.hash_password(pwd_one)
        hash_again = auth_service.hash_password(pwd_one)
        hash_two = auth_service.hash_password(pwd_two)
        
        self.assertNotEqual(hash_one, hash_again)
        self.assertTrue(sha256_crypt.verify(pwd_one, hash_one))
        self.assertTrue(sha256_crypt.verify(pwd_two, hash_two))
        self.assertFalse(sha256_crypt.verify(pwd_one, hash_two))
        self.assertFalse(sha256_crypt.verify(pwd_two, hash_one))


    def test_sign_up(self):
        test_eml = 'test_user%s@unittest.com' % str(randint(0, 100000))
        test_pwd = '1234&sc!'
        test_data = dict(email=test_eml, password=test_pwd)
        test_user = create_user(test_data)
        db = Users.objects(id=test_user['id'])[0]
        self.assertEqual(test_eml, db.email)


