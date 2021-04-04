import pytest
import requests
import json
from src import config
from src.helper import generate_token
from src.error import AccessError, InputError

def test_channel_details():
    """
    Test to check if channel/details/v2 works by passing in valid information.
    """
    # Clear register first.
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json = {'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    # Create 3 users
    rego_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json = {'email':'validemail2@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Fred', 'name_last':'Smith'})
    rego_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json = {'email':'validemail3@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Angus', 'name_last':'Young'})
    rego_3 = r.json()


    r = requests.post(config.url + 'channels/create/v2', json = {'token': rego_1['token'], 'name': 'Channel1', 'is_public': True})
    new_channel = r.json()
    

    
    requests.post(config.url + 'channel/join/v2', json = {'token': rego_2['token'], 'channel_id': new_channel['channel_id']})
    requests.post(config.url + 'channel/join/v2', json = {'token': rego_3['token'], 'channel_id': new_channel['channel_id']})
    
    # system test
    test_4 = requests.get(config.url + 'channel/details/v2', params = {'token': rego_1['token'], 'channel_id': 1})
    payload_4 = test_4.json()
    

    
    correct = 0
    if payload_4['name'] == 'Channel1':
        if len(payload_4['owner_members']) == 1:
            if len(payload_4['all_members']) == 3: #Changed this from 4 to 3 and got rid of rego_4 in line 22-24.
                correct = 1
    assert correct == 1 


def test_channel_details_errors():
    """
    Test to check if the various exception cases work for channel/details/v2.
    """
    # Clear register first.
    requests.delete(config.url + 'clear/v1')
    # Create 4 users
    r = requests.post(config.url + 'auth/register/v2', json = {'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    rego_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json = {'email':'validemail2@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Fred', 'name_last':'Smith'})
    rego_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json = {'email':'validemail3@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Angus', 'name_last':'Young'})
    rego_3 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json = {'email':'validemail4@gmail.com', \
    'password' : '123abc!@#', 'name_first':'James', 'name_last':'Taylor'})
    rego_4 = r.json()
    # Create new channel 'Channel1' using rego_1.
    r = requests.post(config.url + 'channels/create/v2', json = {'token': rego_1['token'], 'name': 'Channel1', 'is_public': True})
    new_channel = r.json()
    requests.post(config.url + 'channel/join/v2', json = {'token': rego_2['token'], 'channel_id': new_channel['channel_id']})
    requests.post(config.url + 'channel/join/v2', json = {'token': rego_3['token'], 'channel_id': new_channel['channel_id']})
    
    # invalid channel id - Input Error
    test_1 = requests.get(config.url + 'channel/details/v2', params = {'token': rego_1['token'], 'channel_id': -1})
    assert test_1.status_code == InputError().code
    # unauthorised user - Access Error
    test_2 = requests.get(config.url + 'channel/details/v2', params = {'token': rego_4['token'], 'channel_id': new_channel['channel_id']})
    assert test_2.status_code == AccessError().code
    # invalid user - Access Error
    test_3 = requests.get(config.url + 'channel/details/v2', params = {'token': 'invalid_user', 'channel_id': new_channel['channel_id']})
    assert test_3.status_code == AccessError().code


def test_channel_invite():
    """
    Tests to see if channel_invite_v2 is working as intended
    """
    # Clear register:
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'madladadmin@gmail.com',\
    'password':'123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    rego_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'peasantuser@gmail.com',\
    'password':'diffpassword!', 'name_first':'Everest', 'name_last':'Hayden'})
    rego_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail3@gmail.com',\
    'password':'123abcd!@#', 'name_first':'Haydeen', 'name_last':'Everesst'})
    rego_3 = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token':rego_1['token'],\
    'name':'dankmemechannel', 'is_public':False})
    new_channel = r.json()

    # invalid channel id - Input error
    test_1 = requests.post(config.url + 'channel/invite/v2', json={'token': rego_1['token'],\
    'channel_id': new_channel['channel_id'] + 1, 'u_id':rego_2['auth_user_id']})
    assert test_1.status_code == InputError().code

    # invalid channel user - Input error
    test_2 = requests.post(config.url + 'channel/invite/v2', json={'token': rego_1['token'],\
    'channel_id': new_channel['channel_id'], 'u_id':rego_2['auth_user_id'] + 100})
    assert test_2.status_code == InputError().code

    # invalid inviter - Access error
    test_3 = requests.post(config.url + 'channel/invite/v2', json={'token': rego_2['token'],\
    'channel_id': new_channel['channel_id'], 'u_id':rego_3['auth_user_id']})
    assert test_3.status_code == AccessError().code

    # invalid token from logout- Access error
    r = requests.post(config.url + 'auth/logout/v1', json={'token':rego_1['token']})
    test_4 = requests.post(config.url + 'channel/invite/v2', json={'token': rego_1['token'],\
    'channel_id': new_channel['channel_id'], 'u_id':rego_2['auth_user_id']})
    assert test_4.status_code == AccessError().code

