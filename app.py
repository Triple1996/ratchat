# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import chat_tables
import requests
import json 

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
    all_signs_log = []
    
    for db_message,db_user in db.session.query(chat_tables.Chat_log.content, chat_tables.Chat_log.user).all():
        all_messages.append(db_message)
        all_signs_log.append(db_user)
        
    socketio.emit(channel, {
        'allMessages': all_messages,
        'allSigns': all_signs_log
    })
    
    
def handle_bot(messageContent):
    cleanInput=str(messageContent).strip()
    sign = "-Verminbot"
    print("Got an event for new message input with data:", messageContent, " from ", sign)
    
    botRetStr = "~/ "
    
    if (cleanInput[0:5]=="about"):
        botRetStr+="I am the Verminlord."
        
    elif (cleanInput[0:4]=="help"):
        botRetStr+="\nCommands:" + \
            "\t!!about\t!!help\t!!mandalore <text>\t!!1337 <text>"

    elif (cleanInput[0:9]=="mandalore"):
        reqResponse = requests.get('https://api.funtranslations.com/translate/mandalorian.json?text="'+cleanInput[9:].strip()+'"').json()
        print(reqResponse)
        
        try:
            botRetStr+=reqResponse['contents']['translated']
        except KeyError:
            botRetStr+="Too many translations, try again later"
        except:
            botRetStr+=reqResponse['error']['message']
        
    elif (cleanInput[0:4]=="1337"):
        leetTranslation = cleanInput[4:].lower()
        
        translations = {
            'o':'0',
            't':'7',
            'l':'1',
            'e':'3',
            'a':'4',
            's':'5'    }
            
        for key in translations:
            leetTranslation = leetTranslation.replace(key, translations[key])

        botRetStr+=str(leetTranslation)
        
    elif (cleanInput=="other 2"):
        botRetStr+="Unimplemented feature 2"
    else:
        botRetStr+="That command was unrecognized. For a list of commands, type !!help"
        
    db.session.add(chat_tables.Chat_log(botRetStr, sign));
    db.session.commit();
    
    
    print(botRetStr)
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    
@socketio.on('new message input')
def on_new_message(data):
    sign = "Sent by user: " + str(userIndex[flask.request.sid])
    print("Got an event for new message input with data:", data, " from ", sign)
    messageContent = data["message"].strip()
    
    db.session.add(chat_tables.Chat_log(data["message"], sign));
    db.session.commit();
    
    # update everyone's chat
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    
    # if bot command (first two chars are !!)
    if (messageContent[0] == '!' and messageContent[1] == '!'):
        handle_bot(messageContent[2:])
        
    

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
