from src.error import InputError, AccessError
from src.data import data
import jwt

SECRET = 'dorito'
def getUserFromToken(token):
    global SECRET
    decoded_jwt = jwt.decode(token.encode(), SECRET, algorithms = ['HS256'])
    u_id = int(decoded_jwt['user_id'])
    return u_id

def channels_list_v1(auth_user_id):
    '''
    channels_list_v1() - z5205069 Julius Vandeleur
    
    Provide a list of all channels (and their associated details) that the authorised user is part of.
    
    Arguments: 
        auth_user_id (int)
        
    Exception: 
        AccessError - Occurs when auth_user_id passed in is not a valid id.
        
    Return value: 
        {'channels': [{channel_id: id, name: name}...} on success
    '''
    # Output will be a dictionary containing a list of dictionaries    
    # Check if auth_user_id matches an id in the database.
    valid = 0
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            valid = 1
    if valid == 0:
        raise AccessError("Error occurred auth_user_id is not valid")
    
        
    userChannels = {'channels':[]} 
    # Loop through each channel in data.
    for channel in data['channels']:
        # Check the all_members section of each channel.
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id: 
                # Append the channel to the userChannels dictionary
                userChannels['channels'].append({
                    'channel_id' : channel['id'],
                    'name' : channel['name'],    
                })
    return userChannels

def channels_list_v2(token):
    '''
    channels_list_v2() - z5205069 Julius Vandeleur
    
    Provide a list of all channels (and their associated details) that the authorised user is part of.
    
    Arguments: 
        token (string)
        
    Exception: 
        AccessError - Occurs when token passed in is not a valid token.
        
    Return value: 
        {'channels': [{channel_id: id, name: name}...} on success
    '''
    # Output will be a dictionary containing a list of dictionaries    
    # Check if auth_user_id matches an id in the database.
    valid = 0
    for user in data['active_tokens']:
        if user == token:
            valid = 1
    if valid == 0:
        raise AccessError("Error occurred token is not valid")
    # Call getUserFromToken helper function.    
    auth_user_id = getUserFromToken(token)   
    userChannels = {'channels':[]} 
    # Loop through each channel in data.
    for channel in data['channels']:
        # Check the all_members section of each channel.
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id: 
                # Append the channel to the userChannels dictionary
                userChannels['channels'].append({
                    'channel_id' : channel['id'],
                    'name' : channel['name'],    
                })
    return userChannels
    

"""
Lists all the channels present in the database

Arguments:
    auth_user_id (int)    - Users ID

Exceptions:
    InputError  - Occurs users ID is not in the database

Return Value:
    Returns {'channels': [{channel_id: id, name: name}...} on success

"""

def channels_listall_v1(auth_user_id):
    ids = [data['users'][c]['u_id'] for c in range(len(data['users']))]
    if auth_user_id not in ids:
        raise AccessError("Invalid ID")
    channelData = {'channels':[]}
    for channel in data['channels']:
        channelData['channels'].append({
            'channel_id': channel['id'],
        	'name': channel['name'],
        })
    return channelData

"""
Creates a new channel with that name that is either a public or private channel

Arguments:
    auth_user_id (int)    - Users id
    name (string)    - Channel name
    is_public (bool)    - Channel is public

Exceptions:
    InputError - Occurs when the channel name is more than 20 characters, or
                when is_public is not given a value of type bool 
    AccessError - Occurs when auth_user_id is not registered on the database,
                does not match any u_id

Return Value:
    Returns {'channel_id': channel_num,} on success

"""

def channels_create_v1(auth_user_id, name, is_public):   
    # Input error checking
    # If length of name is more thant 20 characters raise InputError 
    if len(name) > 20:
        raise InputError("Error the channel name is more than 20 characters")
    
    # Input error also raised if is_public was not of type bool
    if type(is_public) != bool:
        raise InputError("Error the is_public value is not valid can only be True or False")

    # Tracks whether auth_user_id has been matched
    valid = 0

    # If user ids match, store details of user
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            reuser = {
                    'u_id' : user['u_id'],
                    'email' : user['email'],
                    'name_first' : user['name_first'],
                    'name_last' : user['name_last'],
                    'handle_str' : user['handle_str'],
                    'password' : user['password']
            }
            # user id has been matched
            valid = 1

    # If user id hasnt been matched, raise AccessError
    if valid == 0:
        raise AccessError("Error occurred auth_user_id is not valid")
    
    # Find the channel number, which is channel id
    channel_num = len(data['channels']) + 1

    data['channels'].append({
                    'id' : channel_num,
                    'name' : name,
                    'is_public' : is_public,
                    'owner_members' : [reuser],
                    'all_members' : [reuser],
                    'messages': {}
    })

    # returns channel id
    return {
        'channel_id': channel_num,
    }

