
# https://github.com/postrational/rest_api_demo/blob/master/rest_api_demo/database/models.py
# https://flask-pymongo.readthedocs.io/en/latest/#flask_pymongo.PyMongo.init_app
import sys, os
import DNS as dns
from flask import Flask, Blueprint

import logging.config
from database import db
from database.models import init_roles
from api.restplus import api
import settings
#from api.middleware.auth import jwt

# namespace imports
from api.admin.endpoints.user import ns as users_namespace
from api.admin.endpoints.auth import ns as auth_namespace

app = Flask(__name__)

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), './logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['MONGODB_HOST'] = settings.MONGO_URI
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    #flask_app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
    flask_app.config['BCRYPT_ROUNDS'] = settings.NUM_ROUNDS
    #flask_app.config['SECRET_KEY'] = settings.SECRET_KEY
    #flask_app.config['JWT_AUTH_URL_RULE'] = '/api/auth'
    #flask_app.config['JWT_AUTH_ENDPOINT'] = '/login' 

def initialize_app(flask_app):
    configure_app(flask_app)
    #jwt.init_app(flask_app)
    api_blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(api_blueprint)
    api.add_namespace(users_namespace)
    api.add_namespace(auth_namespace)
    flask_app.register_blueprint(api_blueprint)
    
    db.init_app(flask_app)
    
    #init_roles()

def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
