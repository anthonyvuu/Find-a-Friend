from flask import Flask, request, jsonify, g, session
from flask_cors import CORS, cross_origin
import json
from database.setup_db import *
from database.hobbies import *
from database.chat import *
from database.auth import *
from database.friends import *
from database.images import *
from database.friendRequests import *
import pusher

#oppsett av pusher
pusher_client = pusher.Pusher(
    app_id='1203264',
    key='d03450301bfcf65bbaeb',
    secret='f0af54257a38ea91ac6c',
    cluster='eu',
    ssl=True
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "some_secret"
CORS(app, resources={r'/*': {'origins': '*'}})
ALLOWED_IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]
ALLOWED_FILE_EXTENSIONS = ["pdf", "txt", "zip", "docx", "rtf"]


def get_db():
    if not hasattr(g, "_database"):
        print("create connection")
        g._database = sqlite3.connect("database.db")
    return g._database

def valid_login(email, password):
    conn = get_db()
    hash = get_hash_for_login(conn, email)
    if hash != None:
        return check_password_hash(hash, password)


def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

@ app.route('/')
def index():
    return "Hello, cross-orogin"


@app.route('/auth', methods=["POST"])
def authorize():
    data = json.loads(request.data)
    conn = get_db()

    if(data['type'] == 'login'):

        if not valid_login(data['email'], data['password']):
            response_object_error = {
                'ok': 'false',
                'message': 'Login feilet, ugyldig brukernavn eller passord'
            }
            return jsonify(response_object_error)
        else:

            id = get_id_by_email(conn, data['email'])

            return jsonify(id)
    else:
        useradded = add_user(conn, data['email'], data['password'])

        return jsonify(useradded)

#FRIENDS alle registrerte friends
@app.route('/friends', methods=["GET"])
def getFriends():

    conn = get_db()

    friends = get_friends(conn)

    for friend in friends:
        hobbies = get_hobbies_for_friendId(conn, friend['friendId'])
        friend['hobbies'] = hobbies

    return json.dumps(friends)

@app.route('/friends/<friend_id>', methods=["PUT"])
def editFriend(friend_id):

    editFriendData = json.loads(request.data)

    conn = get_db()

    hobbies = editFriendData['hobbies']
    edit_friend(conn, editFriendData['description'],
                editFriendData['image'], friend_id)
    delete_hobbies_friendId(conn, friend_id)

    for hobby in hobbies:
        add_friend_hobby(conn, friend_id, hobby)

    return jsonify("ok")


@app.route('/friends', methods=["POST"])
def addFriend():

    friend = json.loads(request.data)
    hobbies = friend['hobbies']

    conn = get_db()

    friendAdded = add_friend(
        conn, friend['friendId'], friend['firstName'], friend['lastName'], friend['description'],  friend['image'])

    if friendAdded == -1:
        response_object_error = {
            'ok': 'false',
            'message': 'Firstname er i allerede i bruk, bruk et annet'
        }
        return jsonify(response_object_error)

    else:
        for hobby in hobbies:
            add_friend_hobby(conn, friend['friendId'], hobby)

        response_object_success = {
            'ok': 'true',
            'message': 'Registrert fullført'
        }

        return jsonify(response_object_success)

#myFriends , brukere som man er venn med 

@app.route('/myfriends/<friend_id>', methods=["GET"])
def getMyFriends(friend_id):

    conn = get_db()

    myFriends = get_friendWith(conn, friend_id)

    return json.dumps(myFriends)


@app.route('/myfriends', methods=["POST"])
def friendAccpeted():

    data = json.loads(request.data)
    conn = get_db()

    add_friendWith(conn, data["friendId"], data["friendWith"])
    add_friendWith(conn, data["friendWith"], data["friendId"])
    delete_friend_request(conn, data["friendId"], data["friendWith"])
    delete_friend_request(conn, data["friendWith"], data["friendId"])

    return jsonify("ok")


