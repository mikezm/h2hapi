from flask import request
from functools import wraps
from services import token_service, auth_service
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
        params = dict(kwargs)
        token_header = None
        if 'Authorization' in request.headers:
            token_header = request.headers['Authorization']

        if not token_header:
            return {'message:': 'Missing Token in Headers'}, 401

        token = token_service.extract_token_from_header(token_header)
        if not token:
            return {'message:': 'Could not read supplied token'}, 401

        authenticated, res = token_service.decode_token(token)
        if not authenticated:
            return {'message': res}, 401
        
        params['user_id'] = res
            
        return f(*args, **params)    
    return decorated

class access_required(object):
    """
    authorization decorator for setting access privileges to select endpoints
    works in concert with token_required to asses access rights of token authenticated user
    parameters:
    <string> [admin|editor|reader] - the access level required
    parameters <boolean> - defaults to False. Whether or not to return user_id and usr_role as parameters
    examples:
        @token_required
        @access_required('admin')
        def get(self):
            return {'messages': 'auth passed'}, 200
        -------------------------------------------------------    
        @token_required
        @access_required('admin', parameters=True)
        def get(self, user_id, usr_role):
            return {'messages': 'user usr_role is: ' + usr_role}, 200
    """
    def __init__(self, access, parameters=False):
        self.access = access
        self.parameters = parameters

    def __call__(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            params = dict(kwargs)
            if 'user_id' in params:
                if self.parameters:
                    usr_id = params['user_id']
                else:
                    usr_id = params.pop('user_id')

            if not usr_id:
                return {'message': 'Not Authorized'}, 401

            usr_role = auth_service.authorize_user(usr_id=usr_id, access=self.access)
            if not usr_role:
                return {'message': 'Not Authorized'}, 401

            if self.parameters:
                params['role'] =  usr_role

            return f(*args, **params)
        return decorated