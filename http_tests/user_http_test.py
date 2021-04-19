import pytest
import requests
import json
from src import config
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
    r2 = requests.get(config.url + 'user/profile/v2', params={'token': user['token'], 'u_id': user['auth_user_id']})
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
    r = requests.get(config.url + 'user/profile/v2', params={'token': user['token'], 'u_id': 50})
    assert r.status_code == InputError().code
    r = requests.get(config.url + 'user/profile/v2', params={'token': -1, 'u_id': user['auth_user_id']})
    assert r.status_code == AccessError().code
 

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
    r = requests.get(config.url + 'users/all/v1', params={'token': register1['token']})
    user_list = r.json()

    assert user_list['users'] == [
        {'u_id': 1, 'email': 'validemail@gmail.com', 'name_first': 'Hayden', 'name_last': 'Everest', 'handle_str': 'haydeneverest'},
        {'u_id': 2, 'email': 'validemail22@gmail.com', 'name_first': 'Haydennn', 'name_last': 'Everesttt', 'handle_str': 'haydennneveresttt'}
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
    invalid_token = -1

    # Call user/all/v1 to get list of users
    r = requests.get(config.url + 'users/all/v1', params={'token': invalid_token})

    # Test the case where the token is invalid - Expected fobidden 403 (AccessError)
    assert r.status_code == AccessError().code

def test_user_profile_setemail():
    '''
    Register a user and calls user/profile/setemail/v2 to change email successfully.
    '''
    # Clear data first.
    requests.delete(config.url + 'clear/v1')
    # Register a user
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user = r.json()
    requests.put(config.url + 'user/profile/setemail/v2', json ={'token': user['token'], 'email': 'newemail@gmail.com'})
    
    r3 = requests.get(config.url + 'user/profile/v2', params={'token': user['token'], 'u_id': user['auth_user_id']})
    assert r3.json() == {'user': {
                             'u_id': user['auth_user_id'],
                             'email': 'newemail@gmail.com',
                             'name_first': 'Hayden',
                             'name_last': 'Everest',
                             'handle_str': 'haydeneverest'          
    }}


def test_user_profile_setemail_errors():
    '''
    Checks the InputError (400) and AccessError (403) cases.
    '''
    # Clear data first.
    requests.delete(config.url + 'clear/v1')
    # Register some users
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    requests.post(config.url + 'auth/register/v2', json={'email':'takenemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Fred', 'name_last':'Smith'})

    # Invalid email - Input Error
    r = requests.put(config.url + 'user/profile/setemail/v2', json ={'token': user_1['token'], 'email': 'invalidemail.com'})
    assert r.status_code == InputError().code
    # Taken email - Input Error
    r = requests.put(config.url + 'user/profile/setemail/v2', json ={'token': user_1['token'], 'email': 'takenemail@gmail.com'})
    assert r.status_code == InputError().code
    # Invalid token - Access Error
    r = requests.put(config.url + 'user/profile/setemail/v2', json ={'token': 'invalid_token', 'email': 'newemail@gmail.com'})
    assert r.status_code == AccessError().code
     
def test_user_profile_setname():
    '''
    Register a user and calls user/profile/setname/v2 to change name successfully.
    '''
    # Clear data first.
    requests.delete(config.url + 'clear/v1')
    # Register a user
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user = r.json()
    requests.put(config.url + 'user/profile/setname/v2', json ={'token': user['token'], 'name_first': 'Fred', 'name_last': 'Smith'})
    
    r3 = requests.get(config.url + 'user/profile/v2', params={'token': user['token'], 'u_id': user['auth_user_id']})
    assert r3.json() == {'user': {
                             'u_id': user['auth_user_id'],
                             'email': 'validemail@gmail.com',
                             'name_first': 'Fred',
                             'name_last': 'Smith',
                             'handle_str': 'haydeneverest'          
    }}

def test_user_profile_setname_errors():
    '''
    Checks the InputError (400) and AccessError (403) cases.
    '''
    # Clear data first.
    requests.delete(config.url + 'clear/v1')
    # Register user
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user = r.json()

    # Invalid token - Access Error
    r = requests.put(config.url + 'user/profile/setname/v2', json ={'token': 'invalid_token', 'name_first': 'Fred', 'name_last': 'Smith'})
    assert r.status_code == AccessError().code     
    # Invalid name_first - Input Error
    r = requests.put(config.url + 'user/profile/setname/v2', json ={'token': user['token'], 'name_first': 'asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2', 'name_last': 'Smith'})
    assert r.status_code == InputError().code 
    # Invalid name_last - Input Error
    r = requests.put(config.url + 'user/profile/setname/v2', json ={'token': user['token'], 'name_first': 'Fred', 'name_last': 'asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2'})
    assert r.status_code == InputError().code 
    
def test_user_profile_sethandle():
    '''
    Register a user and calls user/profile/sethandle/v1 to change handle successfully.
    '''
    # Clear data first.
    requests.delete(config.url + 'clear/v1')
    # Register a user
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user = r.json()
    requests.put(config.url + 'user/profile/sethandle/v1', json ={'token': user['token'], 'handle_str': 'newhandle'})
    
    r3 = requests.get(config.url + 'user/profile/v2', params={'token': user['token'], 'u_id': user['auth_user_id']})
    assert r3.json() == {'user': {
                             'u_id': user['auth_user_id'],
                             'email': 'validemail@gmail.com',
                             'name_first': 'Hayden',
                             'name_last': 'Everest',
                             'handle_str': 'newhandle'          
    }}

    
def test_user_profile_sethandle_errors():
    '''
    Checks the InputError (400) and AccessError (403) cases.
    '''
    # Clear data first.
    requests.delete(config.url + 'clear/v1')
    # Register some users
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    requests.post(config.url + 'auth/register/v2', json={'email':'takenemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Fred', 'name_last':'Smith'})
       
    # Invalid token - Access Error
    r = requests.put(config.url + 'user/profile/sethandle/v1', json ={'token': 'invalid_token', 'handle_str': 'newhandle'})
    assert r.status_code == AccessError().code 
    # Invalid email - Input Error
    r = requests.put(config.url + 'user/profile/sethandle/v1', json ={'token': user_1['token'], 'handle_str': 'thishandleislongerthantwentycharacters'})
    assert r.status_code == InputError().code
    # Taken handle - Input Error
    r = requests.put(config.url + 'user/profile/sethandle/v1', json ={'token': user_1['token'], 'handle_str': 'fredsmith'})
    assert r.status_code == InputError().code

def test_user_http_stats_invalidtoken():
    '''
    Check if access error is raised for invalid token
    '''
    # Clear data first.
    requests.delete(config.url + 'clear/v1')

    # Register some users
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})

    # Access Error
    r = requests.get(config.url + '/user/stats/v1', params ={'token': 2})
    assert r.status_code == AccessError().code

def test_user_http_stats_dreams():
    '''
    Check if stats dreams works correctly
    '''
    # Clear data first.
    requests.delete(config.url + 'clear/v1')

    # Register users
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user = r.json()
    requests.post(config.url + 'auth/register/v2', json={'email':'validemail2@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    
    # Create a channel
    requests.post(config.url + 'channels/create/v2', json = {'token': user['token'], 'name': 'Channel1', 'is_public': True})

    # Access Error
    r = requests.get(config.url + '/user/stats/v1', params ={'token': user['token']})
    stats = r.json()
    assert stats['channels_exist']['num_channels_exist'] == 1
    assert stats['dms_exist']['num_dms_exist'] == 0
    assert stats['messages_exist']['num_messages_exist'] == 0
    assert stats['utilization_rate'] == 0.5