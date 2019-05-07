import logging

from flask import request, make_response
from flask_restplus import Resource
from app.main.api.models import serializers, parsers
from app.main.api.restplus import api
from app.main.api.middleware.token_auth import token_required
from app.main.api.middleware.access import access_level
from app.main.api.middleware.basic_auth import basic_auth_required

log = logging.getLogger(__name__)

ns = api.namespace('auth', description='Auth Operations for Users')

@ns.route('/login')
class UsersCollection(Resource):
    @api.expect(parsers.login_request)
    @api.doc(form=parsers.create_user_args)
    @api.response(200, 'Authentication Passed', model=serializers.auth_res)
    @api.response(401, 'Authentication Failed', model=serializers.message) 
    #@api.marshal_with(serializers.message, code=401, description='Authentication Failed')
    #@api.marshal_with(serializers.auth_res, code=200, description='Authentication Passed', skip_none=True)
    @basic_auth_required
    def get(self, auth_data):
        """
        Login. Returns an Auth Token
        """
        res = {'message': 'Welcome back', 'data': auth_data}
        return res, 200
        
    
@ns.route('/test')
class TokenTest(Resource):
    @api.doc(security='apikey')
    @token_required
    @access_level('reader', parameters=True)
    def get(self, auth_data):
        return {'message': 'success!', 'role': auth_data['role']}, 200
