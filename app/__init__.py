from flask import Blueprint
from app.main.api.restplus import api
from app.main.api.controllers.user import ns as users_namespace
from app.main.api.controllers.auth import ns as auth_namespace

api_blueprint = Blueprint('api', __name__, url_prefix='/api',)
api.init_app(api_blueprint)
api.add_namespace(users_namespace)
api.add_namespace(auth_namespace)
