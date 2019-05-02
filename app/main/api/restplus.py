import logging
from flask_restplus import Api
#import settings
from flask_mongoengine import DoesNotExist
from mongoengine.errors import NotUniqueError
from app.main.config import APP_RUN_ENV

log = logging.getLogger(__name__)

authorizations = {
    'apikey' : {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(version='1.0', title='Halfway to History API', authorizations=authorizations,
          description='Article and User management for Halfway to History project')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if APP_RUN_ENV == 'prod': #not app.config['DEBUG']: #settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(DoesNotExist)
def database_not_found_error_handler(e):
    log.warning('dummy text')
    return {'message': 'A database result was required but none was found.'}, 404

@api.errorhandler(NotUniqueError)
def database_user_already_exists_error_handler(e):
    log.warn('User creation rejected: User already exists')
    return {'message': 'User Already Exists'}, 400

