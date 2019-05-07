from flask import request
from functools import wraps
from app.main.services import user_service
import logging

log = logging.getLogger(__name__)


#def token_required(f):
#    """
#    Token Authentication. Extracts Auth Token and validates expiration.
#    return user_id as a parameter
#    example:
#    @token_required
#    get(self, user_id):
#        return {'messages': 'user id is: ' + user_id}, 200
#    """
#    @wraps(f)
#    def decorated(*args, **kwargs):
#        if 'Authorization' in request.headers:
#            token_header = request.headers['Authorization']
#            if token_header:
#                token = token_service.extract_token_from_header(token_header)
#                if token:
#                    authenticated, res = token_service.decode_token(token)
#                    if authenticated:
#                        params = dict(kwargs)
#                        params['user_id'] = res
#                        return f(*args, **params)
#                        
#        return {'message': 'Authentication Failed'}, 401
#        
#    return decorated
#
#class access_required(object):
#    """
#    authorization decorator for setting access privileges to select endpoints
#    works in concert with token_required to asses access rights of token authenticated user
#    parameters:
#    <string> [admin|editor|reader] - the access level required
#    parameters <boolean> - defaults to False. Whether or not to return user_id and usr_role as parameters
#    examples:
#        @token_required
#        @access_required('admin')
#        def get(self):
#            return {'messages': 'auth passed'}, 200
#        -------------------------------------------------------    
#        @token_required
#        @access_required('admin', parameters=True)
#        def get(self, auth_data):
#            return {'messages': 'id: %s <> role: %s ' % (auth_data['id'], auth_data['role']) }, 200
#    """
#    def __init__(self, access, parameters=False):
#        self.access = access
#        self.parameters = parameters
#
#    def __call__(self, f):
#        @wraps(f)
#        def decorated(*args, **kwargs):
#            params = dict(kwargs)
#            if 'user_id' in params:
#                usr_id = params.pop('user_id')
#                if usr_id:
#                    usr_role = auth_service.authorize_user(usr_id=usr_id, access=self.access)
#                    if usr_role:
#                        if self.parameters:                            
#                            auth_data = dict(id=usr_id, role=usr_role)
#                            params['auth_data'] =  auth_data
#                        return f(*args, **params)
#
#            return {'message': 'Not Authorized'}, 401
#
#        return decorated
#
def basic_auth_required(f):
    """
    Basic Authentication. Extracts username and password from request.
    return auth as a parameter
    example:
    @basic_auth_required
    get(self, auth):
        return {'messages': 'username is: ' + auth.username}, 200
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        params = dict(kwargs)
        basic_auth = request.authorization
        if basic_auth and basic_auth.username and basic_auth.password:
            auth_data = user_service.login_user(basic_auth.username, basic_auth.password)
            if auth_data:
                params['auth_data'] = auth_data
                return f(*args, **params)

        return {'message': 'Authentication Failed'}, 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'} 

    return decorated