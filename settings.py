import os

# Flask settings
FLASK_SERVER_NAME = 'localhost:8888'
FLASK_DEBUG = False  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False


# Mongo DB URI
if os.environ["H2H_API_ENV"] == 'prod':
    MONGO_DBNAME = 'h2hdb' 
else:
    FLASK_DEBUG = True
    MONGO_DBNAME = 'h2h_test_db'
MONGO_HOST = os.environ["MONGO_ATLAS_HOST"] 
MONGO_USER = os.environ["MONGO_ATLAS_USER"] 
MONGO_PWD = os.environ["MONGO_ATLAS_PWD"] 
MONGO_URI = "mongodb+srv://%s:%s@%s/%s?retryWrites=true" % (MONGO_USER, MONGO_PWD, MONGO_HOST, MONGO_DBNAME)

# mongodb+srv://h2hapi:6j1yv1bg4A33f9ss@cluster0-bdme9.gcp.mongodb.net/h2hdb?retryWrites=true

# secret key
SECRET_KEY = os.environ["H2H_SECRET_KEY"]

# hash rounds
NUM_ROUNDS = 87943