import logging

from flask import request
from flask_restplus import Resource
from app.main.api.admin import business, serializers, parsers
from app.main.api.restplus import api
from app.main.api.middleware import token_required, access_required

log = logging.getLogger(__name__)

ns = api.namespace('auth', description='Auth Operations for Users')

#class DM:
#    def get(user_id):
#        return 

@ns.route('/login')
class UsersCollection(Resource):
    @api.expect(parsers.create_user_args)
    @api.doc(form=parsers.create_user_args)
    @api.response(200, 'Authentication Passed', model=serializers.auth_res)
    @api.response(401, 'Authentication Failed', model=serializers.message) 
    #@api.marshal_with(serializers.message, code=401, description='Authentication Failed')
    #@api.marshal_with(serializers.auth_res, code=200, description='Authentication Passed', skip_none=True)
    
    def post(self):
        """
        Login in. Returns an Auth Token
        """
        curr_user = parsers.create_user_args.parse_args(request)
        data  = business.login_user(curr_user)
        if data:
            res = {'message': 'Welcome back', 'data': data}
            return res, 200
        else:
            return {'message': 'Authentication Failed'}, 401 

@ns.route('/test')
class TokenTest(Resource):
    @api.doc(security='apikey')
    @token_required
    @access_required('reader', parameters=True)
    def post(self, user_id, role):
        return {'message': 'success! id: '+ user_id}, 200
