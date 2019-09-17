import logging
from flask_restplus import Api
from app.main.config import APP_RUN_ENV
from app.main.dynamodb import client

log = logging.getLogger(__name__)

authorizations = {
    'apikey' : {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'basicAuth' : {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(version='1.0', 
    title='Halfway to History API', 
    description='Article and User management for Halfway to History project',
    authorizations=authorizations,
    validate=True)

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if APP_RUN_ENV == 'prod': 
        return {'message': message}, 500


@api.errorhandler(client.exceptions.ResourceNotFoundException)
def database_not_found_error_handler(e):
    log.warning('dummy text')
    return {'message': 'A database result was required but none was found.'}, 404


