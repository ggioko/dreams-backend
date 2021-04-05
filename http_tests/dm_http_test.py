import pytest
import requests
import json
from src import config
from src.error import AccessError, InputError

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
    u_id1 = user_2['auth_user_id']
    u_id2 = user_3['auth_user_id']

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

    # Get user ids 
    u_id1 = user_2['auth_user_id']
    u_id2 = user_3['auth_user_id']

    # Test the case where the token is invalid
    # Expected forbidden AccessError
    r = requests.post(config.url + 'dm/create/v1',  json={'token': -1, 'u_ids': [u_id1, u_id2]})
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

    # Get user ids
    u_id1 = user_2['auth_user_id']
    u_id2 = user_3['auth_user_id']

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
    Testing for input and access errors 
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

    # Get user ids
    u_id1 = user_2['auth_user_id']
    u_id2 = user_3['auth_user_id']

    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id1, u_id2]})
    dm_1 = r.json()

    # Testing when an invalid token is used
    # expected AccessError
    r = requests.get(config.url + 'dm/details/v1', params={'token': -1, 'dm_id': dm_1['dm_id']})
    assert r.status_code == AccessError().code

    # Testing when an invalid DM ID is used
    # expected InputError
    r = requests.get(config.url + 'dm/details/v1', params={'token': user_1['token'], 'dm_id': 6})
    assert r.status_code == InputError().code

    # Testing when an authorised id is not a member of DM
    # expected AcessError
    r = requests.get(config.url + 'dm/details/v1', params={'token': user_4['token'], 'dm_id': dm_1['dm_id']})
    assert r.status_code == AccessError().code

def test_dm_leave():
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

    # Get user ids from members
    u_id1 = user_2['auth_user_id']
    u_id2 = user_3['auth_user_id']
    # create a DM
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id1, u_id2]})
    dm_1 = r.json()
    # remove user_3
    r = requests.post(config.url + 'dm/leave/v1',  json={'token': user_3['token'], 'dm_id': dm_1['dm_id']})
    # get details of DM
    r = requests.get(config.url + 'dm/details/v1', params={'token': user_1['token'], 'dm_id': dm_1['dm_id']})
    dm_details_1 = r.json()

    assert dm_details_1['members'] == [{'u_id': 1, 'email': 'validemail@gmail.com', 'name_first': 'Hayden', 'name_last': 'Everest', 'handle_str': 'haydeneverest',},
                                        {'u_id': 2, 'email': 'secondemail@gmail.com', 'name_first': 'Fred', 'name_last': 'Smith', 'handle_str': 'fredsmith', },]

def test_dm_leave_errors():
    """
    Testing for input and access errors 
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
    'password' : '321bca#@!', 'name_first':'Jamie', 'name_last':'Oliver'})
    user_4 = r.json()

    # Get user ids from members
    u_id1 = user_2['auth_user_id']
    u_id2 = user_3['auth_user_id']
    # create a DM
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id1, u_id2]})
    dm_1 = r.json()

    # Testing when an invalid token is used
    # expected AccessError
    r = requests.post(config.url + 'dm/leave/v1',  json={'token': -1, 'dm_id': dm_1['dm_id']})
    assert r.status_code == AccessError().code

    # Testing when an invalid DM ID is used
    # expected InputError
    r = requests.post(config.url + 'dm/leave/v1',  json={'token': user_3['token'], 'dm_id': 6})
    assert r.status_code == InputError().code

    # Testing when an authorised id is not a member of DM
    # expected AcessError
    r = requests.post(config.url + 'dm/leave/v1',  json={'token': user_4['token'], 'dm_id': dm_1['dm_id']})
    assert r.status_code == AccessError().code
    
def test_dm_remove_http_valid():
    """
    Testings dm remove by making sure the dm_id is invalid in dm_details
    """
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()

    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [user_2['auth_user_id']]})
    dm_1 = r.json()

    # Checks if DM exists
    r = requests.get(config.url + 'dm/details/v1', params={'token': user_1['token'], 'dm_id': dm_1['dm_id']})
    assert r.status_code == 200

    requests.delete(config.url + 'dm/remove/v1',  json={'token': user_1['token'], 'dm_id': dm_1['dm_id']})

    # Checks if DM no longer exists
    r = requests.get(config.url + 'dm/details/v1', params={'token': user_1['token'], 'dm_id': dm_1['dm_id']})
    assert r.status_code == InputError().code

def test_dm_remove_http_invalid_dm_id():
    """
    Testings dm remove input error by passing in an invalid dm_id
    """
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()

    r = requests.delete(config.url + 'dm/remove/v1',  json={'token': user_1['token'], 'dm_id': -1})
    assert r.status_code == InputError().code

def test_dm_remove_http_non_owner():
    """
    Testings dm remove input error by passing non owner token
    """
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()

    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [user_2['auth_user_id']]})
    dm_1 = r.json()

    r = requests.delete(config.url + 'dm/remove/v1',  json={'token': user_2['token'], 'dm_id': dm_1['dm_id']})
    assert r.status_code == AccessError().code
