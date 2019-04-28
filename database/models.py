from database import db
from mongoengine.errors import NotUniqueError
from datetime import datetime

#from flask_mongoengine.wtf import model_form

class Users(db.Document):
    email = db.EmailField(required=True, unique=True, db_field='email')
    password = db.StringField(required=True, db_field='password')
    first_name = db.StringField(max_length=50, db_field='first_name')
    last_name = db.StringField(max_length=50, db_field='last_name')
    role = db.StringField(max_length=50, default='reader', db_field='role')
    active = db.BooleanField(default=False, db_field='active')
    created_date = db.DateTimeField(default=datetime.utcnow, db_field='created_date')
    updated_date = db.DateTimeField(default=datetime.utcnow, db_field='modified_date')

class Roles(db.Document):
    key = db.IntField(required=True, unique=True, db_field='key')
    role = db.StringField(required=True, unique=True, db_field='role')

# database initializations
def init_roles():
    # add Roles
    preset_roles = ['admin', 'editor', 'user']
    k = 1
    for role in preset_roles:
        try:
            Roles(key=k, role=role).save()
        except(NotUniqueError):
            pass



