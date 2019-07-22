import os

APP_RUN_ENV = os.environ.get("H2H_API_ENV")
HASH_ROUNDS = 87943
SKEY = os.environ.get("H2H_SECRET_KEY")

MONGO_HOST = os.environ.get("MONGO_ATLAS_HOST")
MONGO_QS = os.environ.get("MONGO_ATLAS_QS") 
MONGO_USER = os.environ.get("MONGO_ATLAS_USER") 
MONGO_PWD = os.environ.get("MONGO_ATLAS_PWD") 

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
    MONGO_DBNAME = 'h2h_test_db'
    #MONGODB_HOST = "mongodb://%s:%s@%s/%s?%s" % (MONGO_USER, MONGO_PWD, MONGO_HOST, MONGO_DBNAME, MONGO_QS)
    MONGODB_HOST = "mongodb://localhost/%s" % (MONGO_DBNAME)
    SSL_CONTEXT = ('adhoc')
    
class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SERVER_NAME = 'halfwaytohistory.com'
    MONGO_DBNAME = 'h2h_test_db'
    #MONGODB_HOST = "mongodb://%s:%s@%s/%s?%s" % (MONGO_USER, MONGO_PWD, MONGO_HOST, MONGO_DBNAME, MONGO_QS)
    MONGODB_HOST = "mongodb://localhost/%s" % (MONGO_DBNAME)
    SSL_CONTEXT = ('adhoc')
    
class ProductionConfig(Config):
    DEBUG = False
    SERVER_NAME = 'halfwaytohistory.com'
    MONGO_DBNAME = 'h2hdb'
    MONGODB_HOST = "mongodb://%s:%s@%s/%s?%s" % (MONGO_USER, MONGO_PWD, MONGO_HOST, MONGO_DBNAME, MONGO_QS)
    SSL_CONTEXT = ('adhoc')

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
