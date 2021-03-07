from src.error import InputError, AccessError
from src.data import data

'''
channel_invite adds a user to a channel when an existing channel
user invites them into the channel.

Arguments:
    auth_user_id (int) - The ID of the existing member of the channel
    channel_id (int)   - The ID of the channel that the new member is to join
    u_id (int)         - The ID of the user new to the channel

Exceptions:
    InputError  - Occurs when channel_id does not refer to a valid channel
    InputError  - Occurs when u_id is not a valid user
    AccessError - Occurs when auth_user_id is not a member of the channel

Return Value:
    Returns an empty dictionary when exceptions are not raised
'''
def channel_invite_v1(auth_user_id, channel_id, u_id):
    foundChannel = {}
    for channel in data['channels']:
        if channel['id'] == channel_id:
            foundChannel = channel
            break
        print(channel['id'])

    if foundChannel == {}:
        raise InputError('Invalid channel ID provided')

    userMatch = False
    for user in data['users']:
        if user['u_id'] == u_id:
            userMatch = True
            break
    if userMatch == False:
        raise InputError('Member to add not a valid user')

    userMatch = False
    for user in channel['owner_members']:
        if user['u_id'] == auth_user_id:
            userMatch = True
            break
    if userMatch == False:
        raise AccessError('Authorised user not a channel member')

    channel_join_v1(u_id, channel_id)
    
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

# Not required for iteration 1
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

    # Under 6.3 of the spec raise an assesserror if the auth_user_id is invalid
    ids = [data['users'][c]['u_id'] for c in range(len(data['users']))]
    if auth_user_id not in ids:
        raise AccessError('Invalid auth_user_id')

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
                'name' : channel['name'],
                'is_public': channel.get('is_public'),
            }
    
    if channel_valid == 0:
        raise InputError("Invalid channel_id")

    if data_copy.get('is_public') == True:
        # Added user to all members for channel
        for channel in data['channels']:
            if channel['id'] == channel_id:
                channel['all_members'].append(reuser)
    else:
        raise AccessError('The channel you are trying to join is private')
    
    return {}

# Not required for iteration 1
def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

# Not required for iteration 1
def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

