import re, jwt, hashlib, pickle
from src.data import data

SECRET = 'dorito'

valid_permission_ids = [0,1]

def save_data():
    """
    Opens a pickle data file and saves current data to it
    """
    with open('src/data.p', 'wb') as FILE:
        pickle.dump(data, FILE)


def load_data():
    """
    Opens a pickle data file and loads saved data from it
    and stores it into the data global variable
    """
    with open('src/data.p', 'rb') as FILE:
        data = pickle.load(FILE)
    return data

def get_token_user_id(token):
    """
    Takes in a token and on success returns a u_id on success
    """
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    u_id = int(decoded_token['u_id'])
    return u_id

def generate_token(u_id):
    """
    Takes in a u_id and on success returns a token on success
    THIS FUNCTION IS USED TO CREATE FAKE TOKENS WHEN TESTING
    """
    token = jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256')
    return token

def get_token(user_data):
    """
    Helper function to generate new token for a new session.
    Takes in user data and outputs token
    """
    i = 0
    while True:
        token = jwt.encode({'u_id' : user_data['u_id'], 'session_id' : i}, SECRET, algorithm='HS256')
        i += 1
        if token not in data['active_tokens']:
            break
    data['active_tokens'].append(token)
    return token

def get_user_data(data_type):
    """
    Helper function that returns a list of user data for a specific 
    parameter. E.g. argument 'email' returns a list of user emails
    """
    return [data['users'][c][data_type] for c in range(len(data['users']))]

def email_in_use(email):
    """
    Helper function that check if email is in use
    """
    emails = get_user_data('email')
    if email in emails:
        return True
    return False

def check_token_valid(token):
    """
    Helper function to check if a token is valid.
    Takes in a token and outputs True if valid, False otherwise
    """
    active_tokens = data['active_tokens']
    for x in active_tokens:
        if x == token:
            return True
    return False

def no_check_dreams_change_permission(u_id, permission_id):
    print(data['users'])
    
    for user in data['users']:
        # print(user)
        if user['u_id'] == u_id:
            user['permission_id'] = permission_id
            break
    channels = data['channels']
    for channel in channels:
        for owner_member in channel['owner_members']:
            if owner_member['u_id'] == u_id:
                owner_member['permission_id'] = permission_id
                break
        for all_member in channel['all_members']:
            if all_member['u_id'] == u_id:
                all_member['permission_id'] = permission_id
                break

def is_dreams_owner(u_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            if user['permission_id'] == 1:
                return True
            return False
    return False

def check_channel_id_exists(channel_id):
    """
    Helper function to check if a channel exists.
    Takes in a channel_id and outputs True if valid, False otherwise
    """
    for channel in data['channels']:
        if channel['id'] == channel_id:
            return True
    return False
