import logging

from flask import request
from flask_restplus import Resource
from app.main.api.models import serializers, parsers
from app.main.services import user_service
from app.main.api.restplus import api
from app.main.api.middleware.token_auth import token_required

log = logging.getLogger(__name__)

ns = api.namespace('user', description='Operations for Users')

@ns.route('/create')
class RegisterUser(Resource):

    @api.expect(parsers.create_user_args)
    @api.marshal_with(serializers.message)
    #@api.response(201, 'User creation successful', serializers.message)
    def post(self):
        """
        Creates a new User
        """
        new_user = parsers.create_user_args.parse_args(request)
        user_id = user_service.create_user(new_user['email'], new_user['password'])
        return {'message': 'User Created'}, 201

@ns.route('/activate')
class ActivateUser(Resource):

    @api.doc(security='apikey')
    @api.response(201, 'User Activated', model=serializers.message)
    @api.response(401, 'Activation Failed', model=serializers.message)
    @api.expect(parsers.auth_header)
    @api.marshal_with(serializers.message)
    @token_required
    def put(self, user_id):
        """
        Activates a user
        """
        res = user_service.activate_user(user_id)
        if res:
            return {'message': 'User Activated'}, 200

        return {'message': 'Activation Failed'}, 401 