from app.main.dynamodb import articles
import logging
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from flask import json

log = logging.getLogger(__name__)

article_fields = [
    'headline',
    'article_date',
    'speakers',
    'info',
    'paragraphs',
    'tags'
]

def get_articles_summary():
    """
    :return: Array(Object) - summary of all articles
    """
    res = articles.scan(
        Select='SPECIFIC_ATTRIBUTES',
        ProjectionExpression='headline, speakers, article_date, tags, info'
    )
    if res['Count'] < 1:
        return None

    return res['Items']
        
def get_article(headline):
    """
    :return: article detail
    """
    res = articles.get_item(Key=dict(headline=headline))
    if 'Item' not in res:
        return None

    return res['Item']

def add_article(data):
    """
    :return: message, status code
    """

    # check to make sure article doesn't exist
    duplicate_articles = articles.query(
        Select='COUNT', 
        KeyConditionExpression=Key('headline').eq(data['headline'])
    )
    if duplicate_articles['Count'] > 0:
        return 'Article already exists.', 403

    new_article = dict(created_date=datetime.utcnow().isoformat())

    for item in article_fields:
        try:
            new_article[item] = data[item] if data[item] != '' else None
        except KeyError:
            pass

    try:
        articles.put_item(Item=new_article)
    except ClientError:
        print(json.dumps(new_article))
        return 'Could not add article', 400

    return 'Article added.', 201
        
