import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.channels import channels_create_v2

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
    is_public = bool(data['is_public'])

    channel_id = channels_create_v2(token, name, is_public)

    return dumps (channel_id)


if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
