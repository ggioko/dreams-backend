import pytest
import requests
import json
from src import config

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
    A check to see if listall runs correctly with two channels
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
    assert json.loads(resp.text) == {'channels': [
        "My Channel",
        "My second Channel"
    ]}

