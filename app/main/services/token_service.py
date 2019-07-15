import jwt
import app.main.config as app_conf
from flask import request, json
from datetime import datetime, timedelta
import logging, re
from app.main.database.models.auth import BlacklistedTokens

log = logging.getLogger(__name__)

def extract_token(token_string):
    p = re.compile('(token|bearer)\s{1}', re.IGNORECASE)
    match_token = p.match(token_string)
    if match_token:
        token = token_string.split(match_token.group(0))[1]
        if token and token!=' ':
            return token
    return False

def encode_token(user_id, duration=120):
    """
    Generates the Auth Token
    :return: string
    """
    now = datetime.utcnow()
    expire = now + timedelta(days=0, seconds=duration) 
    payload = {
        'exp': expire,
        'iat': now,
        'sub': user_id
    }
    try:
        return True, jwt.encode(
            payload,
            app_conf.SKEY,
            algorithm='HS256'
        ).decode('utf-8')
    except Exception as e:
        return False, e

def decode_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: bool, integer|string
    """
    token = bytes(auth_token, 'utf-8')
    try:
        payload = jwt.decode(auth_token, app_conf.SKEY, algorithm='HS256')
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, 'Expired token. Please log in again.'
    except jwt.InvalidTokenError:
        return False, 'Invalid token. Please log in again.'

def blacklist_token(auth_token):
    """
    Blacklists an auth_token
    :param auth_token:
    :return: bool
    """
    exp_date = datetime.utcnow()
    token_is_active, res = decode_token(auth_token)
    if token_is_active:
        exp_date = datetime.utcfromtimestamp(res['exp']) 
    bt = BlacklistedTokens(token=auth_token, expiration_date=exp_date)
    try:
        bt.save()
        return True
    except e:
        return False

def is_token_blacklisted(auth_token):
    """
    Checks to see if token is currently blacklisted
    :param auth_token:
    :return: bool
    """
    bt = BlacklistedTokens.objects(token=auth_token).first()
    if bt and bt.token:
        return True
    return False