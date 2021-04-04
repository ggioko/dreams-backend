import pytest
import requests
import json
from src import config
from src.helper import generate_token
from src.error import AccessError, InputError

def test_user_profile():
    """
    A simple test to check if user_profile_v2 works by passing in valid info.
    """
    # Clear data first.
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user = r.json()
    r2 = requests.get(config.url + 'user/profile/v2', json={'token': user['token'], 'u_id': user['auth_user_id']})
    assert r2.json() == {'user': {
                             'u_id': user['auth_user_id'],
                             'email': 'validemail@gmail.com',
                             'name_first': 'Hayden',
                             'name_last': 'Everest',
                             'handle_str': 'haydeneverest'          
          }}
    
    
def test_user_profile_errors():
    """
    Checks the InputError (400) and AccessError cases (403).
    """
    # Clear data first.
    requests.delete(config.url + 'clear/v1')
    
    # Test for input error - invalid u_id
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user = r.json()
    r = requests.get(config.url + 'user/profile/v2', json={'token': user['token'], 'u_id': 'invalid_u_id'})
    assert r.status_code == InputError().code
    r = requests.get(config.url + 'user/profile/v2', json={'token': -1, 'u_id': user['auth_user_id']})
    assert r.status_code == AccessError().code
 