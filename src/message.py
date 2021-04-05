from src.error import InputError, AccessError
from src.data import data
from src.helper import get_token_user_id, check_token_valid
from dm import dm_list_v1
from time import time

def message_send_v2(token, channel_id, message):
    """
    Sends a message from authorised_user to the channel specified by channel_id. 
    Each message has it's own unique ID such that no two messages share an ID, 
    even if that other message is in a different channel.

    Arguments:
        token (string)    - Token
        channel_id (int)    - Channel id
        message (string)    - Message given to change

    Exceptions:
        InputError  - Message is over 1000 characters
        AccesError  - When the authorised user has not joined the channel they are trying to post to

    Return Value:
        Returns {message_id} on success
    """
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
        token (string)    - Token
        message_id (int)    - Messages id

    Exceptions:
        InputError  - Occurs when the message_id no longer exists
        AccesError  - When none of the following are true: 
                        - Message with message_id was sent by the authorised user making this request
                        - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

    Return Value:
        Returns {} - (empty dict) on success
    """
    # Checks if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Not a valid token")

    user_id = get_token_user_id(token)

    # Checks if message_id is still valid (not been removed or has even been created yet)
    # Checks if user is allowed to delete the message
    message_found = False
    auth = False

    for channel in data['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                message_found = True
                owners = channel['owner_members']
                # Check if the user trying to delete is a channel owner
                for owner in owners:
                    if user_id == owner['u_id']:
                        auth = True
                        channel['messages'].remove(message)
                    # Check if the user trying to delete is the one who sent it
                    elif user_id == message['u_id']:
                        auth = True
                        channel['messages'].remove(message)
    
    if message_found == False:
        raise InputError(description="Message_id not found")
    
    if auth == False:
        raise AccessError(description="You are not allowed to delete this message")

    return {}

def message_edit_v2(token, message_id, message):
    """
    Given a message, update its text with new text. If the new message is an empty string, the message is deleted.

    Arguments:
        token (string)    - Token
        message_id (int)    - Messages id
        message (string)    - Message to replace old message

    Exceptions:
        InputError  - Occurs when the message_id refers to a deleted message
                    - Message is over 1000 characters
        AccesError  - When none of the following are true: 
                        - Message with message_id was sent by the authorised user making this request
                        - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

    Return Value:
        Returns {} - (empty dict) on success
    """
    # Checks if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Not a valid token")

    # If message is over 1000 characters, raise InputError
    if len(message) > 1000:
        raise InputError(description="Message is more than 1000 characters")

    # If the new message is an empty string, the message is deleted.
    if len(message) == 0:
        message_remove_v1(token, message_id)
        return {}
    
    edited_message = message

    user_id = get_token_user_id(token)

    # Checks if message_id is still valid (not been removed or has even been created yet)
    # Checks if user is allowed to delete the message
    message_found = False
    auth = False

    for channel in data['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                message_found = True
                owners = channel['owner_members']
                # Check if the user trying to delete is a channel owner
                for owner in owners:
                    if user_id == owner['u_id']:
                        auth = True
                        message['message'] = edited_message
                    # Check if the user trying to delete is the one who sent it
                    elif user_id == message['u_id']:
                        auth = True
                        message['message'] = edited_message
    
    if message_found == False:
        raise InputError(description="Message_id not found")
    
    if auth == False:
        raise AccessError(description="You are not allowed to edit this message")

    return {}

def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    """
    Takes in token, og_message_id, message, channel_id, dm_id and shares a message 
    (og_message_id) to either a channel or dm with a another message on top (message)
    message is the optional message in addition to the shared message, and will be 
    an empty string '' if no message is given

    Arguments:
        token (string)    - Token
        og_message_id (integer)    - Messages id of message going to be shared
        message (string)    - Optional message to add to share
        channel_id (integer)    - id of channel to share to (-1 if share location isnt a channel)
        dm_id (integer)     - id of dm to share to (-1 if share location isnt a dm)

    Exceptions:
        AccesError  - if the user isnt in the channel or dm they want to share to

    Return Value:
        Returns {shared_message_id} on success
    """
    # Checks if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Not a valid token")

    # If message is over 1000 characters, raise InputError
    if len(message) > 1000:
        raise InputError(description="Message is more than 1000 characters")
    
    user_id = get_token_user_id(token)

    og_message_found = False
    auth = False
    copy_of_message = ''

    # Loop through channels to get a copy of the og_message
    # and to check if user is in the channel
    for channel in data['channels']:
        for messages in channel['messages']:
            if og_message_id == messages['message_id']:
                og_message_found = True
                members = channel['all_members']
                # Check if the user trying to share is in the channel
                for member in members:
                    if user_id == member['u_id']:
                        auth = True
                        copy_of_message = messages['message']



    # If message is not found either channels or dms raises InputError
    # If message is found but user is not in chat, raises AccessError
    if og_message_found == False:
        raise InputError(description="Message_id not found")
    
    if auth == False:
        raise AccessError(description="You are not allowed to edit this message")

    #Update message to format seen on frontend
    send_message = message + copy_of_message 
    
    # Share to channel
    if channel_id != -1
        # send new message using existing functions
        message_send_v2(token, channel_id, send_message)

    # Share to dm
    if dm_id != -1

        for channel in data['channels']:
            for message in channel['messages']:
                if og_message_id == message['message_id']:
                    og_message_found = True
                    members = channel['all_members']
                    # Check if the user trying to share is in the channel
                    for member in members:
                        if user_id == member['u_id']:
                            auth = True
                            copy_of_message = message['message']

    list_dms = dm_list_v1(token)
    for dm in list_dms:

    return {}
