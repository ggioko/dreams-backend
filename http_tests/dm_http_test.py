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


def test_dm_list():

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
    
    # Get user ids
    u_id1 = user_1['auth_user_id']
    u_id2 = user_2['auth_user_id']
    u_id3 = user_3['auth_user_id']

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
    

def test_dm_leave():
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


def test_dm_invite_http_valid():
    """
    Test to see if dm invite works by inviting a user then
    them calling dm_details 
    """
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

    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [user_2['auth_user_id']]})
    dm_1 = r.json()

    requests.post(config.url + 'dm/invite/v1',  json={'token': user_1['token'],'dm_id' : dm_1['dm_id'] ,'u_id': user_3['auth_user_id']})
    
    assert requests.get(config.url + 'dm/details/v1', params={'token': user_3['token'], 'dm_id': dm_1['dm_id']})


def test_dm_invite_http_invalid_dm_id():
    """
    Test to see if dm invite raises input error by passing in
    an invalid DM ID 
    """
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

    requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [user_2['auth_user_id']]})

    r = requests.post(config.url + 'dm/invite/v1',  json={'token': user_1['token'],'dm_id' : 33 ,'u_id': user_3['auth_user_id']})
    assert r.status_code == InputError().code


def test_dm_invite_http_invalid_u_id():
    """
    Test to see if dm invite raises input error by passing in
    an invalid User ID 
    """
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    requests.post(config.url + 'auth/register/v2', json={'email':'thirdemail@gmail.com',
    'password' : '321bca#@!', 'name_first':'Bob', 'name_last':'Jones'})
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [user_2['auth_user_id']]})
    dm_1 = r.json()

    r = requests.post(config.url + 'dm/invite/v1',  json={'token': user_1['token'],'dm_id' : dm_1['dm_id'] ,'u_id': 33})
    assert r.status_code == InputError().code


def test_dm_invite_http_invalid_token():
    """
    Test to see if dm invite raises access error by passing in
    an invalid token
    """
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    requests.post(config.url + 'auth/register/v2', json={'email':'thirdemail@gmail.com',
    'password' : '321bca#@!', 'name_first':'Bob', 'name_last':'Jones'})
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [user_2['auth_user_id']]})
    dm_1 = r.json()

    r = requests.post(config.url + 'dm/invite/v1',  json={'token': 22,'dm_id' : dm_1['dm_id'] ,'u_id': 33})
    assert r.status_code == AccessError().code

def test_dm_invite_http_non_member():
    """
    Test to see if dm invite raises access error when a user
    who is not a member of the dm tries to invite someone
    """
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
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [user_2['auth_user_id']]})
    dm_1 = r.json()

    r = requests.post(config.url + 'dm/invite/v1',  json={'token': user_3['token'],'dm_id' : dm_1['dm_id'] ,'u_id': user_1['auth_user_id']})
    assert r.status_code == AccessError().code

def test_dm_messages_http_invalid_token():
    """
    Test to see if dm messages raises access error by passing in
    an invalid token
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
    r = requests.get(config.url + 'dm/messages/v1',  params={'token': 1, 'dm_id': dm_1['dm_id'], 'start' : 0})
    assert r.status_code == AccessError().code
    
def test_dm_messages_http_invalid_dm_id():
    """
    Test to see if dm messages raises input error by passing in
    an invalid DM ID
    """
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [user_2['auth_user_id']]})
    r = requests.get(config.url + 'dm/messages/v1',  params={'token': user_1['token'], 'dm_id': 33, 'start' : 0})
    assert r.status_code == InputError().code

def test_dm_messages_http_invalid_start():
    """
    Test to see if dm messages raises input error by passing in
    an invalid start index
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
    r = requests.get(config.url + 'dm/messages/v1',  params={'token': user_1['token'], 'dm_id': dm_1['dm_id'], 'start' : 33})
    assert r.status_code == InputError().code

def test_dm_messages_http_unauthorised_user():
    """
    Test to see if dm messages raises access error when a user
    who is not a member of the dm calls the function
    """
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'thirdemail@gmail.com',
    'password' : '321bca#@!', 'name_first':'Bob', 'name_last':'Jones'})
    user_3 = r.json()
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [user_2['auth_user_id']]})
    dm_1 = r.json()
    r = requests.get(config.url + 'dm/messages/v1',  params={'token': user_3['token'], 'dm_id': dm_1['dm_id'], 'start' : 0})
    assert r.status_code == AccessError().code

def test_dm_messages_http_valid():
    """
    Test to see if dm messages works with valid data
    """
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'thirdemail@gmail.com',
    'password' : '321bca#@!', 'name_first':'Bob', 'name_last':'Jones'})
    user_3 = r.json()
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [user_2['auth_user_id'], user_3['auth_user_id']]})
    dm_1 = r.json()
    message_1 = "My first message"
    message_2 = "My second message"

    r = requests.post(config.url + 'message/senddm/v1', json={'token': user_1['token'], 'dm_id': dm_1['dm_id'], 'message' : message_1})
    m_1 = r.json()
    r = requests.post(config.url + 'message/senddm/v1', json={'token': user_2['token'], 'dm_id': dm_1['dm_id'], 'message' : message_2})
    m_2 = r.json()

    r = requests.get(config.url + 'dm/messages/v1',  params={'token': user_3['token'], 'dm_id': dm_1['dm_id'], 'start' : 0})
    output = r.json()
    
    message_list = output['messages']
    req_info = message_list[0]
    assert req_info[1]['message_id'] == m_1['message_id']
    assert req_info[1]['u_id'] == user_1['auth_user_id']
    assert req_info[1]['message'] == message_1
    assert req_info[0]['message_id'] == m_2['message_id']
    assert req_info[0]['u_id'] == user_2['auth_user_id']
    assert req_info[0]['message'] == message_2
    assert output['start'] == 0
    assert output['end'] == -1

