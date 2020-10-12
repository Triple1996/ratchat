# app.py
from os.path import join, dirname
import dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import chat_tables
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
user_list = []
userIndex = {}
bot = Verminbot()


def emit_all_messages(channel):

    all_messages = []
    all_signs_log = []
    
    for db_message,db_user in db.session.query(chat_tables.Chat_log.content, chat_tables.Chat_log.user).order_by(chat_tables.Chat_log.id.desc()).limit(50).all():
        all_messages.append(db_message)
        all_signs_log.append(db_user)
    
    all_chat = []
    for i in range(0,len(all_messages)):
        all_chat.append([all_messages[i], all_signs_log[i]])
    
    socketio.emit(channel, {
        'allMessages': all_chat
    })
    
def randomName():
    adjList = ['salty', 'greasy', 'slimy', 'shriveled', 'cracked', 'degenerate', 'decayed', 'washed-up', 'overripe', 'treasonous', 'ornery']
    nounList = ['dog', 'seamonkey', 'babboon', 'degen', 'decadent', 'debaucher', 'deviate', 'weeb', 'heathen']
    adj = random.choice(adjList)
    noun = random.choice(nounList)
    randName = adj + '-' + noun
    return randName
    
@socketio.on('new message input')
def on_new_message(data):
    sign = "Sent by: " + str(userIndex[flask.request.sid])
    print("Got an event for new message input with data:", data, sign)
    messageContent = data["message"].strip()
    
    # commit to DB and update everyone's chat
    db.session.add(chat_tables.Chat_log(data["message"], sign));
    db.session.commit();
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    
    # if bot command (first two chars are !!)
    if (messageContent[0] == '!' and messageContent[1] == '!'):
        botRetStr = bot.handle_command(messageContent[2:])
        botSign='@VERMINBOT'
        db.session.add(chat_tables.Chat_log(botRetStr, botSign));
        db.session.commit();
        emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
        
@app.route('/')
def index():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    return flask.render_template("index.html")


@socketio.on('connect')
def on_connect():
    sid = flask.request.sid
    user_list.append(sid)
    userId = randomName()
    userIndex[sid] = userId
    print('Someone connected with sid: ' + sid + "\t user list:\n" + str(userIndex) )
    socketio.emit('connected', {
        'test': 'Connected'
    })
    
    socketio.emit('updateUsers', {
        'user_count': len(user_list)
    })
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    sid = flask.request.sid
    user_list.remove(sid)
    print ('Someone disconnected!')
    socketio.emit('updateUsers', {
        'user_count': len(user_list)
    })
    
if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
