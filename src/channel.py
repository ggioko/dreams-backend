from src.error import InputError, AccessError
from src.data import data


def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

'''
channel_details_v1() - z5205069 Julius Vandeleur

Given a Channel with ID channel_id that the authorised user is part of, 
    provide basic details about the channel.

Arguments: 
    auth_user_id (int), channel_id (int)
    
Exception: 
    AccessError - Occurs when auth_user_id passed in is not a valid id.
    AccessError - Occurs when authorised user is not a member of channel with channel_id.
    InputError - Channel ID is not a valid channel.
    
Return value: 
    {name, owner_members, all_members} on success

'''
def channel_details_v1(auth_user_id, channel_id):
    
    # Check if auth_user_id matches a user in the database.
    user_valid = 0
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            user_valid = 1
    if user_valid == 0:
        raise AccessError("Error occurred auth_user_id is not valid")
        
    # Check to see if channel_id matches a channel in the database.
    channel_valid = 0
    for channel in data['channels']:
        if channel['id'] == channel_id:
            channel_valid = 1
    if channel_valid == 0:
        raise InputError("Error occurred channel_id is not valid")
        
    # Check to see if authorised user is a member of specified channel.
    authorisation = 0
    for channel in data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                authorisation = 1
    if authorisation == 0:
        raise AccessError("Error occurred authorised user is not a member of channel with channel_id")
    
    
#    return {
#        'name': 'Hayden',
#        'owner_members': [
#            {
#                'u_id': 1,
#                'email': 'cs1531@cse.unsw.edu.au',
#                'name_first': 'Hayden',
#                'name_last': 'Jacobs',
#                'handle_str': 'haydenjacobs',
#            }
#        ],
#        'all_members': [
#            {
#                'u_id': 1,
#                'email': 'cs1531@cse.unsw.edu.au',
#                'name_first': 'Hayden',
#                'name_last': 'Jacobs',
#                'handle_str': 'haydenjacobs',
#            }
#        ],
#    }

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

def channel_join_v1(auth_user_id, channel_id):
    return {
    }

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }