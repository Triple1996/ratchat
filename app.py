# app.py
from os.path import join, dirname
import dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import tables
import requests
import json 
import random
from verminbot import Verminbot

MESSAGES_RECEIVED_CHANNEL = 'messages received'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

try:
    dotenv_path = join(dirname(__file__), 'sql.env')
    dotenv.load_dotenv(dotenv_path)
except Exception as e: 
    print("Handled error: " +  str(e))
    
database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()
db.session.commit()

# list of current users 
userIndex = {}
bot = Verminbot()
botPic = 'https://cdn-images-1.medium.com/max/800/1*ktXRqt9UHhJf3miHG3zpvQ.png'
botSign = '@VERMINBOT'

def emit_all_messages(channel):

    all_messages = []
    all_signs_log = []
    all_pics = []
    
    for db_message,db_user,db_pic in \
            db.session.query(
                tables.Chat_log.content, tables.Chat_log.user, tables.Chat_log.pictureURL) \
            .order_by(tables.Chat_log.id.desc()).limit(50).all():
        all_messages.append(db_message)
        all_signs_log.append(db_user)
        all_pics.append(db_pic)
    all_chat = []
    for i in range(0,len(all_messages)):
        all_chat.append([all_messages[i], all_signs_log[i], all_pics[i]])
    
    socketio.emit(channel, {
        'allMessages': all_chat
    })

@socketio.on('new message input')
def on_new_message(data):
    name, pictureURL = db.session.query(tables.AuthUser.name, tables.AuthUser.pictureURL).filter(tables.AuthUser.email == userIndex[flask.request.sid]).first()
    sign = "Sent by: " + name
    print("Got an event for new message input with data:", data, sign)
    messageContent = data["message"].strip()
    
    # commit to DB and update everyone's chat
    db.session.add(tables.Chat_log(data["message"], sign, pictureURL));
    db.session.commit();
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    
    # if bot command (first two chars are !!)
    if (messageContent[0] == '!' and messageContent[1] == '!'):
        botRetStr = bot.handle_command(messageContent[2:])
        db.session.add(tables.Chat_log(botRetStr, botSign, botPic))
        db.session.commit()
        emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
        
@app.route('/')
def index():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    return flask.render_template("index.html")

@socketio.on('new google user')
def on_new_google_login(data):
    sid = flask.request.sid
    userIndex[sid] = data['email']
    
    print('Someone logged in with data: ' + str(data) + 
            "\nauth user list:")
    
    for user in userIndex:    
        print(user + " : " + userIndex[user])
    
    socketio.emit('updateUsers', {
        'user_count': len(userIndex)
    })
    
    try:
        db.session.add(tables.AuthUser(data['name'], tables.AuthUserType.GOOGLE, data['email'], data['picture']))
        db.session.commit()
    except: # email already exists in the DB
        pass
@socketio.on('connect')
def on_connect():
    sid = flask.request.sid
    print('Someone connected with sid: ' + sid + 
            "\nauth user list:")
    for user in userIndex:    
        print(user + " : " + userIndex[user])
    
    socketio.emit('connected', {
        'test': 'Connected'
    })
    
    socketio.emit('updateUsers', {
        'user_count': len(userIndex)
    })
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    sid = flask.request.sid
    userIndex.pop(sid)
    print ('Someone disconnected with sid: ' + sid + 
            "\nauth user list:")
    for user in userIndex:    
        print(user + " : " + userIndex[user])
    socketio.emit('updateUsers', {
        'user_count': len(userIndex)
    })
    
if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
