import pytest
import requests
import json
from src import config

def test_auth_register():
    '''
    A test to check if auth_register works
    '''
    assert requests.get(config.url + 'echo', params={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})