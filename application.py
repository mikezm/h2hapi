import os
import logging.config
from app import create_app

app = create_app(os.environ.get('H2H_API_ENV') or 'dev')

if app.config['DEBUG']:
    # True for 
    logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), './logging.conf'))
    logging.config.fileConfig(logging_conf_path)
    log = logging.getLogger(__name__)
    log.info('>>>>> Starting development server at https://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))

if __name__ == "__main__":
    app.run(
        debug=app.config['DEBUG'],
        ssl_context=app.config['SSL_CONTEXT']
    )
