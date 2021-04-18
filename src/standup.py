from datetime import datetime, timedelta

from src.error import InputError, AccessError
from src.data import data
from src.helper import check_token_valid, check_channel_id_exists, get_token_user_id

def standup_start_v1(token, channel_id, length):
    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description='Error Invalid token')

    # Check if channel_id exists
    if check_channel_id_exists(channel_id) == False:
        raise InputError(description='Error channel id does not exist')

    for channel in data['channels']:
        if channel_id == channel['id']:
            standup = channel['standup']
    
    # Check if standup is active
    if 'is_active' in standup.keys():
        if standup['is_active'] == True:
            raise InputError(description='Error standup is already active')

    auth_user_id = get_token_user_id(token)    

    # Check if authorised user is part of channel members
    authorisation = 0
    for channel in data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                authorisation = 1
    if authorisation == 0:
        raise AccessError(description="Error occurred authorised user is not a member of channel with channel_id")

    finish = (datetime.now()+timedelta(seconds=length)).timestamp()

    for channel in data['channels']:
        if channel_id == channel['id']:
            channel['standup'] = {
                'finish' : finish,
                'user' : auth_user_id,
                'is_active' : True,
            }

    return {'time_finish': finish}