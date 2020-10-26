"""
 this is the doctring
"""
from os.path import join, dirname
import dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
from verminbot import Verminbot
from HTMLStrings import HTMLStrings

MESSAGES_RECEIVED_CHANNEL = "messages received"

APP = flask.Flask(__name__)

SOCKETIO = flask_socketio.SocketIO(APP)
SOCKETIO.init_app(APP, cors_allowed_origins="*")

try:
    DOTENV_PATH = join(dirname(__file__), "sql.env")
    dotenv.load_dotenv(DOTENV_PATH)
except ImportError as error:
    print("Handled error: " + str(error))

DATABASE_URI = os.environ["DATABASE_URL"]

APP.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

DB = flask_sqlalchemy.SQLAlchemy(APP)
DB.init_app(APP)
DB.app = APP

DB.create_all()
DB.session.commit()

import tables

# list of current users
USER_INDEX = {}
BOT = Verminbot()
HTML_WRITER = HTMLStrings()
BOT_PIC = "https://cdn-images-1.medium.com/max/800/1*ktXRqt9UHhJf3miHG3zpvQ.png"
BOT_SIGN = "@VERMINBOT"


def emit_all_messages(channel):

    all_messages = []
    all_signs_log = []
    all_pics = []

    for db_message, db_user, db_pic in (
            DB.session.query(
                tables.Chat_log.content, tables.Chat_log.user, tables.Chat_log.pictureURL
            )
            .order_by(tables.Chat_log.id.desc())
            .limit(50)
            .all()
        ):
        all_messages.append(db_message)
        all_signs_log.append(db_user)
        all_pics.append(db_pic)
    all_chat = []
    HTML_WRITER.formatHTML(all_messages)
    for i in range(0, len(all_messages)):
        all_chat.append([all_messages[i], all_signs_log[i], all_pics[i]])

    SOCKETIO.emit(channel, {"allMessages": all_chat})


@SOCKETIO.on("new message input")
def on_new_message(data):
    name, picture_url = (
        DB.session.query(tables.AuthUser.name, tables.AuthUser.pictureURL)
        .filter(tables.AuthUser.email == USER_INDEX[flask.request.sid])
        .first()
    )
    sign = "Sent by: " + name
    print("Got an event for new message input with data:", data, sign)
    message_content = data["message"].strip()

    # commit to DB and update everyone's chat
    DB.session.add(tables.Chat_log(data["message"], sign, picture_url))
    DB.session.commit()
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

    # if bot command (first two chars are !!)
    if message_content[0] == "!" and message_content[1] == "!":
        bot_ret_str = BOT.handle_command(message_content[2:])
        DB.session.add(tables.Chat_log(bot_ret_str, BOT_PIC, BOT_SIGN))
        DB.session.commit()
        emit_all_messages(MESSAGES_RECEIVED_CHANNEL)


@APP.route("/")
def index():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    return flask.render_template("index.html")


@SOCKETIO.on("new google user")
def on_new_google_login(data):
    sid = flask.request.sid
    USER_INDEX[sid] = data["email"]

    print("Someone logged in with data: " + str(data) + "\nauth user list:")

    for user in USER_INDEX:
        print(user + " : " + USER_INDEX[user])

    SOCKETIO.emit("updateUsers", {"user_count": len(USER_INDEX)})

    try:
        DB.session.add(
            tables.AuthUser(
                data["name"], tables.AuthUserType.GOOGLE, data["email"], data["picture"]
            )
        )
        DB.session.commit()
    except:  # email already exists in the DB
        pass


@SOCKETIO.on("connect")
def on_connect():
    sid = flask.request.sid
    print("Someone connected with sid: " + sid + "\nauth user list:")
    for user in USER_INDEX:
        print(user + " : " + USER_INDEX[user])

    SOCKETIO.emit("connected", {"test": "Connected"})

    SOCKETIO.emit("updateUsers", {"user_count": len(USER_INDEX)})

    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)


@SOCKETIO.on("disconnect")
def on_disconnect():
    sid = flask.request.sid
    USER_INDEX.pop(sid)
    print("Someone disconnected with sid: " + sid + "\nauth user list:")
    for user in USER_INDEX:
        print(user + " : " + USER_INDEX[user])
    SOCKETIO.emit("updateUsers", {"user_count": len(USER_INDEX)})


if __name__ == "__main__":
    SOCKETIO.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
