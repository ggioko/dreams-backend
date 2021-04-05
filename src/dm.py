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
            for member in dm['members']:
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
        if dm['dm_id'] == dm_id
            # Store name of DM
            dmDetails['name'] = dm['name']
            # Check the all_members section of each channel.
            dmDetails['members'] = []
            for member in dm['all_members']:
                channelDetails['all_members'].append({
                    'u_id': member['u_id'],
                    'email': member['email'],
                    'name_first': member['name_first'],
                    'name_last': member['name_last'],       
                    'handle_str': member['handle_str'],            
                })
    return dmDetails
