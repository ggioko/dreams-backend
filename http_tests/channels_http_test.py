import pytest
import requests
import json
from src import config
from src.helper import generate_token

def test_channels_create():
    """
    A simple test to check channels_create works by passing valid information
    """
    # Clear data first
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    register1 = r.json()
    r = requests.post(config.url + 'channels/create/v2',  json={'token': register1['token'], 'name': 'channel1', 'is_public': True})
    assert r.json() == {'channel_id' : 1}

def test_channels_create_errors():
    """
    Testings for input and access errors 
    """
    # Clear data first
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    register1 = r.json()

    # Test the case where the channel name is more than 20 characters
    # Expected bad request 400
    r = requests.post(config.url + 'channels/create/v2',  json={'token': register1['token'], 'name': 'nameislonger20characters', 'is_public': True})
    assert r.status_code == 400

    # Test the case where is_public is not of type bool
    # Expected bad request 400
    r = requests.post(config.url + 'channels/create/v2',  json={'token': register1['token'], 'name': 'channel1', 'is_public': 20})
    assert r.status_code == 400


    # Test the case where the token is invalid
    # Ezpected fobidden 403
    invalid_token = generate_token(4)
    r = requests.post(config.url + 'channels/create/v2',  json={'token': invalid_token, 'name': 'channel1', 'is_public': True})
    assert r.status_code == 403

