import pytest
import requests
import json
from src import config

def test_echo():
    '''
    A simple test for clear
    '''
    assert requests.get(config.url + '/clear/v1')