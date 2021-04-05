import pytest
import requests
import json
from src import config
from src.error import AccessError, InputError
from src.helper import generate_token, get_token_user_id

def test_channels_create():
    """
    A simple test to check channels_create works by passing valid information
    """
    # Clear data first
    # Register members
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'thirdemail@gmail.com',
    'password' : '321bca#@!', 'name_first':'Bob', 'name_last':'Jones'})
    user_3 = r.json()

    # Get user ids from members with helper function
    u_id1 = get_token_user_id(user_2['token'])
    u_id2 = get_token_user_id(user_3['token'])

    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id1, u_id2]})
    print(r.status_code)
    assert r.json() == {'dm_id' : 1, 'dm_name' : "bobjones, fredsmith, haydeneverest"}

def test_dm_create_errors():
    """
    Testings for input and access errors 
    """
    # Clear data first
    # Register members
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'thirdemail@gmail.com',
    'password' : '321bca#@!', 'name_first':'Bob', 'name_last':'Jones'})
    user_3 = r.json()

    # Get user ids from members with helper function
    u_id1 = get_token_user_id(user_2['token'])
    u_id2 = get_token_user_id(user_3['token'])

    # Test the case where the token is invalid
    # Expected forbidden AccessError
    invalid_token = generate_token(4)
    r = requests.post(config.url + 'dm/create/v1',  json={'token': invalid_token, 'u_ids': [u_id1, u_id2]})
    assert r.status_code == AccessError().code

    # Testing when an u_id does not refer to a valid member
    # Expected bad request InputError
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id1, u_id2, 6]})
    assert r.status_code == InputError().code