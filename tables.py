import flask_sqlalchemy
from app import db
from enum import Enum

class Chat_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120))
    user = db.Column(db.String(120))
    pictureURL = db.Column(db.String(240))
    
    def __init__(self, content, user, pictureURL):
        self.content = content
        self.user = user
        self.pictureURL = pictureURL
        
    def __repr__(self):
        return '<Message content: %s>' % self.content

class AuthUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_type = db.Column(db.String(120))
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    pictureURL = db.Column(db.String(240))
    
    def __init__(self, name, auth_type, email, pictureURL):
        assert type(auth_type) is AuthUserType
        self.name = name
        self.auth_type = auth_type.value
        self.email = email
        self.pictureURL = pictureURL
        
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