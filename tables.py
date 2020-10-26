# pylint: disable=missing-docstring
from app import DB
from enum import Enum


class ChatLog(DB.Model):
    # pylint: disable=too-few-public-methods
    # pylint: disable=no-member
    id = DB.Column(DB.Integer, primary_key=True)
    content = DB.Column(DB.String(200))
    user = DB.Column(DB.String(120))
    picture_url = DB.Column(DB.String(200))

    def __init__(self, content, user, picture_url):
        self.content = content
        self.user = user
        self.picture_url = picture_url

    def __repr__(self):
        return "<Message content: %s>" % self.content


class AuthUser(DB.Model):
    # pylint: disable=too-few-public-methods
    # pylint: disable=no-member
    id = DB.Column(DB.Integer, primary_key=True)
    auth_type = DB.Column(DB.String(120))
    name = DB.Column(DB.String(120))
    email = DB.Column(DB.String(120), unique=True)
    picture_url = DB.Column(DB.String(200))

    def __init__(self, name, auth_type, email, picture_url):
        assert type(auth_type) is AuthUserType
        self.name = name
        self.auth_type = auth_type.value
        self.email = email
        self.picture_url = picture_url

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
