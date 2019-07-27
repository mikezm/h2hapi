import boto3
from app.main.dynamodb.models import Users, BlacklistedTokens
from app.main.config import APP_RUN_ENV

db_tables = [Users, BlacklistedTokens]

if APP_RUN_ENV == 'dev':
    db = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
    client = boto3.client('dynamodb', endpoint_url='http://localhost:8000')
else:
    db = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')

# create table objects
users = db.Table(Users['TableName'])
tokens = db.Table(BlacklistedTokens['TableName'])

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

def drop_db_tables():
    existing_tables = client.list_tables()['TableNames']
    for db_table in db_tables:
        if db_table['TableName'] in existing_tables:
            client.delete_table(TableName=db_table['TableName'])
            waiter = client.get_waiter('table_not_exists')
            waiter.wait(TableName=db_table['TableName'])





