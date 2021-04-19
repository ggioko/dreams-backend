import pytest
import requests
import json
from src import config
from src.error import AccessError, InputError

def test_standup_start_errors():
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

    r = requests.post(config.url + 'channels/create/v2', json={'token': user_1['token'], 'name': 'Channel1', 'is_public': True})
    channel_1 = r.json()

    # Testing when an invalid token is used
    # expected AccessError
    invalid_token = -1
    r = requests.post(config.url + 'standup/start/v1', json={'token': invalid_token,
    'channel_id' : channel_1['channel_id'], 'length' : 60})
    assert r.status_code == AccessError().code

    # Testing when an invalid Channel id is used
    # expected InputError
    invalid_channel = 56
    r = requests.post(config.url + 'standup/start/v1', json={'token': user_1['token'],
    'channel_id' : invalid_channel, 'length' : 60})
    assert r.status_code == InputError().code

    # Testing when an authorised id is not a member of channel
    # expected AcessError
    r = requests.post(config.url + 'standup/start/v1', json={'token': user_2['token'],
    'channel_id' : channel_1['channel_id'], 'length' : 60})
    assert r.status_code == AccessError().code

    # Testing when a standup is already active in channel
    # expected InputError
    requests.post(config.url + 'standup/start/v1', json={'token': user_1['token'],
    'channel_id' : channel_1['channel_id'], 'length' : 60})
    r = requests.post(config.url + 'standup/start/v1', json={'token': user_1['token'],
    'channel_id' : channel_1['channel_id'], 'length' : 60})
    assert r.status_code == InputError().code

def test_standup_active():
    """
    Testing standup active route given valid data
    """
    # Clear data first
    # Register members
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()

    r = requests.post(config.url + 'channels/create/v2', json={'token': user_1['token'], 'name': 'Channel1', 'is_public': True})
    channel_1 = r.json()

    r = requests.post(config.url + 'standup/start/v1', json={'token': user_1['token'],
    'channel_id' : channel_1['channel_id'], 'length' : 60})
    standup = r.json()

    r = requests.get(config.url + 'standup/active/v1', params={'token': user_1['token'],
    'channel_id' : channel_1['channel_id']}) 
    standup_active = r.json()
    
    standup_active == {'is_active' : True, 'time_finish' : standup['time_finish']}

def test_standup_active_finish():
    """
    Testing standup active route when standup is finished given valid data, 
    """
    # Clear data first
    # Register members
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()

    r = requests.post(config.url + 'channels/create/v2', json={'token': user_1['token'], 'name': 'Channel1', 'is_public': True})
    channel_1 = r.json()

    requests.post(config.url + 'standup/start/v1', json={'token': user_1['token'],
    'channel_id' : channel_1['channel_id'], 'length' : 0})

    r = requests.get(config.url + 'standup/active/v1', params={'token': user_1['token'],
    'channel_id' : channel_1['channel_id']}) 
    standup_active = r.json()
    
    standup_active == {'is_active' : False, 'time_finish' : None}

def test_standup_active_errors():
    """
    Testings for input and access errors 
    """
    # Clear data first
    # Register members
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()

    r = requests.post(config.url + 'channels/create/v2', json={'token': user_1['token'], 'name': 'Channel1', 'is_public': True})
    channel_1 = r.json()

    # Testing when an invalid token is used
    # expected AccessError
    invalid_token = -1
    r = requests.get(config.url + 'standup/active/v1', params={'token': invalid_token,
    'channel_id' : channel_1['channel_id']})
    assert r.status_code == AccessError().code

    # Testing when an invalid channel id is used
    # expected InputError
    invalid_channel_id = 20
    r = requests.get(config.url + 'standup/active/v1', params={'token': user_1['token'],
    'channel_id' : invalid_channel_id})
    assert r.status_code == InputError().code

def test_standup_send_errors():
    """
    Testings for input and access errors 
    """
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

    r = requests.post(config.url + 'channels/create/v2', json={'token': user_1['token'], 'name': 'Channel1', 'is_public': True})
    channel_1 = r.json()

    # Testing when an invalid token is used
    # expected AccessError
    invalid_token = -1
    r = requests.post(config.url + 'standup/send/v1', json={'token': invalid_token,
    'channel_id' : channel_1['channel_id'], 'message' : 'hello'})
    assert r.status_code == AccessError().code

    # Testing when an invalid channel is used
    # expected InputError
    invalid_channel_id = 20
    r = requests.post(config.url + 'standup/send/v1', json={'token': user_1['token'],
    'channel_id' : invalid_channel_id, 'message' : 'hello'})
    assert r.status_code == InputError().code

    # Testing when message is greater than 1000 characters
    # expected InputError
    r = requests.post(config.url + 'standup/send/v1', json={'token': user_1['token'],
    'channel_id' : channel_1['channel_id'], 'message' : 'a'*1100})
    assert r.status_code == InputError().code

    # Testing when an authorised user is not a member of channel
    # expected AccessError
    r = requests.post(config.url + 'standup/send/v1', json={'token': user_2['token'],
    'channel_id' : channel_1['channel_id'], 'message' : 'hello'})
    assert r.status_code == AccessError().code

    # Testing when a active standup is not running in channel
    # expected InputError
    requests.post(config.url + 'standup/start/v1', json={'token': user_1['token'],
    'channel_id' : channel_1['channel_id'], 'length' : 0})

    requests.get(config.url + 'standup/active/v1', params={'token': user_1['token'],
    'channel_id' : channel_1['channel_id']}) 

    r = requests.post(config.url + 'standup/send/v1', json={'token': user_1['token'],
    'channel_id' : channel_1['channel_id'], 'message' : 'hello'})
    assert r.status_code == InputError().code


