from src.error import InputError, AccessError
from src.data import data
from src.helper import SECRET, valid_permission_ids, no_check_dreams_change_permission
import jwt

def userpermission_change_v1(token, u_id, permission_id):
    '''
    Arguments:
        token (str)        - Token of the existing **Dreams** owner
        u_id (int)         - User ID of user who's permission is to be changed
        permission_id (int)- New permission_id of the user
    '''
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
        raise InputError(description='Person to change permssions of does not exist')

    no_check_dreams_change_permission(u_id, permission_id)
    return {}
