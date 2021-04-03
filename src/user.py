#from src.helper import get_token_user_id
from src.error import InputError, AccessError
from src.data import data

def user_profile_v1(auth_user_id, u_id):
    """
    For a valid user, returns information about their user_id, email, first name, last name, and handle.
    
    Arguments:
        (auth_user_id, u_id)
    Exception:
        InputError when user with u_id is not a valid user.
    Return value:
        {user: {u_id, email, name_first, name_last, handle_str}}
    """
    return {
        'user': {
            'u_id': 1,
            'email': 'cs1531@cse.unsw.edu.au',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle_str': 'haydenjacobs',
        },
    }

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


def user_profile_setname_v1(auth_user_id, name_first, name_last):
    return {
    }

def user_profile_setemail_v1(auth_user_id, email):
    return {
    }

def user_profile_sethandle_v1(auth_user_id, handle_str):
    return {
    }