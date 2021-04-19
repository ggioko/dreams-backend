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
