from src.error import InputError, AccessError
from src.data import data
from src.helper import get_token_user_id, check_token_valid, is_dreams_owner, get_user_handle
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
    sender_handle = get_user_handle(u_id)
    
    data['message_count'] += 1

    for channel in data['channels']:
        if channel_id == channel['id']:
            user_ids = [channel['all_members'][c]['u_id'] for c in range(len(channel['all_members']))]
            if u_id not in user_ids:
                raise AccessError(description="The authorised user has not joined the channel \
                    they are trying to post to")
            channel_name = channel['name']
            channel['messages'].append({
                'message_id': data['message_count'],
                'u_id': u_id,
                'message': message,
                'time_created': int(time()),
                'reacts' : [],
                'is_pinned' : False,
            })
            if len(message) >= 20:
                snippet = message[0:20]
            else:
                snippet = message
                
            for member in channel['all_members']:
                user_id = member['u_id']
                handle = get_user_handle(user_id)
                if f"@{handle}" in message:
                    for user in data['users']:
                        if user_id == user['u_id']:
                            user['notifications'].append({
                                                    'channel_id': channel_id,
                                                    'dm_id': -1,
                                                    'notification_message': f"{sender_handle} tagged you in {channel_name}: {snippet}",
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

    #Loop through dms to get a copy of the og_message
    # and to check if user is in the channel
    for dms in data['dms']:
        for messages in dms['messages']:
            if og_message_id == messages['message_id']:
                og_message_found = True
                members = dms['all_members']
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
    send_message = message + '\n' + '"""' +'\n' + copy_of_message + '\n' +'"""'
    
    # Share to channel
    if channel_id != -1:
        # send new message using existing functions
        shared_message_id = message_send_v2(token, channel_id, send_message)
        return shared_message_id

    # Share to dm
    if dm_id != -1:
        shared_message_id = message_senddm_v1(token, dm_id, send_message)
        return shared_message_id

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
    sender_handle = get_user_handle(u_id)  
    # Check size of message
    if len(message) > 1000:
        raise InputError(description="Message must be 1000 characters or less")
        
    # Otherwise, send the message to the specified dm
    global data
    data['message_count'] += 1
    message_id = data['message_count']
    
    for dm in data['dms']:
        if dm_id == dm['dm_id']:
            dm_name = dm['name']
            user_ids = [dm['all_members'][c]['u_id'] for c in range(len(dm['all_members']))]
            if u_id not in user_ids:
                raise AccessError(description="Not a member of this dm")
                
            dm['messages'].append({
                'message_id': message_id,
                'u_id': u_id,
                'message': message,
                'time_created': int(time()),
                'reacts' : [],
                'is_pinned' : False,
            })
            if len(message) >= 20:
                snippet = message[0:20]
            else:
                snippet = message
                
            for member in dm['all_members']:
                user_id = member['u_id']
                handle = get_user_handle(user_id)
                if f"@{handle}" in message:
                    for user in data['users']:
                        if user_id == user['u_id']:
                            user['notifications'].append({
                                                    'channel_id': -1,
                                                    'dm_id': dm_id,
                                                    'notification_message': f"{sender_handle} tagged you in {dm_name}: {snippet}"
                                                    })
       
    return {'message_id': message_id}


def message_pin_v1(token, message_id):
    """
    Given a message within a channel or DM, mark it as "pinned" to be given special display treatment by the frontend

    Arguments:
        token (string)    - Token
        message_id (int)    - Messages id

    Exceptions:
        InputError  - Message_id is not a valid message
                    - Message with ID message_id is already pinned
        AccesError  - The authorised user is not a member of the channel or DM that the message is within
                    - The authorised user is not an owner of the channel or DM

    Return Value:
        Returns {} - (empty dict) on success
    """

    # Checks if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Not a valid token")
    
    user_id = get_token_user_id(token)

    message_found = False
    auth = False

    # Loop through channels looking for message
    # and to check if user is in the channel
    for channel in data['channels']:
        for messages in channel['messages']:
            if message_id == messages['message_id']:
                message_found = True
                # Based on AccessError, the user has to be an owner to pin a message
                members = channel['owner_members']
                for member in members:
                    if user_id == member['u_id']:
                        auth = True
                if auth == True:
                    # Check if message is already pinned
                    if messages['is_pinned'] == True:
                        raise InputError(description="This message is already pinned")
                    # Pins the message
                    else:
                        messages['is_pinned'] = True
    
    # If the message was not found check dm messages with same process
    if message_found == False:
        for dms in data['dms']:
            for messages in dms['messages']:
                if message_id == messages['message_id']:
                    message_found = True
                    members = dms['owner_members']
                    # Check if the user trying to pin is in the dm
                    for member in members:
                        if user_id == member['u_id']:
                            auth = True
                    if auth == True:
                        # Check if message is already pinned
                        if messages['is_pinned'] == True:
                            raise InputError(description="This message is already pinned")
                        # Pins the message
                        else:
                            messages['is_pinned'] = True

    # If message is not found either channels or dms raises InputError
    # If message is found but user is not in chat, raises AccessError
    if message_found == False:
        raise InputError(description="Message was not found")
    
    if auth == False:
        raise AccessError(description="You are not allowed to pin this message")

    return {}

def message_unpin_v1(token, message_id):
    """
    Given a message within a channel or DM, remove it's mark as unpinned

    Arguments:
        token (string)    - Token
        message_id (int)    - Messages id

    Exceptions:
        InputError  - Message_id is not a valid message
                    - Message with ID message_id is already unpinned
        AccesError  - The authorised user is not a member of the channel or DM that the message is within
                    - The authorised user is not an owner of the channel or DM

    Return Value:
        Returns {} - (empty dict) on success
    """

    # Checks if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Not a valid token")
    
    user_id = get_token_user_id(token)

    message_found = False
    auth = False

    # Loop through channels looking for message
    # and to check if user is in the channel
    for channel in data['channels']:
        for messages in channel['messages']:
            if message_id == messages['message_id']:
                message_found = True
                # Based on AccessError, the user has to be an owner to unpin a message
                members = channel['owner_members']
                for member in members:
                    if user_id == member['u_id']:
                        auth = True
                if auth == True:
                    # Check if message is already unpinned
                    if messages['is_pinned'] == False:
                        raise InputError(description="This message is already unpinned")
                    # Unpins the message
                    else:
                        messages['is_pinned'] = False
    
    # If the message was not found check dm messages with same process
    if message_found == False:
        for dms in data['dms']:
            for messages in dms['messages']:
                if message_id == messages['message_id']:
                    message_found = True
                    members = dms['owner_members']
                    # Check if the user trying to unpin is in the dm
                    for member in members:
                        if user_id == member['u_id']:
                            auth = True
                    if auth == True:
                        # Check if message is already unpinned
                        if messages['is_pinned'] == False:
                            raise InputError(description="This message is already unpinned")
                        # Unpins the message
                        else:
                            messages['is_pinned'] = False

    # If message is not found either channels or dms raises InputError
    # If message is found but user is not in chat, raises AccessError
    if message_found == False:
        raise InputError(description="Message was not found")
    
    if auth == False:
        raise AccessError(description="You are not allowed to unpin this message")

    return {}

def message_react_v1(token, message_id, react_id):
    """
    Given a message within a channel or DM the authorised user is part of, add a "react" to that particular message

    Arguments:
        token (string)    - Token
        message_id (integer)    - id of the message to react to
        react_id (integer)     - id of a react (currently the only react id is 1 (thunbs up))

    Exceptions:
        InputError  - message_id is not a valid message within a channel or DM that the authorised user has joined
                    - react_id is not a valid React ID. The only valid react ID the frontend has is 1
                    - Message with ID message_id already contains an active React with ID react_id from the authorised user
        AccesError  - The authorised user is not a member of the channel or DM that the message is within

    Return Value:
        Returns {} on success
    """

    # Checks if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Not a valid token")
    
    # Check react_id is valid
    # Currently the front end only has one reaction which is a thumbsup
    # This list can be changed to add in new react ids, 
    # the code below is setup so that nothing needs to be changed if the list is edited
    list_of_reacts = [1]
    if react_id not in list_of_reacts:
        raise InputError(description="Invalid react_id detected")
    
    user_id = get_token_user_id(token)
    message_found = False
    auth = False
    already_reacted = False
    
    # Loop through channels looking for message
    # and to check if user is in the channel
    for channel in data['channels']:
        for messages in channel['messages']:
            if message_id == messages['message_id']:
                message_found = True
                # Raise auth flag if user is a member of the channel
                members = channel['all_members']
                for member in members:
                    if user_id == member['u_id']:
                        auth = True
                if auth == True:
                    # Check if user has already reacted to message with the same react_id
                    for react in messages['reacts']:
                        if react['react_id'] == react_id:
                            for u_id in react['u_ids']:
                                if user_id == u_id:
                                    already_reacted = True
                                    raise InputError(description="You have already reacted to this message")
                    # If user hasnt reacted, react to message
                    if already_reacted == False:
                        flag = 0
                        for react in messages['reacts']:
                            # If a react of that type already exists
                            if react['react_id'] == react_id:
                                flag = 1
                                react['u_ids'].append(user_id)
                                react['is_this_user_reacted'] = True
                            # if its the first react of its type
                        if flag == 0:
                            messages['reacts'].append({
                                'react_id' : int(react_id),
                                'u_ids' : [user_id],
                                'is_this_user_reacted' : True,
                            })

    # If message not found, check dm messages with same process
    if message_found == False:
        for dms in data['dms']:
            for messages in dms['messages']:
                if message_id == messages['message_id']:
                    message_found = True
                    # Raise auth flag if user is a member of the channel
                    members = dms['all_members']
                    for member in members:
                        if user_id == member['u_id']:
                            auth = True
                    if auth == True:
                        # Check if user has already reacted to message
                        for react in messages['reacts']:
                            for u_id in react['u_ids']:
                                if user_id == u_id:
                                    already_reacted = True
                                    raise InputError(description="You have already reacted to this message")
                        # If user hasnt reacted, react to message
                        if already_reacted == False:
                            flag = 0
                            for react in messages['reacts']:
                                # If a react of that type already exists
                                if react['react_id'] == react_id:
                                    flag = 1
                                    react['u_ids'].append(user_id)
                                    react['is_this_user_reacted'] = True
                                # if its the first react of its type
                            if flag == 0:
                                messages['reacts'].append({
                                    'react_id' : int(react_id),
                                    'u_ids' : [user_id],
                                    'is_this_user_reacted' : True,
                                })

    # If message is not found either channels or dms raises InputError
    # If message is found but user is not in chat, raises AccessError
    if message_found == False:
        raise InputError(description="Message was not found")
    
    if auth == False:
        raise AccessError(description="You are not allowed to react to this message")

    return {}

def message_unreact_v1(token, message_id, react_id):
    """
    Given a message within a channel or DM the authorised user is part of, remove a "react" to that particular message

    Arguments:
        token (string)    - Token
        message_id (integer)    - id of the message to react to
        react_id (integer)     - id of a react (currently the only react id is 1 (thunbs up))

    Exceptions:
        InputError  - message_id is not a valid message within a channel or DM that the authorised user has joined
                    - react_id is not a valid React ID. The only valid react ID the frontend has is 1
                    - Message with ID message_id already contains an active React with ID react_id from the authorised user
        AccesError  - The authorised user is not a member of the channel or DM that the message is within

    Return Value:
        Returns {} on success
    """

    # Checks if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Not a valid token")
    
    # Check react_id is valid
    # Currently the front end only has one reaction which is a thumbsup
    # This list can be changed to add in new react ids, 
    # the code below is setup so that nothing needs to be changed if the list is edited
    list_of_reacts = [1]
    if react_id not in list_of_reacts:
        raise InputError(description="Invalid react_id detected")
    
    user_id = get_token_user_id(token)
    message_found = False
    auth = False
    
    # Loop through channels looking for message
    # and to check if user is in the channel
    for channel in data['channels']:
        for messages in channel['messages']:
            if message_id == messages['message_id']:
                message_found = True
                # Raise auth flag if user is a member of the channel
                members = channel['all_members']
                for member in members:
                    if user_id == member['u_id']:
                        auth = True
                if auth == True:
                    # Check if there is an active react from the user with react_id
                    existing_react = False
                    for react in messages['reacts']:
                        if react['react_id'] == react_id:
                            existing_react = True
                            if user_id not in react['u_ids']:
                                raise InputError(description="You have not reacted to this message before")
                    if existing_react == False:
                        raise InputError(description="You have not reacted to this message before")
                    # If user has reacted, unreact to message
                    flag = 0
                    for reacts in messages['reacts']:
                        if reacts['react_id'] == react_id:
                            reacts['u_ids'].remove(user_id)
                            reacts['is_this_user_reacted'] = False
                            if len(reacts['u_ids']) == 0:
                                flag = 1
                    # If list of u_ids for that react is now 0, it removes that react from the list of reacts entirely
                    if flag == 1:
                        for react in messages['reacts']:
                            if react['react_id'] == react_id:
                                messages['reacts'].remove(react)

    # If message not found, check dm messages with same process
    if message_found == False:
        for dms in data['dms']:
            for messages in dms['messages']:
                if message_id == messages['message_id']:
                    message_found = True
                    # Raise auth flag if user is a member of the channel
                    members = dms['all_members']
                    for member in members:
                        if user_id == member['u_id']:
                            auth = True
                    if auth == True:
                        # Check if there is an active react from the user with react_id
                        existing_react = False
                        for react in messages['reacts']:
                            if react['react_id'] == react_id:
                                existing_react = True
                                if user_id not in react['u_ids']:
                                    raise InputError(description="You have not reacted to this message before")
                        if existing_react == False:
                            raise InputError(description="You have not reacted to this message before")
                        # If user has reacted, unreact to message
                        flag = 0
                        for react in messages['reacts']:
                            if react['react_id'] == react_id:
                                react['u_ids'].remove(user_id)
                                react['is_this_user_reacted'] = False
                                if len(react['u_ids']) == 0:
                                    flag = 1
                        # If list of u_ids for that react is now 0, it removes that react from the list of reacts entirely
                        if flag == 1:
                            for react in messages['reacts']:
                                if react['react_id'] == react_id:
                                    messages['reacts'].remove(react)

    # If message is not found either channels or dms raises InputErrors
    # If message is found but user is not in chat, raises AccessError
    if message_found == False:
        raise InputError(description="Message was not found")
    
    if auth == False:
        raise AccessError(description="You are not allowed to unreact to this message")

    return {}
