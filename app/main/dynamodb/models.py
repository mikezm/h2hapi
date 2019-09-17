from app.main.config import USERS_TABLENAME, BLTOKENS_TABLENAME, ARTICLES_TABLENAME

BlacklistedTokens = dict( 
    TableName = BLTOKENS_TABLENAME,
    KeySchema = [dict(AttributeName='auth_token', KeyType='HASH')],
    AttributeDefinitions = [dict(AttributeName='auth_token', AttributeType='S')],
    ProvisionedThroughput = dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
)

Users = dict(
    TableName = USERS_TABLENAME,
    KeySchema=[dict(AttributeName='email', KeyType='HASH')],
    AttributeDefinitions = [dict(AttributeName='email', AttributeType='S')],
    ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
)

Articles = dict(
    TableName = ARTICLES_TABLENAME,
    KeySchema=[dict(AttributeName='headline', KeyType='HASH')],
    AttributeDefinitions = [dict(AttributeName='headline', AttributeType='S')],
    ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
)