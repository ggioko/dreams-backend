from src.error import InputError, AccessError
from src.data import data

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

"""
Creates a new channel with that name that is either a public or private channel

Arguments:
    auth_user_id (int)    - Users id
    name (string)    - Channel name
    is_public (bool)    - Channel is public

Exceptions:
    InputError - Occurs when the channel name is more than 20 characters, or
                when is_public is not given a value of type bool 
    AccessError - Occurs when auth_user_id is not registered on the database,
                does not match any u_id

Return Value:
    Returns {'channel_id': channel_num,} on success

"""

def channels_create_v1(auth_user_id, name, is_public):   
    # Input error checking
    # If length of name is more thant 20 characters raise InputError 
    if len(name) > 20:
        raise InputError("Error the channel name is more than 20 characters")
    
    # Input error also raised if is_public was not of type bool
    if type(is_public) != bool:
        raise InputError("Error the is_public value is not valid can only be True or False")

    # Tracks whether auth_user_id has been matched
    valid = 0

    # If user ids match, store details of user
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            reuser = {
                    'u_id' : user['u_id'],
                    'email' : user['email'],
                    'name_first' : user['name_first'],
                    'name_last' : user['name_last'],
                    'handle' : user['handle_str'],
                    'password' : user['password']
            }
            # user id has been matched
            valid = 1

    # If user id hasnt been matched, raise AccessError
    if valid == 0:
        raise AccessError("Error occurred auth_user_id is not valid")
    
    # Find the channel number, which is channel id
    channel_num = len(data['channels']) + 1

    data['channels'].append({
                    'channel_id' : channel_num,
                    'name' : name,
                    'is_public' : is_public,
                    'owner_members' : [reuser],
                    'all_members' : [reuser],
                    'messages': {}
    })

    # returns channel id
    return {
        'channel_id': channel_num,
    }

