# import hmac
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
    def __init__(self, id, beat_name, beat_type, beat_tempo, image, producer, price):
        self.id = id
        self.beat_name = beat_name
        self.beat_type = beat_type
        self.beat_tempo = beat_tempo
        self.image = image
        self.producer = producer
        self.price = price


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
                     "producer TEXT NOT NULL,"
                     "price INTEGER NOT NULL)")
        print("beat table created")


beats_table()


def get_beats():
    with sqlite3.connect('Store.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM beats")
        beat = cursor.fetchall()

        beat_data = []

        for data in beat:
            beat_data.append(Beat(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
    return beat_data


beats_table()


def image_convert():
    app.logger.info('in upload route')
    cloudinary.config(cloud_name="dh7g4uw8x",
                      api_key="848147445884154",
                      api_secret="HwbSS8r41xhx6tYhQ_KC7TulLL4")
    upload_result = None
    if request.method == 'POST' or request.method == 'PUT':
        picture = request.files['image']
        app.logger.info('%s file_to_upload', picture)
        if picture:
            upload_result = cloudinary.uploader.upload(picture)
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
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']

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
        image = image_convert()
        producer = request.form['producer']
        price = request.form['price']

        with sqlite3.connect('Store.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO beats("
                           "beat_name,"
                           "beat_type,"
                           "beat_tempo,"
                           "image,"
                           "producer,"
                           "price) VALUES(?, ?, ?, ?, ?, ?)", (beat_name, beat_type, beat_tempo, image, producer, price))
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
def delete_beat(id):
    response = {}
    with sqlite3.connect("Store.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM beats WHERE id=" + str(id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "beat deleted successfully."
    return response


@app.route("/delete-user/<int:id>")
def delete_user(id):
    response = {}
    with sqlite3.connect("Store.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=" + str(id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "user deleted successfully."
    return response


@app.route('/edit-beat/<int:id>/', methods=["PUT"])
def edit_post(id):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect('Store.db') as conn:
            beat_name = request.json['beat_name']
            beat_type = request.json['beat_type']
            beat_tempo = request.json['beat_tempo']
            image = request.json['image']
            producer = request.json['producer']
            price = request.json['price']
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
            if image is not None:
                put_data['image'] = image_convert()
                cursor = conn.cursor()
                cursor.execute("UPDATE beats SET image =? WHERE id=?", (put_data["image"], id))
                conn.commit()
                response["image"] = "Content updated successfully"
                response["status_code"] = 200
            if producer is not None:
                put_data['producer'] = producer
                cursor = conn.cursor()
                cursor.execute("UPDATE beats SET producer =? WHERE id=?", (put_data["producer"], id))
                conn.commit()
                response["producer"] = "Content updated successfully"
                response["status_code"] = 200
            if producer is not None:
                put_data['price'] = producer
                cursor = conn.cursor()
                cursor.execute("UPDATE beats SET price =? WHERE id=?", (put_data["price"], id))
                conn.commit()
                response["price"] = "Content updated successfully"
                response["status_code"] = 200

    return response


@app.route('/login/', methods=["PATCH"])
def log():
    response = {}

    if request.method == 'PATCH':
        username = request.json['username']
        password = request.json['password']

        with sqlite3.connect('Store.db') as conn:
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute('SELECT FROM users WHERE username=? and password=?', (username, password))
            user = cursor.fetchall()
            data = []

            for a in user:
                data.append({u: a[u] for u in a.keys()})

        response['data'] = data
        response['status_code'] = 200
        response['message'] = "Data collected"

    return response


if __name__ == "__main__":
    app.run(debug=True)
