import re, jwt, hashlib, pickle
from src.data import data

SECRET = 'dorito'

def save_data():
    global data
    with open('src/data.p', 'wb') as FILE:
        pickle.dump(data, FILE)


def load_data():
    global data
    with open('src/data.p', 'rb') as FILE:
        data = pickle.load(FILE)


def get_token_user_id(token):
    """
    Takes in a token and on success returns a u_id on success
    """
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    u_id = decoded_token['u_id']
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
