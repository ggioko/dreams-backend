#import pytest
import requests
#import json
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
                             'handle_str': 'HaydenEverest'          
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
    
    r3 = requests.get(config.url + 'user/profile/v2', json={'token': user['token'], 'u_id': user['auth_user_id']})
    assert r3.json() == {'user': {
                             'u_id': user['auth_user_id'],
                             'email': 'newemail@gmail.com',
                             'name_first': 'Hayden',
                             'name_last': 'Everest',
                             'handle_str': 'HaydenEverest'          
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
    r = requests.post(config.url + 'auth/register/v2', json={'email':'takenemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    # Invalid email - Input Error
    r = requests.put(config.url + 'user/profile/setemail/v2', json ={'token': user_1['token'], 'email': 'invalidemail.com'})
    assert r.status_code == InputError().code
    # Taken email - Input Error
    r = requests.put(config.url + 'user/profile/setemail/v2', json ={'token': user_1['token'], 'email': user_2['email']})
    assert r.status_code == InputError().code
    # Invalid token - Access Error
    r = requests.put(config.url + 'user/profile/setemail/v2', json ={'token': 'invalid_token', 'email': 'newemail@gmail.com'})
    assert r.status_code == AccessError().code
     
    