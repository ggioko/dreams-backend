import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_register_v2
from src.channel import channel_details_v2

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

@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    """
    Gets user data from http json and passes it to the
    channel_details_v2 function
    Passes in (token, channel_id)
    Returns dictionary containing basic details of specified channel on success.
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    
    data = channel_details_v2(token, channel_id)
    
    return dumps(data)
    
    

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
