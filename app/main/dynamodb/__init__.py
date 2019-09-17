import boto3, os
from app.main.dynamodb.models import Users, BlacklistedTokens, Articles
from app.main.config import APP_RUN_ENV, HASH_ROUNDS
from passlib.hash import sha256_crypt
from bson.objectid import ObjectId
from datetime import datetime

db_tables = [Users, BlacklistedTokens, Articles]

if APP_RUN_ENV == 'dev':
    db = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
    client = boto3.client('dynamodb', endpoint_url='http://localhost:8000')
else:
    db = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')

# create table objects
users = db.Table(Users['TableName'])
tokens = db.Table(BlacklistedTokens['TableName'])
articles = db.Table(Articles['TableName'])

## add tables
def create_db_tables():
    existing_tables = client.list_tables()['TableNames']
    for db_table in db_tables:
        if db_table['TableName'] not in existing_tables:
            table = db.create_table(
                AttributeDefinitions=db_table['AttributeDefinitions'],
                TableName=db_table['TableName'],
                KeySchema=db_table['KeySchema'],
                ProvisionedThroughput=db_table['ProvisionedThroughput']
            )
            table.meta.client.get_waiter('table_exists').wait(TableName=db_table['TableName'])

# drop all tables
def drop_db_tables():
    existing_tables = client.list_tables()['TableNames']
    for db_table in db_tables:
        if db_table['TableName'] in existing_tables:
            client.delete_table(TableName=db_table['TableName'])
            waiter = client.get_waiter('table_not_exists')
            waiter.wait(TableName=db_table['TableName'])

# create's the admin user
def create_admin():
    email = os.environ.get('H2H_ADMIN_USERNAME')
    password = os.environ.get('H2H_ADMIN_PWD')
    existing_tables = client.list_tables()['TableNames']
    if Users['TableName'] in existing_tables:
        res = users.query(Select='COUNT', KeyConditionExpression=boto3.dynamodb.conditions.Key('email').eq(email))
        if res['Count'] > 0:
            return 

        pwd_hash = sha256_crypt.encrypt(password, rounds=HASH_ROUNDS)
        new_id = str(ObjectId())
        users.put_item(Item=
            dict(
                email=email, 
                password=pwd_hash, 
                user_role='admin',
                id=new_id, 
                active=True, 
                deactivated=False, 
                created_date=datetime.utcnow().isoformat()
            )
        )



