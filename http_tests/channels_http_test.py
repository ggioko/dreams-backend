import pytest
import requests
import json
from src import config

def test_channels_listall_v2_runs():
    '''
    A check to see if listall runs correctly with no channels
    '''
    requests.delete(config.url + 'clear/v1')
    data = requests.post(config.url + 'auth/login/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    resp = requests.get(config.url + 'channels/listall/v2', args={'token': data['token']})
    assert json.loads(resp.text) == {'channels': []}

def test_channels_listall_v2_check():
    '''
    A check to see if listall runs correctly with two channels
    '''
    requests.delete(config.url + 'clear/v1')
    data = requests.post(config.url + 'auth/login/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    name = "My Channel"
    name_2 = "My second Channel"
    requests.post(config.url + 'channels/create/v2', args={'token': data['token'], 'name' : name, \
    'is_public' : True})
    requests.post(config.url + 'channels/create/v2', args={'token': data['token'], 'name' : name_2, \
    'is_public' : True})
    resp = requests.get(config.url + 'channels/listall/v2', args={'token': data['token']})
    assert json.loads(resp.text) == {'channels': [
        "My Channel",
        "My second Channel"
    ]}

