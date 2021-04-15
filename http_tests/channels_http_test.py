import pytest
import requests
import json
from src import config
from src.error import AccessError, InputError

def test_channels_listall_v2_runs():
    '''
    A check to see if listall runs correctly with no channels
    '''
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    token = json.loads(resp.text)
    resp = requests.get(config.url + 'channels/listall/v2', params={'token': token['token']})
    assert json.loads(resp.text) == {'channels': []}

def test_channels_listall_v2_check():
    '''
    A check to see if listall runs correctly with two channels.
    A user is registered and their token is used to create two
    channels which are then used to check if list all works.
    '''
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    token = json.loads(resp.text)
    name = "My Channel"
    name_2 = "My second Channel"
    requests.post(config.url + 'channels/create/v2', json={'token': token['token'], 'name' : name, \
    'is_public' : True})
    requests.post(config.url + 'channels/create/v2', json={'token': token['token'], 'name' : name_2, \
    'is_public' : True})
    resp = requests.get(config.url + 'channels/listall/v2', params={'token': token['token']})
    channels = [json.loads(resp.text)['channels'][c]['name'] for c in range(len(json.loads(resp.text)['channels']))]
    assert name in channels
    assert name_2 in channels

def test_channels_listall_v2_access_error():
    """
    Test to see if listall raises access error when passed in an invalid token
    """
    r = requests.get(config.url + 'channels/listall/v2', params={'token': -1})
    assert r.status_code == AccessError().code

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
    # Expected bad request InputError
    r = requests.post(config.url + 'channels/create/v2',  json={'token': register1['token'], 'name': 'nameislonger20characters', 'is_public': True})
    assert r.status_code == InputError().code

    # Test the case where is_public is not of type bool
    # Expected bad request InputError
    r = requests.post(config.url + 'channels/create/v2',  json={'token': register1['token'], 'name': 'channel1', 'is_public': 20})
    assert r.status_code == InputError().code

    # Test the case where the token is invalid
    # Expected forbidden AccessError
    invalid_token = -1
    r = requests.post(config.url + 'channels/create/v2',  json={'token': invalid_token, 'name': 'channel1', 'is_public': True})
    assert r.status_code == AccessError().code

def test_channels_list():
    """
    Test to check if channels_list works by passing in valid information.
    """
    # Clear register first.
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json = {'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    rego_1 = r.json()
    requests.post(config.url + 'channels/create/v2', json = {'token': rego_1['token'], 'name': 'Channel1', 'is_public': True})
    requests.post(config.url + 'channels/create/v2', json = {'token': rego_1['token'], 'name': 'Channel2', 'is_public': True})   
    # Test for valid input
    test_1 = requests.get(config.url + 'channels/list/v2', params = {'token': rego_1['token']})
    payload_1 = test_1.json()
    
    # Number of channels the user is found to be joined to.
    channelCount = 0    
    for k in range(len(payload_1['channels'])):
        if payload_1['channels'][k]['name'] == "Channel1":
            channelCount = channelCount + 1
        elif payload_1['channels'][k]['name'] == "Channel2":
            channelCount = channelCount + 1         
    # User should be in 2 channels.
    assert channelCount == 2
    
def test_channels_list_error():
    # Clear data first
    requests.delete(config.url + 'clear/v1')
    # invalid user - Access Error
    test_2 = requests.get(config.url + 'channels/list/v2', json = {'token': 'invalid_user'})
    assert test_2.status_code == AccessError().code
