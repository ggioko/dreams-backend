import pytest
import requests
import json
from src import confc

def test_create():
    """
    A simple test to check channels_create works by passing valid information
    """
    resp = requests.get(config.url + 'channels_create', params={'token': 'token', 'name': 'channel1', 'is_public': True})
    assert json.loads(resp.text) == {'channel_id': 'channel_id'}