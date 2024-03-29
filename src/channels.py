from src.error import InputError, AccessError
from src.data import data
from src.helper import get_token_user_id, check_token_valid
import re
import jwt
import hashlib


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
        raise AccessError(description = "Error occurred token is not valid")
    # Call get_token_user_id helper function.    
    auth_user_id = get_token_user_id(token) 
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

def channels_listall_v2(token):
    """
    Lists all the channels present in the database

    Arguments:
        token (string)    - Users session token

    Exceptions:
        Access Error  - Occurs when users token is not active

    Return Value:
        Returns {'channels': [{channel_id: id, name: name}...} on success

    """
    # Checks is token is active
    """
    if len(data['active_tokens']) == 0 or token not in data['active_tokens']:
        raise AccessError(description="Invalid Token")
    """
    if check_token_valid(token) == False:
        raise AccessError(description="Invalid Token")
    
    # Creates dictionary with a list of channels and populates it

    channelData = {'channels':[]}
    for channel in data['channels']:
        channelData['channels'].append({
            'channel_id': channel['id'],
        	'name': channel['name'],
        })
    return channelData

def channels_create_v2(token, name, is_public): 
    """
    Creates a new channel with that name that is either a public or private channel

    Arguments:
        token (string)    - Users id
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
    # Check if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Error invalid token")

    # Input error checking
    # If length of name is more thant 20 characters raise InputError 
    if len(name) > 20:
        raise InputError(description="Error the channel name is more than 20 characters")
    
    # Input error also raised if is_public was not of type bool
    if type(is_public) != bool:
        raise InputError(description="Error the is_public value is not valid can only be True or False")

    auth_user_id = get_token_user_id(token)
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
    
    # Find the channel number, which is channel id
    channel_num = len(data['channels']) + 1

    data['channels'].append({
                    'id' : channel_num,
                    'name' : name,
                    'is_public' : is_public,
                    'owner_members' : [reuser],
                    'all_members' : [reuser],
                    'messages': [],
                    'standup' : {
                                'finish' : None,
                                'token' : None,
                                'user' : None,
                                'is_active' : None,
                                'queue' : '',
                                }
    })

    # returns channel id
    return {
        'channel_id': channel_num,
    }

