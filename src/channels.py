from src.data import data
from src.error import AccessError

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

"""
Lists all the channels present in the database

Arguments:
    auth_user_id (int)    - Users ID

Exceptions:
    InputError  - Occurs users ID is not in the database

Return Value:
    Returns {'channels': [{channel_id: id, name: name}...} on success

"""

def channels_listall_v1(auth_user_id):
    ids = [data['users'][c]['u_id'] for c in range(len(data['users']))]
    if auth_user_id not in ids:
        raise AccessError("Invalid ID")
    channelData = {'channels':[]}
    for channel in data['channels']:
        channelData['channels'].append({
            'channel_id': channel['id'],
        	'name': channel['name'],
        })
    return channelData

def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }
