import hmac
import sqlite3

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
import cloudinary
import cloudinary.uploader


class Users(object):
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email


class Beat(object):
    def __init__(self, id, beat_name, beat_type, beat_tempo, image, producer):
        self.id = id
        self.beat_name = beat_name
        self.beat_type = beat_type
        self.beat_tempo = beat_tempo
        self.image = image
        self.producer = producer


def usertable():
    conn = sqlite3.connect('Store.db')
    print("DB opened")

    conn.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "username TEXT NOT NULL,"
                 "password TEXT NOT NULL,"
                 "email TEXT NOT NULL)")
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
        conn.execute("CREATE TABLE IF NOT EXISTS beats (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "beat_name TEXT NOT NULL,"
                     "beat_type TEXT NOT NULL,"
                     "beat_tempo TEXT NOT NULL,"
                     "image TEXT NOT NULL,"
                     "producer TEXT NOT NULL)")
        print("beat table created")


beats_table()


def get_beats():
    with sqlite3.connect('Store.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM beats")
        beat = cursor.fetchall()

        beat_data = []

        for data in beat:
            beat_data.append(Beat(data[0], data[1], data[2], data[3], data[4], data[5]))
    return beat_data


beats_table()


def image_convert():
    app.logger.info('in upload route')
    cloudinary.config(cloud_name="dh7g4uw8x",
                      api_key="848147445884154",
                      api_secret="HwbSS8r41xhx6tYhQ_KC7TulLL4")
    upload_result = None
    if request.method == 'POST' or request.method == 'PUT':
        beat_img = request.files['image']
        app.logger.info('%s file_to_upload', beat_img)
        if beat_img:
            upload_result = cloudinary.uploader.upload(beat_img)
            app.logger.info(upload_result)
            return upload_result['url']

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


@app.route('/create-beat/', methods=["POST"])
def create_beat():
    response = {}

    if request.method == "POST":
        beat_name = request.form['beat_name']
        beat_type = request.form['beat_type']
        beat_tempo = request.form['beat_tempo']
        beat_img = image_convert()
        producer = request.form['producer']

        with sqlite3.connect('Store.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO beats("
                           "id"
                           "beat_name,"
                           "beat_type,"
                           "beat_tempo,"
                           "image,"
                           "producer) VALUES(?, ?, ?, ?, ?, ?)", (id, beat_name, beat_type, beat_tempo, beat_img, producer))
            conn.commit()
            response["message"] = "success"
            response["status_code"] = 201
        return response


@app.route('/display-users/', methods=["GET"])
def get_users():
    response = {}
    with sqlite3.connect("Store.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")

        posts = cursor.fetchall()

    response['status_code'] = 200
    response['data'] = posts
    return response


@app.route('/display-beats/', methods=["GET"])
def get_blogs():
    response = {}
    with sqlite3.connect("Store.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM beats")

        posts = cursor.fetchall()

    response['status_code'] = 200
    response['data'] = posts
    return jsonify(response)


@app.route("/delete-beat/<int:id>")
def delete_post(id):
    response = {}
    with sqlite3.connect("Store.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM beats WHERE id=" + str(id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "beat deleted successfully."
        return response


@app.route('/edit-post/<int:id>/', methods=["PUT"])
def edit_post(id):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect('Store.db') as conn:
            beat_name = request.form['beat_name']
            beat_type = request.form['beat_type']
            beat_tempo = request.form['beat_tempo']
            beat_img = request.files['beat_img']
            producer = request.form['producer']
            put_data = {}

            if beat_name is not None:
                put_data["beat_name"] = beat_name
                cursor = conn.cursor()
                cursor.execute("UPDATE beats SET beat_name =? WHERE id=?", (put_data["beat_name"], id))
                conn.commit()
                response['message'] = "Update was successfully"
                response['status_code'] = 200
            if beat_type is not None:
                put_data['beat_type'] = beat_type
                cursor = conn.cursor()
                cursor.execute("UPDATE beats SET beat_type =? WHERE id=?", (put_data["beat_type"], id))
                conn.commit()
                response["beat_type"] = "Content updated successfully"
                response["status_code"] = 200
            if beat_tempo is not None:
                put_data['beat_tempo'] = beat_tempo
                cursor = conn.cursor()
                cursor.execute("UPDATE beats SET beat_tempo =? WHERE id=?", (put_data["beat_tempo"], id))
                conn.commit()
                response["beat_tempo"] = "Content updated successfully"
                response["status_code"] = 200
            if beat_img is not None:
                put_data['beat_img'] = image_convert()
                cursor = conn.cursor()
                cursor.execute("UPDATE beats SET beat_img =? WHERE id=?", (put_data["beat_img"], id))
                conn.commit()
                response["beat_img"] = "Content updated successfully"
                response["status_code"] = 200
            if producer is not None:
                put_data['producer'] = producer
                cursor = conn.cursor()
                cursor.execute("UPDATE beats SET producer =? WHERE id=?", (put_data["producer"], id))
                conn.commit()
                response["producer"] = "Content updated successfully"
                response["status_code"] = 200
    return response


if __name__ == "__main__":
    app.run(debug=True)
