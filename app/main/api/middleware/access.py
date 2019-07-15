from functools import wraps
from app.main.services import auth_service
import logging

log = logging.getLogger(__name__)

class access_level(object):
    """
    authorization decorator for checking access privileges of requester
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
        @access_level('admin', parameters=True)
        def get(self, auth_data):
            return {'messages': 'id: %s <> role: %s ' % (auth_data['id'], auth_data['role']) }, 200
    """
    def __init__(self, access, parameters=False):
        self.access = access
        self.parameters = parameters

    def __call__(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            params = dict(kwargs)
            if 'data' in params and 'user_id' in params['data']:
                usr_id = params['data']['user_id']
                if usr_id:
                    usr_role = auth_service.authorize_user(usr_id=usr_id, access=self.access)
                    if usr_role:
                        if self.parameters:                            
                            auth_data = dict(id=usr_id, role=usr_role)
                            params['data']['auth_data'] = auth_data
                        return f(*args, **params)

            return {'message': 'Not Authorized'}, 401

        return decorated