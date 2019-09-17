from flask import Blueprint, Flask
from flask_cors import CORS
from app.main.api.restplus import api
from app.main.api.controllers.user import ns as users_namespace
from app.main.api.controllers.article import ns as article_namespace
from app.main.config import config_by_name

api_blueprint = Blueprint('api', __name__, url_prefix='/api',)
api.init_app(api_blueprint)
api.add_namespace(users_namespace)
api.add_namespace(article_namespace)

def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_by_name[config_name])
    app.register_blueprint(api_blueprint)
    
    
    return app
