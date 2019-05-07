from app.tests.base import BaseTestCase
from app.main.services import auth_service
from passlib.hash import sha256_crypt
from app.main.database.models.user import Users 
from bson.objectid import ObjectId

class TestAuthService(BaseTestCase):
    eml = 'test@unittest.com'
    pwd = '12345678'

    def test_hash_password(self):
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

    def test_authenticate_user(self):
        # set up test user in DB
        test_hash = auth_service.hash_password(self.pwd)
        test_user = Users(active=True, email=self.eml, password=test_hash)
        test_user.save()
        # authenticate
        fetched_user = auth_service.authenticate_user(email=self.eml, password=self.pwd)
        # assertions
        self.assertIsNotNone(fetched_user)
        self.assertEqual(fetched_user.id, test_user.id)

    def test_authorize_user(self):
        # set up test users in DB
        test_hash = auth_service.hash_password(self.pwd)
        test_users = []
        admin_user = Users(active=True, email='admin'+self.eml, password=test_hash, role='admin', public_id=ObjectId())
        admin_user.save()
        editor_user = Users(active=True, email='editor'+self.eml, password=test_hash, role='editor', public_id=ObjectId())
        editor_user.save()
        reader_user = Users(active=True, email='reader'+self.eml, password=test_hash, role='reader', public_id=ObjectId())
        reader_user.save()
        inactive_user = Users(active=False, email='inactive'+self.eml, password=test_hash, role='reader', public_id=ObjectId())
        inactive_user.save()
        # check authorizations for users
        admin_access_admin     = auth_service.authorize_user(usr_id=str(admin_user.public_id), access='admin')
        admin_access_editor    = auth_service.authorize_user(usr_id=str(admin_user.public_id), access='editor')
        admin_access_reader    = auth_service.authorize_user(usr_id=str(admin_user.public_id), access='reader')
        editor_access_admin    = auth_service.authorize_user(usr_id=str(editor_user.public_id), access='admin')
        editor_access_editor   = auth_service.authorize_user(usr_id=str(editor_user.public_id), access='editor')
        editor_access_reader   = auth_service.authorize_user(usr_id=str(editor_user.public_id), access='reader')
        reader_access_admin    = auth_service.authorize_user(usr_id=str(reader_user.public_id), access='admin')
        reader_access_editor   = auth_service.authorize_user(usr_id=str(reader_user.public_id), access='editor')
        reader_access_reader   = auth_service.authorize_user(usr_id=str(reader_user.public_id), access='reader')
        inactive_access_admin  = auth_service.authorize_user(usr_id=str(inactive_user.public_id), access='admin')
        inactive_access_editor = auth_service.authorize_user(usr_id=str(inactive_user.public_id), access='editor')
        inactive_access_reader = auth_service.authorize_user(usr_id=str(inactive_user.public_id), access='reader')
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


if __name__ == '__main__':
    unittest.main()