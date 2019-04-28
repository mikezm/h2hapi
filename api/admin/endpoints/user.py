import logging

from flask import request
from flask_restplus import Resource
from api.admin import business, serializers, parsers
from api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('users', description='Operations for Users')

@ns.route('/create')
class UsersCollection(Resource):

    @api.expect(parsers.create_user_args)
    @api.marshal_with(serializers.message)
    #@api.response(201, 'User creation successful', serializers.message)
    def post(self):
        """
        Creates a new User
        """
        new_user = parsers.create_user_args.parse_args(request)
        user_id = business.create_user(new_user)
        return {'message': 'User Created'}, 201