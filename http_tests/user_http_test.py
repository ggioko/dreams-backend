import pytest
import requests
import json
from src import config
from src.helper import generate_token

def test_users_all_v1_successful():
    '''
    Registers some users and provides a valid token to users/all/v1 returning a list of all registered users
    '''
    # Clear register first.
    r = requests.delete(config.url + 'clear/v1')

    # Register users
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    register1 = r.json()

    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail22@gmail.com',
    'password' : '1234abc!@#', 'name_first':'Haydennn', 'name_last':'Everesttt'})
    
    # Call user/all/v1 to get list of users
    r = requests.get(config.url + 'users/all/v1', json={'token': register1['token']})
    user_list = r.json()

    assert user_list['users'] == [
        {'u_id': 1, 'email': 'validemail@gmail.com', 'name_first': 'Hayden', 'name_last': 'Everest', 'handle_str': 'HaydenEverest'},
        {'u_id': 2, 'email': 'validemail22@gmail.com', 'name_first': 'Haydennn', 'name_last': 'Everesttt', 'handle_str': 'HaydennnEveresttt'}
    ]

def test_users_all_v1_invalid_token():
    '''
    Registers some users and provides an invalid token to users/all/v1 returning a fobidden 403 Error (AccessError)
    '''
    # Clear register first.
    r = requests.delete(config.url + 'clear/v1')

    # Register users
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})

    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail22@gmail.com',
    'password' : '1234abc!@#', 'name_first':'Haydennn', 'name_last':'Everesttt'})
    
    # Get a fake token
    invalid_token = generate_token(5)

    # Call user/all/v1 to get list of users
    r = requests.get(config.url + 'users/all/v1', json={'token': invalid_token})

    # Test the case where the token is invalid - Expected fobidden 403 (AccessError)
    assert r.status_code == 403