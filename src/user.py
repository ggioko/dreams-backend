#from src.helper import get_token_user_id
from src.error import InputError, AccessError
from src.data import data
from src.helper import check_token_valid, email_in_use, get_token_user_id
import re

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
    if user_valid == 0:
        raise InputError(description = "InputError - invalid u_id")

    token_valid = 0
    for user in data['active_tokens']:
        if user == token:
            token_valid = 1
    if token_valid == 0:
        raise AccessError(description = "AccessError - invalid token")
    # Create empty dictionary with key 'user'
    user_info = {}
    user_info['user'] = {}
    # Return info about user.
    for user in data['users']:
        if user['u_id'] == u_id:
            user_info['user']['u_id'] = user['u_id']
            user_info['user']['email'] = user['email']
            user_info['user']['name_first'] = user['name_first']
            user_info['user']['name_last'] = user['name_last']
            user_info['user']['handle_str'] = user['handle_str']
            
    return user_info


def user_profile_setname_v2(auth_user_id, name_first, name_last):
    return {
    }

def user_profile_setemail_v2(token, email):
    # Email syntax check
    if not re.match('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$',email):
        raise InputError('InputError: Incorrect email format')
    # Check if email is in use
    if email_in_use(email) == True:
        raise InputError('InputError - Email is already in use')
    # Check if token is valid
    token_valid = 0
    for user in data['active_tokens']:
        if user == token:
            token_valid = 1
    if token_valid == 0:
        raise AccessError(description = "AccessError - invalid token")
    
    # Find current user in data register and change email.
    u_id = get_token_user_id(token)
    for user in data['users']:
        if user['u_id'] == u_id:
            user['email'] = email
    for channel in data['channels']:
        for user in channel['owner_members']:
            if user['u_id'] == u_id:
                user['email'] == email
        for user in channel['all_members']:
            if user['u_id'] == u_id:
                user['email'] == email
                
    return {
    }

def user_profile_sethandle_v2(auth_user_id, handle_str):
    return {
    }