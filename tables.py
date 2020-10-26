import flask_sqlalchemy
from app import DB
from enum import Enum

class Chat_log(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    content = DB.Column(DB.String(200))
    user = DB.Column(DB.String(120))
    pictureURL = DB.Column(DB.String(200))
    
    def __init__(self, content, user, pictureURL):
        self.content = content
        self.user = user
        self.pictureURL = pictureURL
        
    def __repr__(self):
        return '<Message content: %s>' % self.content

class AuthUser(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    auth_type = DB.Column(DB.String(120))
    name = DB.Column(DB.String(120))
    email = DB.Column(DB.String(120), unique=True)
    pictureURL = DB.Column(DB.String(200))
    
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
