from app.main.database.models.user import Users 
from passlib.hash import sha256_crypt
import app.main.config as app_conf
import logging

log = logging.getLogger(__name__)

def authenticate_user(email=None, password=None):
    """
    authenticates a user
    :return Users db.Document
    """
    user = Users.objects(email=email).first()
    if user and user.password: 
        if sha256_crypt.verify(password, user.password):
            return user
    return None

def hash_password(password):
    return sha256_crypt.encrypt(password, rounds=app_conf.HASH_ROUNDS)

def authorize_user(usr_id=None, access='reader'):
    roles = {'admin': 0, 'editor': 1, 'reader': 2}
    user = Users.objects(public_id=usr_id, active=True).first()
    if user and user.role:
        if access in roles:
            if roles[user.role] <= roles[access]:
                return user.role
    return False