import os

APP_RUN_ENV = os.environ.get("H2H_API_ENV")
HASH_ROUNDS = os.environ.get("H2H_HASH_ROUNDS")
SKEY = os.environ.get("H2H_SECRET_KEY")

USERS_TABLENAME = os.environ.get("USERS_TABLENAME")
BLTOKENS_TABLENAME = os.environ.get("BLTOKENS_TABLENAME")

class Config:
    SECRET_KEY = SKEY
    NUM_ROUNDS = HASH_ROUNDS
    DEBUG = False  # Do not use debug mode in production
    # Flask-Restplus settings
    SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    ERROR_404_HELP = False    

class DevelopmentConfig(Config):
    DEBUG = True
    SERVER_NAME = 'localhost:8888'
    SSL_CONTEXT = ('adhoc')

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SERVER_NAME = 'halfwaytohistory.com'
    SSL_CONTEXT = ('adhoc')
    
class ProductionConfig(Config):
    DEBUG = False
    SERVER_NAME = 'halfwaytohistory.com'
    SSL_CONTEXT = ('adhoc')

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
