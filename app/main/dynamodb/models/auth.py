Roles = {
    TableName='users',
    KeySchema=[dict(AttributeName='username', KeyType='HASH')],
    AttributeDefinitions=[dict(AttributeName='username', AttributeType='S')],
    ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
}

class BlacklistedTokens(): 
    TableName = 'BlacklistedTokens'
    KeySchema = [dict(AttributeName='token', KeyType='HASH')],
    AttributeDefinitions = [dict(AttributeName='token', AttributeType='B')]
    ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)

class Users():
    TableName = 'H2H_USERS'
    KeySchema=[
        dict(AttributeName='public_id', KeyType='HASH'),
        dict(AttributeName='email', KeyType='RANGE')
    ]
    AttributeDefinitions = [
        dict(AttributeName='public_id', AttributeType='N'),
        dict(AttributeName='email', AttributeType='S')
    ]
    ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)