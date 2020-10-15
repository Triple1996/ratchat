# models.py
import flask_sqlalchemy
from app import db
from enum import Enum

class AuthUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_type = db.Column(db.String(120))
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    
    def __init__(self, name, auth_type, email):
        assert type(auth_type) is AuthUserType
        self.name = name
        self.auth_type = auth_type.value
        self.email = email
        
    def __repr__(self):
        return "<User name: {}\ntype: {}".format(self.name, self.auth_type)

class AuthUserType(Enum):
    LINKEDIN = "linkedin"
    GOOGLE = "google"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    GITHUB = "github"
    PASSWORD = "password"