import pytest
import requests
import json
from src import config
from src.helper import generate_token

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

    r = requests.post(config.url + 'channels/create/v2', json = {'token': register1['token'], 'name': 'Channel1', 'is_public': True})
    channel1 = r.json()

    # Test the case where the token is invalid - Expected fobidden 403 (AccessError)
    invalid_token = generate_token(4)
    r = requests.get(config.url + 'channel/messages/v2', json={'token': invalid_token, 'channel_id': channel1['channel_id'], 'start': 0})
    assert r.status_code == 403

    # Test the case where the registered user is not a member of the channel - Expected fobidden 403 (AccessError)
    r = requests.get(config.url + 'channel/messages/v2', json={'token': register2['token'], 'channel_id': channel1['channel_id'], 'start': 0})
    assert r.status_code == 403

    # Test the case where the channel_id is not valid - Expected bad request 400 (InputError)
    r = requests.get(config.url + 'channel/messages/v2', json={'token': register1['token'], 'channel_id': 20, 'start': 0})
    assert r.status_code == 400

    # Test the case where the start is greater than the total number of messages in the channel - Expected bad request 400 (InputError)
    r = requests.get(config.url + 'channel/messages/v2', json={'token': register1['token'], 'channel_id': channel1['channel_id'], 'start': 50})
    assert r.status_code == 403