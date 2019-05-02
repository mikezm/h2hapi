from flask import Blueprint
from .main.api.restplus import api
from .main.api.admin.endpoints.user import ns as users_namespace
from .main.api.admin.endpoints.auth import ns as auth_namespace

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(api_blueprint)
api.add_namespace(users_namespace)
api.add_namespace(auth_namespace)
