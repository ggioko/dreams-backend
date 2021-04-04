import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_login_v2, auth_register_v2, auth_logout_v1
from src.channels import channels_create_v2
from src.channel import channel_join_v2, channel_messages_v2
from src.other import clear_v1

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/channels/create/v2", methods=['POST'])
def channels_create():
    """
    Gets user data from http json and passes it to the
    channels_register_v2 function

    Returns { 'channel_id': channel_id,} on success

    """
    data = request.get_json()

    token = data['token']
    name = data['name']
    is_public = data['is_public']

    response = channels_create_v2(token, name, is_public)

    return dumps (response)

@APP.route("/auth/login/v2", methods=["POST"])
def login_user():
    """
    Gets user data from http json and passes it to the
    auth_login_v2 function

    Returns {'token': token, 'auth_user_id': id,} on success
    """
    data = request.get_json()
    email = data["email"]
    password = data["password"]
   
    data = auth_login_v2(email, password)

    return dumps({
        'token' : data['token'],
        'auth_user_id' : data['auth_user_id']
    })

@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    """
    Function to call clear_v1
    """
    clear_v1()
    return dumps({})

@APP.route("/auth/register/v2", methods=['POST'])
def register():
    """
    Gets user data from http json and passes it to the
    auth_register_v2 function

    Returns {'token' : token, 'auth_user_id': id} on success

    """
    data = request.get_json()
    email = data['email']
    password = data['password']
    name_first = data['name_first']
    name_last = data['name_last']

    data = auth_register_v2(email,password,name_first,name_last)

    return dumps({
        'token' : data['token'],
        'auth_user_id' : data['auth_user_id']
    })

@APP.route("/auth/logout/v1", methods=["POST"])
def logout_user():
    """
    Gets user data from http json and passes it to the
    auth_logout_v1 function

    Returns {'is_success': True} on successful logout
    """
    data = request.get_json()
    token = data['token']
    result = auth_logout_v1(token)

    return dumps({
        'is_success': result
    })

@APP.route("/channel/join/v2", methods=["POST"])
def channel_join():
    """ 
    Gets user data from http json and passes it to the
    channel_join_v2 function

    Returns {} - an empty dictionary
    """
    data = request.get_json()

    token = data['token']
    channel_id = data['channel_id']
 
    channel_join_v2(token, channel_id)

    return dumps({})

@APP.route("/channel/messages/v2", methods=["GET"])
def channel_messages():
    """ 
    Gets user data from http json and passes it to the
    channel_messages_v2 function

    Returns { 'messages': messages, 'start': start, 'end': end }
    """
    data = request.get_json
    
    token = data['token']
    channel_id = data['channel_id']
    start = data['start']

    data = channel_messages_v2(token, channel_id, start)

    return dumps({
        'messages': data['messages'],
        'start': data['start'],
        'end': data['end']
    })
    
if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
