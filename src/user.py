from src.error import InputError, AccessError
from src.data import data
from src.helper import check_token_valid, email_in_use, get_token_user_id, get_user_data
import re
from time import time

def users_all_v1(token):
    '''
    Function that returns a list of all users and their associated details
    
    Arguments:
        token (string)    - token

    Exceptions:
        AccessError  - Occurs when token is invalid

    Return Value:
        Returns {users} on success
    '''

    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description='Invalid token')
    
    users_all = data['users']

    user_dict = {'users':[]}

    # Loop through data['users'] adding all user data to list of users except password
    for user in users_all:
        user_dict['users'].append({
            'u_id': user['u_id'], 
            'email': user['email'],
            'name_first': user['name_first'], 
            'name_last': user['name_last'], 
            'handle_str': user['handle_str'],
        })

    return user_dict

def user_profile_v2(token, u_id):
    """
    For a valid user, returns information about their user_id, email, first name, last name, and handle.
    
    Arguments:
        (token, u_id)
    Exception:
        InputError when user with u_id is not a valid user.
        AccessError when token is invalid.
    Return value:
        {user: {u_id, email, name_first, name_last, handle_str}}
    """
    # Check for exceptions first
    user_valid = 0
    for user in data['users']:
        if user['u_id'] == u_id:
            user_valid = 1
    for user in data['removed_u_ids']:
        if user == u_id:
            user_valid = 2
    if user_valid == 0:
        raise InputError(description = "InputError - invalid u_id")

    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description = 'Invalid token')
    # Create empty dictionary with key 'user'
    user_info = {}
    user_info['user'] = {}
    # Return info about user
    if user_valid == 1: # Get user info from data['users']
        for user in data['users']:
            if user['u_id'] == u_id:
                user_info['user']['u_id'] = user['u_id']
                user_info['user']['email'] = user['email']
                user_info['user']['name_first'] = user['name_first']
                user_info['user']['name_last'] = user['name_last']
                user_info['user']['handle_str'] = user['handle_str']
    elif user_valid == 2: # Get user info from data['removed_users']
        for user in data['removed_users']:
            if user != {} and user['u_id'] == u_id:
                user_info['user']['u_id'] = user['u_id']
                user_info['user']['email'] = user['email']
                user_info['user']['name_first'] = 'Removed'
                user_info['user']['name_last'] = 'user'
                user_info['user']['handle_str'] = user['handle_str']
            
    return user_info


def user_profile_setname_v2(token, name_first, name_last):
    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description='Invalid token')
    # Name size check
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError('First name needs to be between 1 and 50 characters')
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError('Last name needs to be between 1 and 50 characters')
        
    # Find current user in data register and change name
    u_id = get_token_user_id(token)
    for user in data['users']:
        if user['u_id'] == u_id:
            user['name_first'] = name_first
            user['name_last'] = name_last
    for channel in data['channels']:
        for user in channel['owner_members']:
            if user['u_id'] == u_id:
                user['name_first'] = name_first
                user['name_last'] = name_last
        for user in channel['all_members']:
            if user['u_id'] == u_id:
                user['name_first'] = name_first
                user['name_last'] = name_last
                
    return {
    }

def user_profile_setemail_v2(token, email):
    # Email syntax check
    if not re.match('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$',email):
        raise InputError('InputError: Incorrect email format')
    # Check if email is in use
    if email_in_use(email) == True:
        raise InputError('InputError - Email is already in use')
    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description = 'Invalid token')
    
    # Find current user in data register and change email.
    u_id = get_token_user_id(token)
    for user in data['users']:
        if user['u_id'] == u_id:
            user['email'] = email
    for channel in data['channels']:
        for user in channel['owner_members']:
            if user['u_id'] == u_id:
                user['email'] = email
        for user in channel['all_members']:
            if user['u_id'] == u_id:
                user['email'] = email
                
    return {
    }

def user_profile_sethandle_v1(token, handle_str):
    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description = 'Invalid token')
    # Check to see if handle is between 3 and 20 chars inclusive
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(description = "handle_str is not between 3 and 20 chars inclusive")
    # Check to see if handle is used already
    handles = get_user_data('handle_str')
    if handle_str in handles:
        raise InputError(description = "handle_str is already in use")
    
    # Otherwise, find user in data register and change handle to new handle_str.
    u_id = get_token_user_id(token)
    for user in data['users']:
        if user['u_id'] == u_id:
            user['handle_str'] = handle_str
    for channel in data['channels']:
        for user in channel['owner_members']:
            if user['u_id'] == u_id:
                user['handle_str'] = handle_str
        for user in channel['all_members']:
            if user['u_id'] == u_id:
                user['handle_str'] = handle_str
    
    return {
    }

def user_stats_dreams_v1(token):
    """
    Fetches the required statistics about the use of UNSW Dreams
    
    Arguments:
        token (string)  - Users token
    Exception:
        AccessError when token is invalid.
    Return value:
        {dreams_stats}
    """

    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description='Error Invalid token')

    num_channels_exist = len(data['channels'])
    num_dms_exist = len(data['dms'])
    num_messages_exist = data['message_count']
    time_stamp = int(time())
    total_num_users = len(data['users'])
    num_users = []
    channel_users = [data['channels'][c]['all_members'] for c in range(len(data['channels']))]
    dm_users = [data['dms'][c]['all_members'] for c in range(len(data['dms']))]
    if len(channel_users) != 0:
        for user in channel_users[0]:
            if user['u_id'] not in num_users:
                num_users.append(user['u_id'])
    if len(dm_users) != 0:
        for user in dm_users[0]:
            if user['u_id'] not in num_users:
                num_users.append(user['u_id'])

    data['dreams_stats']['channels_exist'].append({
        'num_channels_exist' : num_channels_exist, 
        'time_stamp' : time_stamp
    })
    data['dreams_stats']['dms_exist'].append({
        'num_dms_exist' : num_dms_exist, 
        'time_stamp' : time_stamp
    })
    data['dreams_stats']['messages_exist'].append({
        'num_messages_exist' : num_messages_exist, 
        'time_stamp' : time_stamp
    })

    return {
        'channels_exist': data['dreams_stats']['channels_exist'][-1], 
        'dms_exist': data['dreams_stats']['dms_exist'][-1], 
        'messages_exist': data['dreams_stats']['messages_exist'][-1], 
        'utilization_rate' : len(num_users) / total_num_users
    }
    
