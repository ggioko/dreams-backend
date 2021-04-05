import pytest
import requests
import json
from src import config
from src.error import AccessError, InputError
from src.helper import generate_token, get_token_user_id

def test_dm_create():
    """
    A simple test to check dm_create works by passing valid information
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

def test_dm_details():
    """
    A simple test to check dm_details works by passing valid information
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
    dm_1 = r.json()

    r = requests.get(config.url + 'dm/details/v1', params={'token': user_1['token'], 'dm_id': dm_1['dm_id']})
    dm_details_1 = r.json()

    assert dm_details_1['name'] == "bobjones, fredsmith, haydeneverest"
    assert dm_details_1['members'] == [{'u_id': 1, 'email': 'validemail@gmail.com', 'name_first': 'Hayden', 'name_last': 'Everest', 'handle_str': 'haydeneverest',},
                                        {'u_id': 2, 'email': 'secondemail@gmail.com', 'name_first': 'Fred', 'name_last': 'Smith', 'handle_str': 'fredsmith', },
                                        {'u_id': 3, 'email': 'thirdemail@gmail.com', 'name_first': 'Bob', 'name_last': 'Jones', 'handle_str': 'bobjones',}]

def test_dm_details_errors():
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
    r = requests.post(config.url + 'auth/register/v2', json={'email':'fourthemail@gmail.com',
    'password' : '321bca#@!', 'name_first':'Billy', 'name_last':'Elliot'})
    user_4 = r.json()

    # Get user ids from members with helper function
    u_id1 = get_token_user_id(user_2['token'])
    u_id2 = get_token_user_id(user_3['token'])

    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id1, u_id2]})
    dm_1 = r.json()

    # Testing when an invalid token is used
    # expected AccessError
    invalid_token = generate_token(6)
    r = requests.get(config.url + 'dm/details/v1', params={'token': invalid_token, 'dm_id': dm_1['dm_id']})
    assert r.status_code == AccessError().code

    # Testing when an invalid DM ID is used
    # expected InputError
    r = requests.get(config.url + 'dm/details/v1', params={'token': user_1['token'], 'dm_id': 6})
    assert r.status_code == InputError().code

    # Testing when an authorised id is not a member of DM
    # expected AcessError
    r = requests.get(config.url + 'dm/details/v1', params={'token': user_4['token'], 'dm_id': dm_1['dm_id']})
    assert r.status_code == AccessError().code

def test_dm_list():
    """
    A simple test to check dm_details works by passing valid information
    """
    # Clear data first
    requests.delete(config.url + 'clear/v1')
    # Register members
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'thirdemail@gmail.com',
    'password' : '321bca#@!', 'name_first':'Bob', 'name_last':'Jones'})
    user_3 = r.json()
#    r = requests.post(config.url + 'auth/register/v2', json={'email':'fourthemail@gmail.com',
#    'password' : '321bca#@!', 'name_first':'Billy', 'name_last':'Elliot'})
#    user_4 = r.json()
    
    # Get user ids from members with helper function
    u_id1 = get_token_user_id(user_1['token'])
    u_id2 = get_token_user_id(user_2['token'])
    u_id3 = get_token_user_id(user_3['token'])

    r1 = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id2, u_id3]})
    new_dm = r1.json()
    r2 = requests.post(config.url + 'dm/create/v1',  json={'token': user_2['token'], 'u_ids': [u_id1]})
    new_dm_2 = r2.json()
    r = requests.get(config.url + 'dm/list/v1',  params={'token': user_1['token']})
    assert r.json() == {
        'dms': [
        {
                'dm_id': new_dm['dm_id'], 
                'name': new_dm['dm_name']
        },
        {
                'dm_id': new_dm_2['dm_id'],
                'name': new_dm_2['dm_name']
        }
        ],
    }


def test_dm_list_error():
    """
    Test for AccessError
    """
    # Clear data first
    requests.delete(config.url + 'clear/v1')
    # Call dm/list/v1 with an invalid token
    r = requests.get(config.url + 'dm/list/v1',  params={'token': 'invalid_token'})
    assert r.status_code == AccessError().code
    
