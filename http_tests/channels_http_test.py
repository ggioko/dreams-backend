"""
COMP1531 Team DORITO
channels_http_test.py
"""

import pytest
import requests
import json
from src import config

def test_channels_list_system():
    """
    Test to check if channels_list works by passing in valid information.
    """
    # Clear register first.
    r = requests.post(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', params = {'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    rego_1 = r.json()
    requests.post(config.url + 'channel/create/v2', params = {'token': rego_1['token'], 'name': 'Channel1', 'is_public': True})
    requests.post(config.url + 'channel/create/v2', params = {'token': rego_1['token'], 'name': 'Channel2', 'is_public': True})   
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
    
    # invalid user - Access Error
    test_2 = requests.get(config.url + 'channels/list/v2', params = {'token': 'invalid_user'})
    assert test_2.status_code == 403
