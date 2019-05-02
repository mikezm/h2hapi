
# https://github.com/postrational/rest_api_demo/blob/master/rest_api_demo/database/models.py
# https://flask-pymongo.readthedocs.io/en/latest/#flask_pymongo.PyMongo.init_app
import sys, os, unittest
import logging.config
from flask_script import Manager
import unittest
from app.main import create_app
from app import api_blueprint
#import DNS as dns
#from flask import Flask, Blueprint
#
#from flask_script import Manager
#import unittest
#
#from app.main.database import db
#from api.restplus import api
#import settings
#from api.middleware.auth import jwt

# namespace imports
#from api.admin.endpoints.user import ns as users_namespace
#from api.admin.endpoints.auth import ns as auth_namespace
#
#from config import config_by_name

#app = Flask(__name__)

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), './logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

#def configure_app(flask_app):
    #flask_app.config.from_object(config_by_name['dev'])
    #flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    #flask_app.config['MONGODB_HOST'] = settings.MONGO_URI
    #flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    #flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    #flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    #flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

#def initialize_app():
#    #configure_app(flask_app)
#    flask_app = Flask(__name__)
#    flask_app.config.from_object(config_by_name['dev'])
#    api_blueprint = Blueprint('api', __name__, url_prefix='/api')
#    api.init_app(api_blueprint)
#    api.add_namespace(users_namespace)
#    api.add_namespace(auth_namespace)
#    flask_app.register_blueprint(api_blueprint)
#    
#    db.init_app(flask_app)
#    return flask_app
    
    #init_roles()

#def main():
#    initialize_app(app)
#    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
#    app.run(debug=settings.FLASK_DEBUG)

#app = initialize_app(app)
app = create_app(os.environ["H2H_API_ENV"] or 'dev')
app.register_blueprint(api_blueprint)
log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))

# new stuff
app.app_context().push()
manager = Manager(app)

@manager.command
def run():
    app.run(debug=app.config['DEBUG'])

# end new stuff
@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/tests', pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == "__main__":
    manager.run()
    #main()
