def channel_invite(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave(auth_user_id, channel_id):
    return {
    }

def channel_join(auth_user_id, channel_id):
    return {
    }

def channel_addowner(auth_user_id, channel_id, u_id):
    return {
    }

def channel_removeowner(auth_user_id, channel_id, u_id):
    return {
    }