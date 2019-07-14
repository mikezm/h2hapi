import os
import logging.config
from app.main import create_app
from app import api_blueprint
from app.main.database.models import create_all

app = create_app(os.environ.get('H2H_API_ENV') or 'dev')
app.register_blueprint(api_blueprint)

if app.config['DEBUG']:
    logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), './logging.conf'))
    logging.config.fileConfig(logging_conf_path)
    log = logging.getLogger(__name__)
    log.info('>>>>> Starting development server at https://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))

app.run(
    debug=app.config['DEBUG'],
    ssl_context=app.config['SSL_CONTEXT']
)
