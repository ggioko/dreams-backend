"""
COMP1531 Team DORITO
channel_http_test.py 
"""

import pytest
import requests
import json
from src import config

def test_channel_details_system():
    """
    Test to check if channel_details works by passing in valid information.
    """
    # Clear register first.
    r = requests.post(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', params = {'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    rego_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', params = {'email':'validemail2@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Fred', 'name_last':'Smith'})
    rego_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', params = {'email':'validemail3@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Angus', 'name_last':'Young'})
    rego_3 = r.json()
    r = requests.post(config.url + 'auth/register/v2', params = {'email':'validemail4@gmail.com', \
    'password' : '123abc!@#', 'name_first':'James', 'name_last':'Taylor'})
    rego_4 = r.json()
    r = requests.post(config.url + 'channel/create/v2', params = {'token': rego_1['token'], 'name': 'Channel1', 'is_public': True})
    new_channel = r.json()
    requests.post(config.url + 'channel/join/v2', params = {'token': rego_2['token'], 'channel_id': new_channel['channel_id']})
    requests.post(config.url + 'channel/join/v2', params = {'token': rego_3['token'], 'channel_id': new_channel['channel_id']})
    
    # invalid channel id - Input Error
    test_1 = requests.get(config.url + 'channel/details/v2', params = {'token': rego_1['token'], 'channel_id': 'invalid_id'})
    assert test_1.status_code == 400
    # unauthorised user - Access Error
    test_2 = requests.get(config.url + 'channel/details/v2', params = {'token': rego_4['token'], 'channel_id': new_channel['channel_id']})
    assert test_2.status_code == 403
    # invalid user - Access Error
    test_3 = requests.get(config.url + 'channel/details/v2', params = {'token': 'invalid_user', 'channel_id': new_channel['channel_id']})
    assert test_3.status_code == 403
    # system test
    test_4 = requests.get(config.url + 'channel/details/v2', params = {'token': rego_1['token'], 'channel_id': new_channel['channel_id']})
    payload_4 = test_4.json()
    correct = 0
    if payload_4['name'] == 'Channel1':
        if len(payload_4['owner_members']) == 1:
            if len(payload_4['all_members']) == 4:
                correct = 1
    assert correct == 1 
