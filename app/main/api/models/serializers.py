from flask_restplus import fields
from app.main.api.restplus import api
from datetime import datetime

# nullable fields
class NullableString(fields.String):
    __schema_type__ = ['string', 'null']
    __schema_example__ = 'nullable string'

class NullableDate(fields.Date):
    __schema_type__ = ['datetime', 'null']
    __schema_example__ = 'nullable Datetime'


msg_field = fields.String(required=False, description='Message')
eml_field = fields.String(required=True, description='email address')
userid_field = fields.String(required=True, description='user id')
pwd_field = fields.String(required=True, description='password')
token_field = fields.String(required=True, description='Auth Token')
role_field = fields.String(required=True, description='Role')
err_field = fields.String(required=False, description='Error')
token_exp_field = fields.Integer(required=True, description='Token Expiration')

new_user = api.model('User', {
    'email': eml_field,
    'password': pwd_field
})

error = api.model('Error', {
    'error': err_field
})

message = api.model('Message', {
    'message': msg_field
})

password_reset = api.model('Password Reset', {
    'message': msg_field,
    'email': eml_field
})

auth_data = api.model('Auth data', {
    'token': token_field,
    'id': userid_field,
    'user_role': role_field,
    'expires_in': token_exp_field
})

auth_res = api.model('Auth Response', {
    'message': msg_field,
    'data': fields.Nested(auth_data)
})

## Articles ##

article_paragraph = api.model('Article Parapaph', {
    'text': NullableString(required=True, description='Paragraph text'),
    'speaker': NullableString(required=False, description='Speaker name'),
    'question': fields.Boolean(required=False, description='Question'),
    'comment': fields.Boolean(required=False, description='Comment')
})

article_speaker = api.model('Article Speaker', {
    'speaker_name': fields.String(required=False, description='Speaker name'),
    'affiliation': NullableString(required=False, description='Speaker Affiliation')
})

# fields
headline_field = article_headline = fields.String(required=True, description='Article Headline')
speakers_field = fields.List(fields.Nested(article_speaker), description='Speakers')
date_field = NullableString(description='Article Date')
info_field = fields.List(fields.String)
tags_field = fields.List(fields.String)
paragraphs_field = fields.List(fields.Nested(article_paragraph), description='Article Paragraphs', required=False)

article_summary = api.model('Article Summary', {
    'headline': headline_field,
    'speakers': speakers_field,
    'article_date': date_field,
    'info': info_field,
    'tags': tags_field,
})

article = api.model('Article', {
    'headline': headline_field,
    'speakers': speakers_field,
    'article_date': date_field,
    'info': info_field,
    'tags': tags_field,
    'paragraphs': paragraphs_field
})

articles_summary_response = api.model('Article Summary Response', {
    'data': fields.List(fields.Nested(article_summary))
})

get_article_request = api.model('Get Article Request', {
    'headline': article_headline
})

get_article_response = api.model('Get Article Response', {
    'data': fields.Nested(article)
})

