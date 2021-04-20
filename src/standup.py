from datetime import datetime, timedelta

from src.error import InputError, AccessError
from src.data import data
from src.helper import check_token_valid, check_channel_id_exists, get_token_user_id
from src.message import message_send_v2

def standup_start_v1(token, channel_id, length):
    '''    
    For a given channel, start the standup period whereby for the next "length" seconds 
    if someone calls "standup_send" with a message, it is buffered during the X second window 
    then at the end of the X second window a message will be added to the message queue in the channel.
    
    Arguments: 
        token (string) - Users session token
        channel_id (int)    - channel id
        length (int)    - length of the standup in seconds
        
    Exception: 
        InputError  - Channel id is not a valid channel.
        InputError  - An active standup is currently running in this channel
        AccessError - Occurs when token passed in is not a valid token.
        AccessError - Occurs when authorised user is not a a member of the channel.
        
    Return value: 
        {time_finish} on success
    ''' 
    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description='Error Invalid token')

    # Check if channel_id exists
    if check_channel_id_exists(channel_id) == False:
        raise InputError(description='Error channel id does not exist')

    for channel in data['channels']:
        if channel_id == channel['id']:
            standup = channel['standup']
    
    # Check if standup is active
    if standup['is_active'] == True:
        raise InputError(description='Error standup is already active')

    auth_user_id = get_token_user_id(token)    

    # Check if authorised user is part of channel members
    authorisation = 0
    for channel in data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                authorisation = 1
    if authorisation == 0:
        raise AccessError(description="Error occurred authorised user is not a member of channel with channel_id")

    finish = (datetime.now()+timedelta(seconds=length)).timestamp()

    for channel in data['channels']:
        if channel_id == channel['id']:
            channel['standup'] = {
                'finish' : finish,
                'token' : token,
                'user' : auth_user_id,
                'is_active' : True,
                'queue' : '',
            }

    return {'time_finish': finish}

def standup_active_v1(token, channel_id):
    '''    
    For a given channel, return whether a standup is active in it, and what time the standup finishes. 
    If no standup is active, then time_finish returns None
    
    Arguments: 
        token (string) - Users session token 
        channel_id (int)  - channel id
        
    Exception: 
        InputError  - Channel id is not a valid channel.
        AccessError - Occurs when token passed in is not a valid token.
        
    Return value: 
        { is_active, time_finish } on success
    ''' 

    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description='Error Invalid token')

    # Check if channel_id exists
    if check_channel_id_exists(channel_id) == False:
        raise InputError(description='Error channel id does not exist')
    
    current_time = datetime.now().timestamp()

    for channel in data['channels']:
        if channel_id == channel['id']:
            standup = channel['standup']
            # If standup is finished
            if standup['finish'] < current_time:
                if standup['is_active'] == True:
                    standup['is_active'] = False
                    message_send_v2(standup['token'], channel_id, standup['queue'])
                return {'is_active' : False, 'time_finish' : None}
            return {'is_active' : True, 'time_finish' : standup['finish']}

def standup_send_v1(token, channel_id, message):
    '''    
    Sending a message to get buffered in the standup queue, assuming a standup is currently active
    
    Arguments: 
        token (string) - Users session token 
        channel_id (int)  - channel id
        message (str)  - message for standup
        
    Exception: 
        InputError  - Channel ID is not a valid channel
        InputError  - Message is more than 1000 characters (not including the username and colon)
        InputError  - An active standup is not currently running in this channel
        AccessError - Occurs when token passed in is not a valid token.
        AccessError - The authorised user is not a member of the channel that the message is within
        
    Return value: 
        { } on success
    ''' 
    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description='Error Invalid token')

    # Check if channel_id exists
    if check_channel_id_exists(channel_id) == False:
        raise InputError(description='Error channel id does not exist')

    # Check if message is more than 1000 characters
    if len(message) > 1000:
        raise InputError(description='Error message is more than 1000 characters')

    auth_user_id = get_token_user_id(token)

    # Check if authorised user is part of channel members
    authorisation = 0
    for channel in data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                authorisation = 1

    if authorisation == 0:
        raise AccessError(description="Error occurred authorised user is not a member of channel with channel_id")

    for channel in data['channels']:
        if channel_id == channel['id']:
            standup = channel['standup']
            standup_message = standup['queue']

    # Check if active standup is running in channel
    if standup['is_active'] == False:
        raise InputError(description='Error active standup is not running in channel')
    
    # Find users first name using auth_user_id
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            user_name = user['name_first']
    
    # Append message to queue
    standup_message += user_name+": "+message+"\n"

    standup['queue'] = standup_message
    return {}