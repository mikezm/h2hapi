from app.main.database import db
from datetime import datetime
from bson.objectid import ObjectId

class Users(db.Document):
    public_id = db.ObjectIdField(required=True, unique=True, default=ObjectId())
    email = db.EmailField(required=True, unique=True, db_field='email')
    password = db.StringField(required=True, db_field='password')
    first_name = db.StringField(max_length=50, db_field='first_name')
    last_name = db.StringField(max_length=50, db_field='last_name')
    role = db.StringField(max_length=50, default='reader', db_field='role')
    active = db.BooleanField(default=False, db_field='active')
    deactivated = db.BooleanField(default=False, db_field='deactivated')
    created_date = db.DateTimeField(default=datetime.utcnow, db_field='created_date')
    updated_date = db.DateTimeField(default=datetime.utcnow, db_field='modified_date')
    deactivated_date = db.DateTimeField(default=None, db_field='deactivation_date')




