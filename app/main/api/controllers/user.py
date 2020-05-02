import logging

from flask import abort
from flask_restplus import Resource
from app.main.api.models import serializers
from app.main.services import user_service, mail_service, token_service
from app.main.api.restplus import api
from app.main.api.middleware.token_auth import token_required
from app.main.api.middleware.basic_auth import basic_auth_required
from app.main.api.middleware.access import access_level

log = logging.getLogger(__name__)

ns = api.namespace('user', description='Operations for Users')


@ns.route('/create')
class CreateUser(Resource):

    @api.expect(serializers.new_user)
    @api.marshal_with(serializers.message)
    def post(self):
        """
        Creates a new User
        """
        new_user = api.payload
        user_id = user_service.create_user(new_user['email'], new_user['password'])
        if not user_id:
            abort(400, 'User Already Exists')

        token_passed, token = token_service.encode_token(user_id, duration=3600)
        if not token_passed:
            abort(400, '{}'.format(token))

        email_result = mail_service.send_activation_email(new_user['email'], token)
        return {'message': 'User Created. Email delivery: {}'.format(email_result)}, 201


@ns.route('/activate')
class ActivateUser(Resource):

    @api.doc(security='apikey')
    @api.response(201, 'User Activated', model=serializers.message)
    @api.response(401, 'Activation Failed', model=serializers.message)
    @api.marshal_with(serializers.message)
    @token_required
    def get(self, data):
        """
        Activates a user
        """
        res = user_service.activate_user(data['user_id'])
        if not res:
            abort(401, 'Activation Failed')

        return {'message': 'User Activated'}, 200


@ns.route('/login')
class LoginUser(Resource):
    @api.doc(security='basicAuth')
    @api.response(200, 'Authentication Passed', model=serializers.auth_data)
    @basic_auth_required
    def get(self, data):
        """
        Login. Returns an Auth Token
        """
        return data['auth_data'], 200


@ns.route('/test')
class TokenTest(Resource):
    @api.doc(security='apikey')
    @token_required
    @access_level('reader', parameters=True)
    def get(self, data):
        return {'message': 'success!', 'user_role': data['auth_data']['user_role']}, 200


@ns.route('/logout')
class LogoutUser(Resource):
    @api.doc(security='apikey')
    @token_required
    def get(self, data):
        logged_out = token_service.blacklist_token(data['token'])
        if logged_out:
            return {'message': 'logged out'}, 200
        else:
            return {'message': 'failed'}, 401
