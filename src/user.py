from src.data import data
from src.error import AccessError
from src.helper import check_token_valid

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

def user_profile_v1(auth_user_id, u_id):
    return {
        'user': {
            'u_id': 1,
            'email': 'cs1531@cse.unsw.edu.au',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle_str': 'haydenjacobs',
        },
    }

def user_profile_setname_v1(auth_user_id, name_first, name_last):
    return {
    }

def user_profile_setemail_v1(auth_user_id, email):
    return {
    }

def user_profile_sethandle_v1(auth_user_id, handle_str):
    return {
    }