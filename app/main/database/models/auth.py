from app.main.database import db
from mongoengine.errors import NotUniqueError
from datetime import datetime

class Roles(db.Document):
    key = db.IntField(required=True, unique=True, db_field='key')
    role = db.StringField(required=True, unique=True, db_field='role')

class BlacklistedTokens(db.Document):
    token = db.StringField(required=True, db_field='token', max_length=250)
    created_date = db.DateTimeField(required=True, default=datetime.utcnow, db_field='created_date')
    expiration_date = db.DateTimeField(required=True, db_field='expiration_date')
    meta = {'collection': 'blacklisted_tokens'}

def drop_all():
    for user in Users.objects:
        user.delete()
    for role in Roles.objects:
        role.delete()

def create_all():
    preset_roles = ['admin', 'editor', 'reader']
    k = 0
    for role in preset_roles:
        try:
            Roles(key=k, role=role).save()
            k += 1
        except(NotUniqueError):
            pass