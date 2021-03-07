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

"""

Given a Channel with ID channel_id that the authorised user is part of, 
return up to 50 messages between index "start" and "start + 50". 
Message with index 0 is the most recent message in the channel. 

Arguments:
    auth_user_id (int)    - Users id
    channel_id (int)    - Channel id
    start (int)    - Start of the messages

Exceptions:
    InputError - Occurs when the channel ID is not a valid channel or start is 
                greater than the total number of messages in the channel
    AccessError - Occurs when authorised user is not a member of channel with  
                channel_id

Return Value:
    Returns { messages, start, end } on success

"""
def channel_messages_v1(auth_user_id, channel_id, start):
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

    # Gets a list of all the messages and also the length of the list
    for channel in data['channels']:
        if channel['id'] == channel_id:
            messages = list(channel['messages'])
            num_messages = len(messages)

    # No messages
    if num_messages == 0 and start == 0:
        return {
                'messages': [], 
                'start': start, 
                'end': -1
        }

    # If start is larger than number of items in messages
    # Raise inputError
    if start >= num_messages:
        raise InputError("Error Start value is larger than number of items in messages")
    
    # Loop through messages list, append messages to a list
    end = start + 50
    counter = 0
    messages = []
    
    while counter < 50:
        index = start + counter
        if index >= end or index >= num_messages:
            break

        new_message = {
                'message_id': messages[index].get('message_id'),
                'u_id': messages[index].get('user_id'),
                'message': messages[index].get('message_sent'),
                'time_created': messages[index].get('time_created'),
        }
        messages.append(new_message)
        counter += 1
    
    # If this function has returned the least recent messages in the channel, 
    # returns -1 in "end" to indicate there are no more messages to load after 
    # this return.           
    if counter < 50:
        end = -1

    return {
            'messages': messages, 
            'start': start, 
            'end': end
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
