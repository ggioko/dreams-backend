from src.error import InputError, AccessError
from src.data import data
from src.helper import get_user_data, email_in_use, get_token_user_id
from time import time

def message_send_v1(token, channel_id, message):
    global data
    if token not in data['active_tokens']:
        raise AccessError(description="Not a valid token")

    u_id = get_token_user_id(token)

    data['message_count'] += 1

    found_channel = False
    for channel in data['channels']:
        if channel_id == channel['id']:
            found_channel = True
            channel['messages'].append({
                'message_id': data['message_count'],
                'u_id': u_id,
                'message': message,
                'time_created': int(time()),
            })

    if found_channel == False:
        raise InputError(description="Channel ID is not a valid channel")

    return {
        'message_id': data['message_count'],
    }

def message_remove_v1(auth_user_id, message_id):
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    return {
    }