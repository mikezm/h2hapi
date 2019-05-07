import os

APP_RUN_ENV = os.environ["H2H_API_ENV"]
HASH_ROUNDS = 87943
SKEY = os.environ["H2H_SECRET_KEY"]

LOCAL_CERT_PATH = os.environ["HOME"] + "/certs/"
MONGO_HOST = os.environ["MONGO_ATLAS_HOST"] 
MONGO_USER = os.environ["MONGO_ATLAS_USER"] 
MONGO_PWD = os.environ["MONGO_ATLAS_PWD"] 

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
    MONGODB_HOST = "mongodb+srv://%s:%s@%s/%s?retryWrites=true" % (MONGO_USER, MONGO_PWD, MONGO_HOST, MONGO_DBNAME)
    SSL_CERTS = (LOCAL_CERT_PATH + 'h2h_cert.pem', LOCAL_CERT_PATH + 'h2h_key.pem')
    
class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SERVER_NAME = 'localhost:8888'
    MONGO_DBNAME = 'h2h_test_db'
    MONGODB_HOST = "mongodb+srv://%s:%s@%s/%s?retryWrites=true" % (MONGO_USER, MONGO_PWD, MONGO_HOST, MONGO_DBNAME)
    #SSL_CERTS = (LOCAL_CERT_PATH + 'h2h_cert.pem', LOCAL_CERT_PATH + 'h2h_key.pem')
    SSL_CONTEXT = (LOCAL_CERT_PATH + 'h2h_cert.pem', LOCAL_CERT_PATH + 'h2h_key.pem')
    
class ProductionConfig(Config):
    DEBUG = False
    SERVER_NAME = 'halfwaytohistory.com'
    MONGO_DBNAME = 'h2hdb'
    MONGODB_HOST = "mongodb+srv://%s:%s@%s/%s?retryWrites=true" % (MONGO_USER, MONGO_PWD, MONGO_HOST, MONGO_DBNAME)
    SSL_CERTS = ''

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
