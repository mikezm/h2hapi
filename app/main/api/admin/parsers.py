from flask_restplus import reqparse

create_user_args = reqparse.RequestParser()
create_user_args.add_argument('email', type=str, required=True, help='Email Address')
create_user_args.add_argument('password', type=str, required=True, help='Password')

reset_password_args = reqparse.RequestParser()
reset_password_args.add_argument('email', type=str, required=True, help='Email Address')
reset_password_args.add_argument('password', type=str, required=True, help='Password')

auth_header = reqparse.RequestParser()
auth_header.add_argument('Authorization', type=str, required=True, help='Authorization Token', location='headers')
