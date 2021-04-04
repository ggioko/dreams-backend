from src.error import InputError, AccessError
from src.data import data
from src.helper import get_user_data, email_in_use, get_token_user_id
from time import time

def message_send_v2(token, channel_id, message):
    global data
    if token not in data['active_tokens']:
        raise AccessError(description="Not a valid token")

    if len(message) > 1000:
        raise InputError(description="Message is more than 1000 characters")

    u_id = get_token_user_id(token)

    data['message_count'] += 1

    for channel in data['channels']:
        if channel_id == channel['id']:
            user_ids = [channel['all_members'][c]['u_id'] for c in range(len(channel['all_members']))]
            if u_id not in user_ids:
                raise AccessError(description="The authorised user has not joined the channel \
                    they are trying to post to")
            channel['messages'].append({
                'message_id': data['message_count'],
                'u_id': u_id,
                'message': message,
                'time_created': int(time()),
            })

    return {
        'message_id': data['message_count'],
    }

def message_remove_v1(token, message_id):
    """
    Given a message_id for a message, this message is removed from the channel/DM

    Arguments:
        token (string)    - token
        message_id (int)    - messages id

    Exceptions:c
        InputError  - Occurs when the message_id no longer exists
        AccesError  - 

    Return Value:
        Returns {} - (empty dict) on success
    """
    return {
    }

def message_edit_v2(token, message_id, message):
    """
    Given a registered users' email and password and returns their `auth_user_id` value and 'token'

    Arguments:
        email (string)    - Users email
        password (string)    - Users password

    Exceptions:
        InputError  - Occurs when email has an incorrect format, email is not
                    registered or when the password does not match the given
                    email

    Return Value:
        Returns {'auth_user_id': id,} on success
        Returns {'token': token,} on success
    """
    return {
    }