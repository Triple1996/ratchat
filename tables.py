import flask_sqlalchemy
from app import db


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120))
    
    def __init__(self, a):
        self.content = a
    
    def __repr__(self):
        return '<Message content: %s>' % self.content
