from flask import request
from functools import wraps
from app.main.services import user_service
import logging

log = logging.getLogger(__name__)

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
                params['data'] = dict(auth_data=auth_data)
                return f(*args, **params)

        return {'message': 'Authentication Failed'}, 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'} 

    return decorated