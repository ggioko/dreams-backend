import pytest
import requests
import json
from src import config
from src.error import InputError, AccessError

def test_auth_register():
    '''
    A test to check if auth_register works by passing in valid information
    '''
    # Clear data and register users
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'valid2email@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Bob', 'name_last':'Jones'})
    user_2 = r.json()

    assert user_1['auth_user_id'] == 1
    assert user_2['auth_user_id'] == 2

    
def test_auth_register_errors():
    '''
    Testing for input and access errors
    '''    
    requests.delete(config.url + 'clear/v1')

    # Test for if password is less than 6 characters
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123', 'name_first':'Hayden', 'name_last':'Everest'}) 
    assert r.status_code == InputError().code

    # Test for if first name or last name is between 1 to 50 characters
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Haydenaydenaydenaydenaydenaydenaydenaydenaydenayden', 'name_last':'Everest'}) 
    assert r.status_code == InputError().code

    # Test for if email is not in right format
    r = requests.post(config.url + 'auth/register/v2', json={'email':'com.validemail@gmail', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'}) 
    assert r.status_code == InputError().code

    # Test for if email is already in use
    requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123', 'name_first':'Hayden', 'name_last':'Everest'}) 

    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123', 'name_first':'Bob', 'name_last':'Jones'})
    assert r.status_code == InputError().code

def test_auth_passwordreset_reset_erros():
    '''
    Testing for input erros in password reset
    '''    
    requests.delete(config.url + 'clear/v1')

    # Test for if password is less than 6 characters
    r = requests.post(config.url + 'auth/passwordreset/reset/v1', json={'reset_code':'abcd', \
    'password' : '123',}) 
    assert r.status_code == InputError().code

    # Test for if reset_code is invalid
    r = requests.post(config.url + 'auth/passwordreset/reset/v1', json={'reset_code':'abcd', \
    'password' : '123absdhjj',}) 
    assert r.status_code == InputError().code
