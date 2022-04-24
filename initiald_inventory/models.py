import imp
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
import sqlalchemy

#adding Flask secutiy passwords
from werkzeug.security import generate_password_hash, check_password_hash

#import for secrets module
import secrets

#import for login manager
from flask_login import UserMixin

#import for lfask login
from flask_login import LoginManager

#marshmello
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#make sure to add usermixin
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    initiald = db.relationship('Initiald', backref = 'owner', lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database!'


class Initiald(db.Model):
    id = db.Column(db.String, primary_key =True)
    name = db.Column(db.String(1500))
    description = db.Column(db.String(2000), nullable = True)
    model = db.Column(db.String(2000), nullable = True)
    year = db.Column(db.String(1500), nullable = True)
    engine = db.Column(db.String(1000), nullable = True)
    max_speed = db.Column(db.String(1000))
    owners = db.Column(db.String(1000))
    weight = db.Column(db.String(1000))
    spec_version = db.Column(db.String(1000))
    series = db.Column(db.String(1500))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, model, year, engine, max_speed, owners, weight, spec_version, series, user_token, id =''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.model = model
        self.year = year
        self.engine = engine
        self.max_speed = max_speed
        self.owners = owners
        self.weight = weight
        self.spec_version = spec_version
        self.series = series
        self.user_token = user_token

    def __repr__(self):
        return f"The following car has been added: (self.name)"

    def set_id(self):
        return (secrets.token_urlsafe())

#creation of API Schema via marshmallow object
class initialdSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description','model', 'year', 'engine', 'max_speed', 'owners', 'weight', 'spec_version', 'series']
initiald_schema = initialdSchema()
initialds_schema = initialdSchema(many = True)