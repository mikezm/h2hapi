from database.models import Users 
from api.middleware import auth_service, token_service

def create_user(data):
    email = data.get('email')
    pwd = data.get('password')
    pwd_hash = auth_service.hash_password(pwd)
    user = Users(email=email, password=pwd_hash)
    user.save()
    return dict(id=user.id)

def login_user(data):
    email = data.get('email')
    pwd = data.get('password')
    user = auth_service.authenticate_user(email=email, password=pwd)
    if user and user.id:
        t=token_service.encode_token(str(user.id), duration=86400)
        return dict(
                token=t,
                email=email,
                id=str(user.id),
                role=user.role
            )
    return None


    