def test_channel_addowner():
    """
    Tests to see if channel_addowner_v1 is working as intended
    """
    # Clear register:
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'madladadmin@gmail.com',\
    'password':'123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    rego_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'peasantuser@gmail.com',\
    'password':'diffpassword!', 'name_first':'Everest', 'name_last':'Hayden'})
    rego_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail3@gmail.com',\
    'password':'123abcd!@#', 'name_first':'Haydeen', 'name_last':'Everesst'})
    rego_3 = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token':rego_1['token'],\
    'name':'dankmemechannel', 'is_public':False})
    new_channel = r.json()

    # invalid channel id - Input error
    test_1 = requests.post(config.url + 'channel/addowner/v1', json={'token': rego_1['token'],\
    'channel_id': new_channel['channel_id'] + 1, 'u_id':rego_2['auth_user_id']})
    assert test_1.status_code == InputError().code

    # invalid new owner - Input error
    test_2 = requests.post(config.url + 'channel/addowner/v1', json={'token': rego_1['token'],\
    'channel_id': new_channel['channel_id'], 'u_id':rego_2['auth_user_id'] + 100})
    assert test_2.status_code == InputError().code

    # invalid current owner - Access error
    test_3 = requests.post(config.url + 'channel/addowner/v1', json={'token': rego_2['token'],\
    'channel_id': new_channel['channel_id'], 'u_id':rego_3['auth_user_id']})
    assert test_3.status_code == AccessError().code 

    # Successful addition
    test_4 = requests.post(config.url + 'channel/addowner/v1', json={'token': rego_1['token'],\
    'channel_id': new_channel['channel_id'], 'u_id':rego_2['auth_user_id']})
    assert test_4.status_code == 200
    # Correct repeat information - Access error
    test_5 = requests.post(config.url + 'channel/addowner/v1', json={'token': rego_1['token'],\
    'channel_id': new_channel['channel_id'], 'u_id':rego_2['auth_user_id']})
    assert test_5.status_code == AccessError().code

def test_channel_join_errors():
    """
    Testings for input and access errors 
    """
    # Clear register first.
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    register1 = r.json()
    
    r = requests.post(config.url + 'auth/register/v2', json = {'email':'validemail3@gmail.com',
    'password' : '123abc!@#', 'name_first':'Angus', 'name_last':'Young'})
    register3 = r.json()

    r = requests.post(config.url + 'channels/create/v2', json = {'token': register1['token'], 'name': 'Channel1', 'is_public': True})
    public_channel1 = r.json()

    r = requests.post(config.url + 'channels/create/v2', json = {'token': register3['token'], 'name': 'Channel1', 'is_public': False})
    private_channel1 = r.json()

    invalid_token = generate_token(5)

    # Test the case where the token is invalid - Expected fobidden 403 (AccessError)
    r = requests.post(config.url + 'channel/join/v2', json = {'token': invalid_token, 'channel_id': public_channel1['channel_id']})
    assert r.status_code == AccessError().code

    # Test the case where you try join a private channel - Expected fobidden 403 (AccessError)
    r = requests.post(config.url + 'channel/join/v2', json = {'token': register1['token'], 'channel_id': private_channel1['channel_id']})
    assert r.status_code == AccessError().code

    # Test the case where you try join a private channel - Expected fobidden 400 (InputError)
    r = requests.post(config.url + 'channel/join/v2', json = {'token': register1['token'], 'channel_id': 'channel4'})
    assert r.status_code == InputError().code

def test_channel_messages():
    """
    A simple test to see if channel_messages works by passing valid information
    """
    # Clear register first.
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    register1 = r.json()

    r = requests.post(config.url + 'channels/create/v2', json={'token': register1['token'], 'name': 'channel1', 'is_public': True})
    channel1 = r.json()
    assert requests.get(config.url + 'channel/messages/v2', params={'token': register1['token'], 'channel_id': channel1['channel_id'], 'start': 0})
    

def test_channel_messages_errors():
    """
    Testings for input and access errors 
    """
    # Clear register first.
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    register1 = r.json()
    
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail3@gmail.com',
    'password' : '123abc!@#', 'name_first':'Angus', 'name_last':'Young'})
    register2 = r.json()

    r = requests.post(config.url + 'channels/create/v2', json={'token': register1['token'], 'name': 'Channel1', 'is_public': True})
    channel1 = r.json()
    
    # Test the case where the token is invalid - Expected fobidden 403 (AccessError)
    invalid_token = generate_token(4)
    r = requests.get(config.url + 'channel/messages/v2', params={'token': invalid_token, 'channel_id': channel1['channel_id'], 'start': 0})
    assert r.status_code == AccessError().code

    # Test the case where the registered user is not a member of the channel - Expected fobidden 403 (AccessError)
    r = requests.get(config.url + 'channel/messages/v2', params={'token': register2['token'], 'channel_id': channel1['channel_id'], 'start': 0})
    assert r.status_code == AccessError().code

    # Test the case where the channel_id is not valid - Expected bad request 400 (InputError)
    r = requests.get(config.url + 'channel/messages/v2', params={'token': register1['token'], 'channel_id': 20, 'start': 0})
    assert r.status_code == InputError().code

    # Test the case where the start is greater than the total number of messages in the channel - Expected bad request 400 (InputError)
    r = requests.get(config.url + 'channel/messages/v2', params={'token': register1['token'], 'channel_id': channel1['channel_id'], 'start': 50})
    assert r.status_code == InputError().code
