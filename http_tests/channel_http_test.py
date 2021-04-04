import pytest
import requests
import json
from src import config
from src.helper import generate_token

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
    assert test_1.status_code == 400

    # invalid channel user - Input error
    test_2 = requests.post(config.url + 'channel/invite/v2', json={'token': rego_1['token'],\
    'channel_id': new_channel['channel_id'], 'u_id':rego_2['auth_user_id'] + 100})
    assert test_2.status_code == 400

    # invalid inviter - Access error
    test_3 = requests.post(config.url + 'channel/invite/v2', json={'token': rego_2['token'],\
    'channel_id': new_channel['channel_id'], 'u_id':rego_3['auth_user_id']})
    assert test_3.status_code == 403

    # invalid token from logout- Access error
    r = requests.post(config.url + 'auth/logout/v1', json={'token':rego_1['token']})
    test_4 = requests.post(config.url + 'channel/invite/v2', json={'token': rego_1['token'],\
    'channel_id': new_channel['channel_id'], 'u_id':rego_2['auth_user_id']})
    assert test_4.status_code == 403

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

    # invalid new owner - Input error
    test_2 = requests.post(config.url + 'channel/addowner/v1', json={'token': rego_1['token'],\
    'channel_id': new_channel['channel_id'], 'u_id':rego_2['auth_user_id'] + 100})
    assert test_2.status_code == 400

    # invalid current owner - Access error
    test_3 = requests.post(config.url + 'channel/addowner/v1', json={'token': rego_2['token'],\
    'channel_id': new_channel['channel_id'], 'u_id':rego_3['auth_user_id']})
    assert test_3.status_code == 403

    # Successful addition
    test_4 = requests.post(config.url + 'channel/addowner/v1', json={'token': rego_1['token'],\
    'channel_id': new_channel['channel_id'], 'u_id':rego_2['auth_user_id']})
    assert test_4.status_code == 200
    # Correct repeat information - Access error
    test_5 = requests.post(config.url + 'channel/addowner/v1', json={'token': rego_1['token'],\
    'channel_id': new_channel['channel_id'], 'u_id':rego_2['auth_user_id']})
    assert test_5.status_code == 403

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
    assert r.status_code == 403

    # Test the case where you try join a private channel - Expected fobidden 403 (AccessError)
    r = requests.post(config.url + 'channel/join/v2', json = {'token': register1['token'], 'channel_id': private_channel1['channel_id']})
    assert r.status_code == 403

    # Test the case where you try join a private channel - Expected fobidden 400 (InputError)
    r = requests.post(config.url + 'channel/join/v2', json = {'token': register1['token'], 'channel_id': 'channel4'})
    assert r.status_code == 400
