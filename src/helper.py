import re
import jwt
import hashlib

SECRET = 'dorito'

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
    """
    token = jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256')
    return token