import hmac
import sqlite3

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message


class Users(object):
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email


class Beat(object):
    def __init__(self, beat_name, beat_type, beat_tempo):
        self.beat_name = beat_name
        self.beat_type = beat_type
        self.beat_tempo = beat_tempo


def usertable():
    conn = sqlite3.connect('Store.db')
    print("DB opened")

    conn.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "username TEXT NOT NULL,"
                 "password TEXT NOT NULL,"
                 "email TEXT NOT NULL,")
    print("Table created")
    conn.close()


usertable()


def get_users():
    with sqlite3.connect('Store.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        user = cursor.fetchall()

        user_data = []

        for data in user:
            user_data.append(Users(data[0], data[1], data[2], data[3]))
        return user_data


user = get_users()


def beats_table():
    with sqlite3.connect('Store.db') as conn:
        conn.execute("CREATE TABLE IS NOT EXISTS beats (beat_name TEXT NOT NULL,"
                     "beat_type TEXT NOT NULL,"
                     "beat_tempo TEXT NOT NULL,")
        print("beat table created")


beats_table()


def get_beats():
    with sqlite3.connect('Store.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM beats")
        beats = cursor.fetchall()

        beat_data = []

        for data in beats:
            beat_data.append(Beat(data[0], data[1], data[2]))
    return beat_data


beats = beats_table()

# username_table = {u.username: u for u in user}
# userid_table = {u.id: u for u in user}
#
#
# def authenticate(username, password):
#     user = username_table.get(username, None)
#     if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
#         return user
#
#
# def identity(payload):
#     id = payload['identify']
#     return userid_table.get(id, None)


app = Flask(__name__)

CORS(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'zaidflandorp4@gmail.com'
app.config['MAIL_PASSWORD'] = 'xxxtentacion_17'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/register/', methods=["Post"])
def registration():
    response = {}

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        with sqlite3.connect('Store.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users("
                           "username,"
                           "password,"
                           "email) VALUES(?, ?, ?)", (username, password, email))
            conn.commit()
            response["message"] = "success"
            response["status_code"] = 201

        msg = Message('Hello Message', sender='zaidflandorp4@gamil.com', recipients=[email])
        msg.body = "My email using Flask"
        mail.send(msg)
        return "Message send"
    return response
