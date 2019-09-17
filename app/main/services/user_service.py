from app.main.dynamodb import users
from app.main.services import token_service
from passlib.hash import sha256_crypt
import app.main.config as app_conf
import logging
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from bson.objectid import ObjectId

log = logging.getLogger(__name__)

def create_user(email, password, role='reader'):
    """
    Creates new user
    :return: False|dict['id']
    """
    res = users.query(Select='COUNT', KeyConditionExpression=Key('email').eq(email))
    if res['Count'] > 0:
        return False

    pwd_hash = sha256_crypt.encrypt(password, rounds=app_conf.HASH_ROUNDS)
    new_id = str(ObjectId())
    users.put_item(Item=
        dict(
            email=email, 
            password=pwd_hash, 
            user_role=role,
            id=new_id, 
            active=False, 
            deactivated=False, 
            created_date=datetime.utcnow().isoformat()
        )
    )
    return dict(id=new_id)
    
def activate_user(user_id):
    """
    Activates an existing user
    :return: bool
    """
    res = users.scan(Select='SPECIFIC_ATTRIBUTES', ProjectionExpression='email', FilterExpression=Attr('id').eq(user_id) & Attr('deactivated').eq(False))
    if res['Count'] != 1:
        return False

    user = res['Items'][0]
    users.update_item(
        Key=dict(email=user['email']),
        UpdateExpression='SET active = :val1',
        ExpressionAttributeValues={':val1': True}
    )
    return True

def deactivate_user(user_id):
    """
    Deactivates an exising user
    :return: bool
    """
    res = users.scan(Select='SPECIFIC_ATTRIBUTES', ProjectionExpression='email', FilterExpression=Attr('id').eq(user_id))
    if res['Count'] != 1:
        return False

    user = res['Items'][0]
    users.update_item(
        Key=dict(email=user['email']),
        UpdateExpression='SET active = :val1, deactivated = :val2',
        ExpressionAttributeValues={':val1': False, ':val2': True}
    )
    return True

def login_user(email, password, token_expiry=3600):
    """
    Login an active user
    :return: None|Err|dict['token', 'email', 'id', 'user_role']
    """
    res = users.scan(
        Select='SPECIFIC_ATTRIBUTES',
        ProjectionExpression='id, user_role, password',
        FilterExpression=Key('email').eq(email) & Attr('deactivated').eq(False)
    )
    if res['Count'] != 1:
        return None
    
    user = res['Items'][0]
    if not sha256_crypt.verify(password, user['password']):
        return None

    passed, fetched_token=token_service.encode_token(user['id'], duration=token_expiry)
    if passed:
        return dict(token=fetched_token, id=user['id'], user_role=user['user_role'], expires_in=token_expiry)

    return fetched_token

def authorize_user(usr_id=None, access='reader'):
    """
    Authorizes an existing user
    :return: bool
    """
    roles = {'admin': 0, 'editor': 1, 'reader': 2}
    res = users.scan(
        Select='SPECIFIC_ATTRIBUTES',
        ProjectionExpression='user_role',
        FilterExpression=Attr('id').eq(usr_id) & Attr('active').eq(True)
    )
    if res['Count'] != 1:
        return False
    
    user = res['Items'][0]

    if roles[user['user_role']] <= roles[access]:
        return user['user_role']

    return False