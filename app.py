# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import chat_tables

MESSAGES_RECEIVED_CHANNEL = 'messages received'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

dbuser = os.environ['USER']

database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

# list of current users 
user_list = []
userIndex = {}
userId = 0

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()
db.session.commit()

def emit_all_messages(channel):

    all_messages = []
    all_users_log = []
    
    for db_message,db_user in db.session.query(chat_tables.Chat_log.content, chat_tables.Chat_log.user).all():
        all_messages.append(db_message)
        all_users_log.append(db_user)
        
    socketio.emit(channel, {
        'allMessages': all_messages,
        'allUsers': all_users_log
    })
    
    
def handle_bot(messageContent):
    botStr = "## "
    name = "-Verminbot"
    print("Got an event for new message input with data:", messageContent, " from ", name)
    
    db.session.add(chat_tables.Chat_log(botStr, name));
    db.session.commit();
        
    print(botStr)
    
@socketio.on('new message input')
def on_new_message(data):
    name = "Sent by user: " + str(userIndex[flask.request.sid])
    print("Got an event for new message input with data:", data, " from ", name)
    messageContent = data["message"]
    
    db.session.add(chat_tables.Chat_log(data["message"], name));
    db.session.commit();
    
    if (messageContent[0] == '!' and messageContent[1] == '!'):
        handle_bot(messageContent[2:])
        
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

@app.route('/')
def index():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

    return flask.render_template("index.html")

@socketio.on('connect')
def on_connect():
    sid = flask.request.sid
    user_list.append(sid)
    global userId
    userId+=1
    userIndex[sid] = userId
    print('Someone connected with sid: ' + sid + "\t user list:\n" + str(user_list) )
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
