from app.main.database.models.user import Users 
from app.main.services import auth_service, token_service
import logging

log = logging.getLogger(__name__)

def create_user(email, password):
    
    existing = Users.objects(email=email)
    if len(existing) > 0:
        return False
    
    pwd_hash = auth_service.hash_password(password)
    user = Users(email=email, password=pwd_hash)
    user.save()
    return dict(id=user.public_id)
    

def activate_user(user_id):
    user = Users.objects(public_id=user_id, deactivated=False).first()
    if user and user.public_id:
        user.update(active=True)
        return True
    return False

def deactivate_user(user_id):
    user = Users.objects(public_id=user_id, deactivated=False).first()
    if user and user.public_id:
        user.update(active=False, deactivated=True)
        return True
    return False

def login_user(email, password):
    user = auth_service.authenticate_user(email=email, password=password)
    if user and user.public_id and not user.deactivated:
        user_id = str(user.public_id)
        passed, fetched_token=token_service.encode_token(user_id, duration=3600)
        if passed:
            res = dict(token=fetched_token, email=email, id=user_id, role=user.role)
            return res
        else:
            return fetched_token
    return None

