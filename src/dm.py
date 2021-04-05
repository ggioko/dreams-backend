from src.error import InputError, AccessError
from src.data import data
from src.helper import get_token_user_id, check_token_valid, SECRET
import jwt
import hashlib

def dm_create_v1(token, u_ids):
    '''
    Given a token and u_ids, creates a DM with the creator and u_ids, on success
    returning the dm_id and list of members in alphabetical order as the dm_name

    Arguments:
        token (string)    - Users id
        u_ids (list)    - list of all the members

    Exceptions:
        InputError - Occurs when a u_id does not refer to a valid member
        AccessError - Occurs when token is invalid

    Return Value:
        Returns {dm_id, dm_name} on success
    '''

    # Check if token is valid
    if check_token_valid(token) == False:
        raise AccessError("Error invalid token")

    # Check if u_ids refer to a valid member
    valid_count = len(u_ids)
    valid = 0
    for u_id in u_ids:
        for user in data['users']:
            if user['u_id'] == u_id:
                valid += 1
    
    if valid != valid_count:
        raise InputError("Error a u_id does not refer to a valid member")

    # Get the User id from token
    auth_user_id = get_token_user_id(token)

    # If user ids match, store details of owner
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
    
    # Store handles of members
    dm_name_list = []
    dm_name_list.append(reuser['handle_str'])
    # Store members
    members = []
    members.append(reuser)

    # If user ids match, store details of member
    for u_id in u_ids:
        for user in data['users']:
            if u_id == user['u_id']:
                members.append(
                    {
                    'u_id' : user['u_id'],
                    'email' : user['email'],
                    'name_first' : user['name_first'],
                    'name_last' : user['name_last'],
                    'handle_str' : user['handle_str'],
                    'password' : user['password']
                    }
                )
                dm_name_list.append(user['handle_str'])
    
    # Make list of handles alphabetical
    sorted_dm_name_list = sorted(dm_name_list, key=str.lower)

    dm_num = len(data['dms']) + 1
    dm_name = ', '.join(sorted_dm_name_list)

    data['dms'].append({
                    'dm_id' : dm_num,
                    'name' : dm_name,
                    'owner_members' : [reuser],
                    'all_members' : members,
                    'messages': []
    })

    return {'dm_id': dm_num, 'dm_name': dm_name}