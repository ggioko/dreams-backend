from src.error import InputError, AccessError
from src.data import data
from src.helper import SECRET, valid_permission_ids, no_check_dreams_change_permission, check_token_valid, get_token_user_id
import jwt

def userpermission_change_v1(token, u_id, permission_id):
    '''
    Arguments:
        token (str)        - Token of the existing **Dreams** owner
        u_id (int)         - User ID of user who's permission is to be changed
        permission_id (int)- New permission_id of the user
    '''
    # Check to see if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Invalid Token")
        
    if permission_id not in valid_permission_ids:
        raise InputError(description='Invalid permission ID provided')
    
    # Gets ID of existing **Dreams** owner
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    auth_user_id = decoded_token['u_id']

    is_owner = False
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            if user['permission_id'] == 1:
                is_owner = True
            break
    if is_owner == False:
        raise AccessError(description='Person invoking change is not an owner')

    user_exists = False
    for user in data['users']:
        print(user['u_id'])
        if user['u_id'] == u_id:
            user_exists = True
            break
    if user_exists == False:
        raise InputError(description='Person to change permissions of does not exist')

    no_check_dreams_change_permission(u_id, permission_id)
    return {}

def user_remove_v1(token, u_id):
    '''
    Arguments:
        token (str)        - Token of the existing **Dreams** owner
        u_id (int)         - User ID of user is to be removed      
    Exception:
        InputError when selected user with u_id is not a valid user.
        InputError when the selected user is the only Dreams owner.
        AccessError when token is invalid.
        AccessError when user calling user_remove is not an owner.
    Return value:
        {}
    '''
    # Check to see if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Invalid Token")
        
    # Check to see if selected user exists
    user_exists = False
    for user in data['users']:
        print(user['u_id'])
        if user['u_id'] == u_id:
            user_exists = True
            break
    if user_exists == False:
        raise InputError(description='Selected user does not exist')
        
    # Gets ID of function user
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    auth_user_id = decoded_token['u_id']
    # Check to see if the function user is an Owner.
    is_owner = False
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            if user['permission_id'] == 1:
                is_owner = True
            break
    if is_owner == False:
        raise AccessError(description='Person invoking change is not an owner')
        
    # Check to see if function user is the ONLY owner.
    owner_count = 0
    for user in data['users']:
        if user['permission_id'] == 1:
            owner_count += 1
    if owner_count == 1 and u_id == auth_user_id:
        raise InputError(description="Selected user is currently the only owner")
        
    # Carry out functionality
    for user in data['users']:
        if user['u_id'] == u_id:
            data['removed_users'].append({
                                            'u_id': user['u_id'], 
                                            'email': user['email'],
                                            'name_first': user['name_first'], 
                                            'name_last': user['name_last'], 
                                            'handle_str': user['handle_str'],
                                        })
            data['users'].remove(user)
            data['removed_u_ids'].append(u_id)
            break
    # Remove user from channel members, and make changes to messages they are part of.
    for channel in data['channels']:
        for member in channel['owner_members']:
            if member['u_id'] == u_id:
                channel['owner_members'].remove(member)
        for member in channel['all_members']:
            if member['u_id'] == u_id:
                channel['all_members'].remove(member)
        for message in channel['messages']:
            if message['u_id'] == u_id:
                message['u_id'] = 'Removed user'
            for react in message['reacts']:
                for reacter in react['u_ids']:
                    if reacter == u_id:
                        reacter = 'Removed user'
    # Remove user from dm members, and make changes to messages they are part of.
    for dm in data['dms']:
        for member in dm['owner_members']:
            if member['u_id'] == u_id:
                dm['owner_members'].remove(member)
        for member in dm['all_members']:
            if member['u_id'] == u_id:
                dm['all_members'].remove(member)
        for message in dm['messages']:
            if message['u_id'] == u_id:
                message['u_id'] = 'Removed user'
            for react in message['reacts']:
                for reacter in react['u_ids']:
                    if reacter == u_id:
                        reacter = 'Removed user'
    # Finally, remove the user's token from active_tokens. 
    # They will be unable to log back in as their
    # info has been removed from the data register.
    for token in data['active_tokens']:
        if get_token_user_id(token) == u_id:
            data['active_tokens'].remove(token)