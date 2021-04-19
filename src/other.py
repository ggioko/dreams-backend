from src.data import data
from src.helper import check_token_valid, SECRET

def clear_v1():
    """
    Function to clear internal data
    """
    global data
    data['users'].clear()
    data['channels'].clear()
    data['active_tokens'].clear()
    data['message_count'] = 0
    data['dms'].clear()

def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }

def search_v2(token, query_str):
    """
    Given a query string, return a collection of messages in all of the channels/DMs
    that the user has joined that match the query
    Arguments:
        token (str)        - The token of the user who wants to search their messages
        query_str (str)    - The string that the user wants to find matches of

    Exceptions:
        InputError  - Occurs when the length of the query string is over 1000 characters

    Return Value:
        Returns a dictionary of messages in channels and DMs that the user is a part of
    """
    if len(query_str) > 1000:
        raise InputError(description='Length of query string too long')
    
    return_dict = {'messages': []}
    if not check_token_valid(token):
        return return_dict

    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    user_id = decoded_token['u_id']

    for channel in data['channels']:
        inchannel = False
        for member in channel['all_members']:
            if member['u_id'] == user_id:
                inchannel = True
                break
        if inchannel:
            for message in channel['messages']:
                if query_str in message:
                    return_dict['messages'].append(message)
    
    for dm in data['dms']:
        indm = False
        for member in dm['all_members']:
            if member['u_id'] == user_id:
                indm = True
                break
        if indm:
            for message in dm['messages']:
                if query_str in message:
                    return_dict['messages'].append(message)

    return return_dict


