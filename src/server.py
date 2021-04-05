import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_login_v2, auth_register_v2, auth_logout_v1
from src.channels import channels_create_v2, channels_listall_v2, channels_list_v2
from src.channel import channel_join_v2, channel_invite_v2, channel_messages_v2, channel_details_v2
from src.dm import dm_create_v1, dm_details_v1, dm_remove_v1, dm_invite_v1, dm_leave_v1, dm_list_v1, \
    dm_messages_v1
from src.channel import channel_addowner_v1, channel_removeowner_v1, channel_leave_v1
from src.other import clear_v1
from src.user import users_all_v1, user_profile_v2, user_profile_setemail_v2, user_profile_setname_v2, user_profile_sethandle_v1
from src.message import message_send_v2, message_remove_v1, message_edit_v2, message_share_v1, message_senddm_v1
from src.helper import save_data, load_data
from src.admin import userpermission_change_v1

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
    channels_create_v2 function

    Returns { 'channel_id': channel_id,} on success

    """
    data = request.get_json()

    token = data['token']
    name = data['name']
    is_public = data['is_public']

    response = channels_create_v2(token, name, is_public)
    
    save_data()

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

    save_data()

    return dumps({
        'token' : data['token'],
        'auth_user_id' : data['auth_user_id']
    })

@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    """
    Function to call clear_v1

    Returns {} on success
    """
    clear_v1()

    save_data()

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

    save_data()

    return dumps({
        'token' : data['token'],
        'auth_user_id' : data['auth_user_id']
    })

@APP.route("/message/send/v2", methods=['POST'])
def message_send():
    """
    Gets user data from http json and passes it to the
    message_send_v2 function

    Returns {'message_id' : id} on success

    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']

    data = message_send_v2(token, channel_id, message)

    save_data()

    return dumps(data)
    

@APP.route("/channels/listall/v2", methods=['GET'])
def listall():
    """
    Gets users data from http args and passes it to
    channels_listall_v2 function

    Returns { 'channels': [...]} on success
    """
    token = request.args.get('token')
    data = channels_listall_v2(token)

    save_data()

    return dumps(
        data
    )

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

    save_data()

    return dumps({
        'is_success': result
    })

@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    """
    Gets user data from http json and passes it to the
    channel_details_v2 function
    Passes in (token, channel_id)
    Returns dictionary containing basic details of specified channel on success.
    """
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    data = channel_details_v2(token, channel_id)

    save_data()
    
    return dumps(
        data
    )
    
@APP.route("/channel/invite/v2", methods=['POST'])
def invite_user_to_channel():
    """
    Gets input data from http json and passes it to channel_invite_v2()
    Returns {} if no errors are raised.
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    channel_invite_v2(token, channel_id, u_id)

    save_data()

    return dumps({})

@APP.route("/channel/addowner/v1", methods=["POST"])
def channel_add_owner_to_channel():
    """
    Gets input data from http json and passes it to channel_addowner_v1()
    Returns {} if no errors are raised.
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    channel_addowner_v1(token, channel_id, u_id)

    save_data()

    return dumps({})

@APP.route("/channel/removeowner/v1", methods=["POST"])
def channel_remove_owner_from_channel():
    """
    Gets input data from http json and passes it to channel_removeowner_v1()
    Returns {} if no errors are raised.
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    channel_removeowner_v1(token, channel_id, u_id)
    
    save_data()

    return dumps({})

@APP.route("/channel/leave/v1", methods=["POST"])
def channel_leave():
    """
    Gets input data from http json and passes it to channel_leave_v1()
    Returns {} if no errors are raised.
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    channel_leave_v1(token, channel_id)

    save_data()

    return dumps({})


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

    save_data()

    return dumps({})


@APP.route("/user/profile/v2", methods = ['GET'])
def user_profile():
    """
    Gets user token and u_id from http json and passes it to
    the user_profile_v2 function
    Returns {user} on success
    """
    data = request.get_json()
    token = data['token']
    u_id = data['u_id']
    data = user_profile_v2(token, u_id)

    save_data()
    
    return dumps(data)

@APP.route("/channel/messages/v2", methods=["GET"])
def channel_messages():
    """ 
    Gets user data from http json and passes it to the
    channel_messages_v2 function

    Returns { 'messages': messages, 'start': start, 'end': end }
    """
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    response = channel_messages_v2(token, channel_id, start)

    save_data()

    return dumps(response)
    
@APP.route("/users/all/v1", methods=["GET"])
def users_all():
    """ 
    Gets user data from http json and passes it to the
    users_all_v1 function

    Returns {users} - an list of dictionaries of individual user details
    """
    data = request.get_json()
    token = data['token']
    
    user_list = users_all_v1(token)

    save_data()

    return dumps({
        'users': user_list['users']
    })

@APP.route("/channels/list/v2", methods = ['GET'])
def channels_list():
    """
    Gets user token from http json and passes it to the
    channels_list_v2 function
    Returns {channels:[]} on success
    """
    
    data = request.get_json()
    token = data['token']
    data = channels_list_v2(token)

    save_data()
    
    return dumps(data)

