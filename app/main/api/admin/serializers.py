from flask_restplus import fields
from app.main.api.restplus import api

msg_field = fields.String(required=False, description='Message')
eml_field = fields.String(required=True, description='email address')
userid_field = fields.String(required=True, description='user id')
pwd_field = fields.String(required=True, description='password')
token_field = fields.String(required=True, description='Auth Token')
role_field = fields.String(required=True, description='Role')
access_field = fields.String(required=True, description='Access', default='read')

new_user = api.model('User', {
    'email': eml_field,
    'password': pwd_field
})

message = api.model('Message', {
    'message': msg_field
})

password_reset = api.model('Password Reset', {
    'message': msg_field,
    'email': eml_field
})

auth_data = api.model('Auth data', {
    'token': token_field,
    'id': userid_field,
    'email': eml_field,
    'role': role_field,
    'access': access_field
})

auth_res = api.model('Auth Response', {
    'message': msg_field,
    'data': fields.Nested(auth_data)
})

