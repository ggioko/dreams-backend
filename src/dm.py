from src.error import InputError, AccessError
from src.data import data
from src.helper import get_token_user_id, check_token_valid, SECRET
import jwt
import hashlib

def dm_invite_v1(token, dm_id, u_id):
    '''    
    Given a token, ID dm_id and u_id adds user with u_id to
    the given DM
    
    Arguments: 
        token (string) - Users session token
        dm_id (int)    - ID of the DM
        u_id (int)     - ID of the user
        
    Exception: 
        InputError  - DM ID is not a valid DM.
        InputError  - User ID is not refering to a valid user
        AccessError - Occurs when token passed in is not a valid token.
        AccessError - Occurs when authorised user is not a a member of the DM
        
    Return value: 
        {} on success
    ''' 
    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description='Error Invalid token')

    # If user ids match, store details of user
    uid_valid = False
    for user in data['users']:
        if u_id == user['u_id']:
            uid_valid = True
            user = {
                'u_id' : user['u_id'],
                'email' : user['email'],
                'name_first' : user['name_first'],
                'name_last' : user['name_last'],
                'handle_str' : user['handle_str'],
                'password' : user['password']
            }
    
    # Raise error if it could not find user
    if uid_valid == False:
        raise InputError(description="U_id does not refer to a valid user")
    
    # Adds new user to DM if authorised user is a member and the dm_id is valid
    user_id = get_token_user_id(token)
    dm_valid = False
    member_valid = False
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            dm_valid = True
            # Check if authorised user is a member of DM
            for member in dm['all_members']:
                if user_id == member['u_id']:
                    member_valid = True
                    dm['all_members'].append(user)
                    break
            break

    
    # Raise error if it could not invite the user
    if dm_valid == False:
        raise InputError(description="Dm_id does not refer to a valid DM")
    if member_valid == False:
        raise AccessError(description="User is not the a member of the DM")

    return {}

    

def dm_remove_v1(token, dm_id):
    '''    
    Given a token with ID dm_id that the authorised user is the creator of, 
    deletes the dm
    
    Arguments: 
        token (string) - Users session token
        dm_id (int)    - ID of the DM
        
    Exception: 
        InputError  - DM ID is not a valid DM.
        AccessError - Occurs when token passed in is not a valid token.
        AccessError - Occurs when authorised user is not a the original creator,
                    of DM with dm_id.
        
    Return value: 
        {} on success
    '''   
    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description='Error Invalid token')
    
    # Removes DM if it can find it
    user_id = get_token_user_id(token)
    owner = False
    dm_valid = False
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            dm_valid = True
            # Check if authorised user is an owner of DM
            for member in dm['owner_members']:
                if user_id == member['u_id']:
                    owner = True
                    data['dms'].remove(dm)

    # Raise error if it could not delete the DM
    if dm_valid == False:
        raise InputError(description="Dm_id does not refer to a valid DM")
    if owner == False:
        raise AccessError(description="User is not the original DM creator")
        

    return {}

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
        raise AccessError(description="Error invalid token")

    # Check if u_ids refer to a valid member
    valid_count = len(u_ids)
    valid = 0
    for u_id in u_ids:
        for user in data['users']:
            if user['u_id'] == u_id:
                valid += 1
    
    if valid != valid_count:
        raise InputError(description="Error a u_id does not refer to a valid member")

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
                members.append({
                    'u_id' : user['u_id'],
                    'email' : user['email'],
                    'name_first' : user['name_first'],
                    'name_last' : user['name_last'],
                    'handle_str' : user['handle_str'],
                    'password' : user['password']
                })
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


def dm_list_v1(token):
    '''
    Given a token,
    On success returns a list of dictionaries called 'dms':
    Where each dictionary contains the dm_id and list of members in 
    alphabetical order as the dm_name

    Arguments:
        token (string)    - Users id

    Exceptions:
        AccessError - Occurs when token is invalid

    Return Value:
        Returns {dms} on success
        where {dms} consists of {'dms':[{dm_id,name}]}
    '''

    # Check if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description="Error invalid token")
    
    dm_list = {}
    dm_list['dms'] = []
    # Get the User id from token
    auth_user_id = get_token_user_id(token)
    for dm in data['dms']:
        for member in dm['all_members']:
            if member['u_id'] == auth_user_id:
                dm_list['dms'].append({
                    'dm_id': dm['dm_id'],
                    'name': dm['name']
                })
    
    return dm_list
               
 
def dm_details_v1(token, dm_id):
    '''
    dm_details_v1()
    
    Given a token with ID dm_id that the authorised user is part of, 
        provide basic information about the DM.
    
    Arguments: 
        token (string), dm_id (int)
        
    Exception: 
        AccessError - Occurs when token passed in is not a valid token.
        AccessError - Occurs when authorised user is not a member of DM with dm_id.
        InputError - DM ID is not a valid DM.
        
    Return value: 
        {name, members} on success
    '''   
    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description='Error Invalid token')
    
    # Check if dm_id is valid
    user_id = get_token_user_id(token)
    authorisation = 0
    dm_valid = 0
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            # Check if authorised user is a member of DM
            for member in dm['all_members']:
                if user_id == member['u_id']:
                    authorisation = 1
            dm_valid = 1
            break

    if dm_valid == 0:
        raise InputError(description="Error occurred dm_id is not valid")
    if authorisation == 0:
        raise AccessError(description="Error authorised user is not a valid member of DM")
    
    # Used to store members and name of DM
    dmDetails = {} 

    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            # Store name of DM
            dmDetails['name'] = dm['name']
            # Check the all_members section of each channel.
            dmDetails['members'] = []
            for member in dm['all_members']:
                dmDetails['members'].append({
                    'u_id': member['u_id'],
                    'email': member['email'],
                    'name_first': member['name_first'],
                    'name_last': member['name_last'],       
                    'handle_str': member['handle_str'],            
                })
    return dmDetails

def dm_leave_v1(token, dm_id):
    '''
    Given a DM ID, the user is removed as a member of this DM

    Arguments:
        token (string)    - Users id
        dm_id (int)    - DM ID

    Exceptions:
        InputError - Occurs when a u_id does not refer to a valid member
        AccessError - Occurs when token is invalid or Authorised user is 
                    not a member of DM with dm_id

    Return Value:
        Returns {} on success
    '''

    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description='Error Invalid token')
    
    # Check if dm_id is valid
    user_id = get_token_user_id(token)
    authorisation = 0
    dm_valid = 0
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            # Check if authorised user is a member of DM
            for member in dm['all_members']:
                if user_id == member['u_id']:
                    authorisation = 1
            dm_valid = 1
            break

    if dm_valid == 0:
        raise InputError(description="Error occurred dm_id is not valid")
    if authorisation == 0:
        raise AccessError(description="Error authorised user is not a valid member of DM")

    # Loop through list to find the member being removed
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            for member in dm['all_members']:
                if member['u_id'] == user_id:
                    # Copy all the user data for easier access
                    dm['all_members'].remove(member)

    return {}