@APP.route("/message/remove/v1", methods=["DELETE"])
def message_remove():
    """
    Gets user token and message_id from http json and passes it to the
    message_remove_v1 function
    Returns {} (empty dictionary) on success
    """
    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])

    message_remove_v1(token, message_id)

    save_data()

    return dumps({})

@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    """
    Gets user data from http json and passes it to the
    dm_create_v1 function

    Returns { dm_id, dm_name} on success
    """
    data = request.get_json()

    token = data['token']
    u_ids = data['u_ids']

    response = dm_create_v1(token, u_ids)

    save_data()

    return dumps (response) 

@APP.route("/user/profile/setemail/v2", methods = ['PUT'])
def set_email():
    """
    Gets user token and email from http json and pass is to the
    user_profile_setemail_v2 function
    Returns {} on success
    """
    
    data = request.get_json()
    token = data['token']
    new_email = data['email']
    user_profile_setemail_v2(token, new_email)

    save_data()
    
    return dumps({})

@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    """
    Gets user token and dm_id from http json and pass is to the
    dm_details_v1 function
    Returns {name, members} on success
    """
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))

    data = dm_details_v1(token, dm_id)

    save_data()
    
    return dumps(data)

@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove():
    """
    Gets user token and dm_id from http json and pass is to the
    dm_remove_v1 function
    Returns {} on success
    """
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']

    dm_remove_v1(token, dm_id)

    save_data()
    
    return dumps({})

@APP.route("/dm/invite/v1", methods=['POST'])
def dm_invite():
    """
    Gets user token, dm_id and u_id from http json and 
    pass is to the dm_invite_v1 function
    Returns {} on success
    """
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']
    u_id = data['u_id']

    dm_invite_v1(token, dm_id, u_id)

    save_data()
    
    return dumps({})

@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
    """
    Gets user token, dm_id and start from http params and 
    pass is to the dm_messages_v1 function
    Returns {messages, start, end} on success
    """
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    start = int(request.args.get('start'))

    response = dm_messages_v1(token, dm_id, start)

    save_data()
    
    return dumps(response)

@APP.route("/user/profile/setname/v2", methods = ['PUT'])
def set_name():
    """
    Gets user token, new first name and last name from http json and passes 
    it to the user_profile_setname_v2 function
    Returns {} on success
    """
    
    data = request.get_json()
    token = data['token']
    name_first = data['name_first']
    name_last = data['name_last']
    user_profile_setname_v2(token, name_first, name_last)

    save_data()
    
    return dumps({})

@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def userpermission_change():
    """
    Gets input data from http json and passes it to userpermission_change_v1()
    Returns {} if no errors are raised.
    """
    data = request.get_json()
    token = data['token']
    u_id = data['u_id']
    permission_id = data['permission_id']
    userpermission_change_v1(token, u_id, permission_id)
    
@APP.route("/message/edit/v2", methods=["PUT"])
def edit():
    """
    Gets user token, message_id and a message from http json and passes it to the
    message_edit_v2 function
    Returns {} (empty dictionary) on success
    """
    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])
    message = data['message']

    message_edit_v2(token, message_id, message)

    save_data()

    return dumps({})
    
@APP.route("/user/profile/sethandle/v1", methods = ['PUT'])
def set_handle():
    """
    Gets user token and new handle_str from http json and passes 
    it to the user_profile_sethandle_v1 function
    Returns {} on success
    """
    
    data = request.get_json()
    token = data['token']
    new_handle = data['handle_str']
    user_profile_sethandle_v1(token, new_handle)

    save_data()
    
    return dumps({})

@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    """
    Gets user token from arguments and passes to the
    dm_list_v1 function.
    Returns {dms} on success.
    """
    token = request.args.get('token')

    data = dm_list_v1(token)

    save_data()
    
    return dumps(data) 

@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave():
    """
    Gets user token and dm_id from http json and passes 
    it to the dm_leave_v1 function
    Returns {} on success
    """ 
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']

    response = dm_leave_v1(token, dm_id)

    save_data()
    
    return dumps(response)

@APP.route("/message/share/v1", methods=['POST'])
def message_share():
    """
    Gets user token, og_message_id, message, channel_id,
    dm_id from http json and passes it to the message_share_v1 function
    Returns {reponse} on success where response = shared_message_id
    """ 
    data = request.get_json()
    token = data['token']
    og_message_id = data['og_message_id']
    message = data['message']
    channel_id = data['channel_id']
    dm_id = data['dm_id']

    response = message_share_v1(token, og_message_id, message, channel_id, dm_id)

    save_data()
    
    return dumps(response)

@APP.route("/message/senddm/v1", methods=['POST'])
def send_dm():
    """
    Gets user token, dm_id and message from http json and passes 
    it to the message_senddm_v1 function
    Returns {message_id} on success.
    """ 
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']
    message = data['message']

    response = message_senddm_v1(token, dm_id, message)

    save_data()
    
    return dumps (response)


load_data()  # Gets data from previous server run

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