@app.route('/myfriends', methods=["DELETE"])
def friendDeclined():

    data = json.loads(request.data)
    conn = get_db()

    delete_friend_request(conn, data["friendWith"], data["friendId"])

    return jsonify("ok")

#friendREQUESTS

@app.route('/requests/<friend_id>', methods=["GET"])
def getRequests(friend_id):
    conn = get_db()

    requests = get_requests_for_friendId(conn, friend_id)

    return json.dumps(requests)


@app.route('/requests', methods=["POST"])
def addRequest():
    conn = get_db()

    data = json.loads(request.data)

    result = send_friend_request(conn, data['friendId'], data['requesttoId'])

    if result == None:
        pusher_client.trigger(data['requesttoId'], 'new-request', "test")
        return jsonify({"ok": "true"})
    else:
        return jsonify(result)

#HOBBIES

@app.route('/hobbies', methods=["GET"])
def getHobbies():

    conn = get_db()

    hobbies = get_hobbies(conn)

    return json.dumps(hobbies)


@app.route('/hobbies', methods=["POST"])
def newHobby():

    conn = get_db()

    data = json.loads(request.data)
    added = add_hobby(conn, data['hobby'])

    return jsonify(added)

#gallery IMAGES

@app.route('/images', methods=["POST"])
def uploadImage():

    conn = get_db()

    imageData = json.loads(request.data)

    if allowed_file(imageData['filename'], ALLOWED_IMAGE_EXTENSIONS):
        add_image(conn, imageData['friendId'], imageData['image'])
        return jsonify("ok")
    else:
        error_msg = {
            "ok": "false",
            "message": "Bilde Formatet må være i (.jpeg/.png/.jpg/.gif)"
        }
        return jsonify(error_msg)

@app.route('/images/<image_id>', methods=["DELETE"])
def deleteImage(image_id):
    conn = get_db()
    delete_image(conn, image_id)
    return jsonify("ok")

@app.route("/images/<friend_id>", methods=["GET"])
def getImage(friend_id):

    conn = get_db()

    result = get_image_for_friendId(conn, friend_id)

    return json.dumps(result)


#CHAT

@app.route("/chat", methods=["POST"])
def send_message():
    conn = get_db()
    data = json.loads(request.data)

    isAttachment = data['isAttachment']

    channel = list(data['channel'])
    pusher_client.trigger(channel[0], 'notification', channel[1])
    pusher_client.trigger(channel[1], 'notification', channel[0])

    # skjekker om chat meldingen som sender er attachment, også skjekker om attachment er et bilde eller en fil og i riktig format som er tillat. 
    if isAttachment:
        if allowed_file(data['message']['fileName'], ALLOWED_IMAGE_EXTENSIONS):
            add_chatmessage(conn, data['channel'], True,
                            False, data['firstName'], data['message']['fileData'], data['message']['fileName'], data['date'])
            pusher_client.trigger(data['channel'], 'new-message', "image")
        elif allowed_file(data['message']['fileName'], ALLOWED_FILE_EXTENSIONS):
            add_chatmessage(conn, data['channel'],  False,
                            True, data['firstName'], data['message']['fileData'], data['message']['fileName'], data['date'])
            pusher_client.trigger(data['channel'], 'new-message', "file")
        else:
            err_msg = {
                "ok" : "false",
                "message" : "Filtypen må være av typen png/jpeg/jpg/gif/pdf/txt/zip/docx/rtf"
            }
            return jsonify(err_msg)
    else:
        add_chatmessage(conn, data['channel'], False,
                        False, data['firstName'], data['message'], "null" ,data['date'])
        pusher_client.trigger(data['channel'], 'new-message', "message")

    return jsonify("ok")


@app.route("/chat/<channel_id>", methods=["GET"])
def get_messages(channel_id):

    conn = get_db()

    messages = get_chatmessage_for_channel(conn, channel_id)

    return json.dumps(messages)


if __name__ == "__main__":
    app.run(debug=True)
