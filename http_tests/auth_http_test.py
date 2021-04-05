import pytest
import requests
import json
from src import config

def test_auth_register():
    '''
    A test to check if auth_register works by passing in valid information
    '''
    requests.delete(config.url + 'clear/v1')
    assert requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    