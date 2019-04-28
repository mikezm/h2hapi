from database.models import Users 
from passlib.hash import sha256_crypt
import settings

def authenticate_user(email=None, password=None):
    """
    authenticates a user
    :return Users db.Document
    """
    user = Users.objects(email=email)[0]
    if user: 
        if sha256_crypt.verify(password, user.password):
            return user
    return None

def hash_password(password):
    return sha256_crypt.encrypt(password, rounds=settings.NUM_ROUNDS)
