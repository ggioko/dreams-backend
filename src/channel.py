from src.error import InputError, AccessError
from src.data import data

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

"""
Given a channel_id of a channel that the authorised user can join, adds them to that channel

Arguments:
    auth_user_id (integer)    - Users email
    channel_id (integer)    - Users set password

Exceptions:
    InputError  - Occurs when channel_id is not a valid channel
    AccessError  - Occurs when channel_id refers to a channel that is private (when
                    the authorised user is not a global owner)

Return Value:
    Returns {}

"""

def channel_join_v1(auth_user_id, channel_id):

    reuser = {}
    # Loop until u_id match
    for user in data['users']:
        if auth_user_id == user['u_id']:
            # Copy all the user data for easier access
            reuser = {
                'u_id': user['u_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
            }

    # Check if channel_id is in the database
    channel_valid = 0
    data_copy = {}
    for channel in data['channels']:
        if channel['id'] == channel_id:
            channel_valid = 1
            data_copy = {
                'name' : 'channel1',
                'public': True,
            }
    
    if channel_valid == 0:
        raise InputError("Invalid channel_id")

    if data_copy.get('public') == True:
        # Added user to all members for channel
        for channel in data['channels']:
            if channel['id'] == channel_id:
                channelData['all_members'].append(reuser)
    elif data_copy.get('public') == False:
        raise AccessError('The channel you are trying to join is private')
    
    return {}

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }