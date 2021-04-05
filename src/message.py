from src.error import InputError, AccessError
from src.data import data
from src.helper import get_token_user_id, check_token_valid, is_dreams_owner
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

    if is_dreams_owner(user_id):
        auth = True

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

    if is_dreams_owner(user_id):
        auth = True

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


def message_senddm_v1(token, dm_id, message):
    """
    Send a message from authorised user to the DM specified by dm_id.
    Each message will have its own unique message_id in all of Dreams.

    Arguments:
        token (string)      - Token
        dm_id (int)         - identifies the dm to receive the message
        message (string)    - Message being sent as a string

    Exceptions:
        InputError  - Message is over 1000 characters
        AccessError - Invalid token
                    - User is not a member of the dm they are trying to message.

    Return Value:
        Returns {} - (empty dict) on success    
    """
    # Check if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Not a valid token")
        
    u_id = get_token_user_id(token)
    # Check if user is a member of the dm
#    membership = 0
#    for dm in data['dms']:
#        if dm['dm_id'] == dm_id:
#            for member in dm['all_members']:
#                if u_id == member['u_id']:
#                    membership = 1 
#    if membership == 0:
#        raise AccessError(description="Not a member of this dm")
        
    # Check size of message
    if len(message) > 1000:
        raise InputError(description="Message must be 1000 characters or less")
        
    # Otherwise, send the message to the specified dm
    global data
    data['message_count'] += 1
    message_id = data['message_count']
    
    
    for dm in data['dms']:
        if dm_id == dm['dm_id']:
            user_ids = [dm['all_members'][c]['u_id'] for c in range(len(dm['all_members']))]
            if u_id not in user_ids:
                raise AccessError(description="Not a member of this dm")
                
            dm['messages'].append({
                'message_id': message_id,
                'u_id': u_id,
                'message': message,
                'time_created': int(time()),
            })
       
    return {'message_id': message_id}
 
    




