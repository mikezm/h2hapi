from flask import request
from functools import wraps
from services import token_service, auth_service
import logging

log = logging.getLogger(__name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token_header = None
        if 'Authorization' in request.headers:
            token_header = request.headers['Authorization']

        if not token_header:
            return {'message:': 'Missing Token in Headers'}, 401

        token = token_service.extract_token_from_header(token_header)
        if not token:
            return {'message:': 'Could not read supplied token'}, 401

        authenticated, user_id = token_service.decode_token(token)
        if not authenticated:
            return {'message': res}, 401
        
        authorized = auth_service.authorize_user(usr_id=user_id, access='editor')
        if not authorized:
            return {'message': 'Not Authorized'}, 401
            
        return f(*args, **kwargs)    
    return decorated