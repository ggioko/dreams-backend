'''
channels_list_v1() - z5205069 Julius Vandeleur

Provide a list of all channels (and their associated details) that the authorised user is part of.

Arguments: 
    auth_user_id (int)
    
Return value: 
    {'channels':[]}

Exception: 
    AccessError - Occurs when auth_user_id passed in is not a valid id.
'''

from src.data import data
from src.error import AccessError

def channels_list_v1(auth_user_id):
    # Output will be a dictionary containing a list of dictionaries
    
    # Check if auth_user_id matches an id in the database.
    valid = 0
    for user in data['users']:
        if auth_user_id == user['u_id']:
            ++valid
            
    if valid == 0:
        raise AccessError("Error occurred auth_user_id is not valid")
    
        
    userChannels = {'channels':[]} 
    # Loop through each channel in data.
    for channel in data['channels']:
        # Check the all_members section of each channel.
        for member in channel['all_members']:
            if auth_user_id == member['u_id']: 
                # Append the channel to the userChannels dictionary
                userChannels['channels'].append({
                    'channel id' : channel['id'],
                    'name' : channel['name'],    
                })
    return userChannels

    

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }
