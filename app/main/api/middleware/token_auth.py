from flask import request
from functools import wraps
from app.main.services import token_service
import logging

log = logging.getLogger(__name__)


def token_required(f):
    """
    Token Authentication. Extracts Auth Token and validates expiration.
    return user_id as a parameter
    example:
    @token_required
    get(self, user_id):
        return {'messages': 'user id is: ' + user_id}, 200
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'Authorization' in request.headers:
            token_header = request.headers['Authorization']
            if token_header:
                token = token_service.extract_token(token_header)
                if token:
                    authenticated, res = token_service.decode_token(token)
                    if authenticated:
                        params = dict(kwargs)
                        params['user_id'] = res
                        return f(*args, **params)
                        
        return {'message': 'Authentication Failed'}, 401
        
    return decorated