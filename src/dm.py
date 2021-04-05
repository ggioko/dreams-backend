from src.error import InputError, AccessError
from src.data import data
from src.helper import get_token_user_id, check_token_valid, SECRET
import jwt
import hashlib

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

    # Remove user from all_members

    # Loop through list to find the member being removed
    for dm in data['dms']:
        if dm['dm_id'] == dm_id:
            for member in dm['all_members']:
                if member['u_id'] == user_id:
                    # Copy all the user data for easier access
                    dm['all_members'].remove(member)

    return {}


    
