from src.error import InputError
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

def channels_create_v1(auth_user_id, name, is_public):
    
    # Input error checking 
    if len(name) > 20:
        raise InputError("Error the channel name is more than 20 characters")

    # If user ids match, store details of user
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            reuser = {
                    'u_id' : user['u_id'],
                    'email' : user['email'],
                    'first_name' : user['name_first'],
                    'last_name' : user['name_last'],
                    'handle' : user['handle_str'],
                    'password' : user['password']
            }
    
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

