import sys, os, unittest
import logging.config
from flask_script import Manager
from app.main import create_app
from app import api_blueprint

app = create_app(os.environ["H2H_API_ENV"] or 'dev')
app.register_blueprint(api_blueprint)
if app.config['DEBUG']:
    logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), './logging.conf'))
    logging.config.fileConfig(logging_conf_path)
    log = logging.getLogger(__name__)
    log.info('>>>>> Starting development server at https://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))

app.app_context().push()
manager = Manager(app)

@manager.command
def run():
    app.run(
        debug=app.config['DEBUG'],
        ssl_context=app.config['SSL_CERTS']
    )

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
