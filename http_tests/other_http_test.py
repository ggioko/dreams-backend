import pytest
import requests
import json
from src import config
from src.error import AccessError, InputError

def test_search():
    """
    Tests to see if HTTP implementation is working properly for search/v2
    """
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'madladadmin@gmail.com',\
    'password':'123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    rego_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'peasantuser@gmail.com',\
    'password':'diffpassword!', 'name_first':'Everest', 'name_last':'Hayden'})
    rego_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail3@gmail.com',\
    'password':'123abcd!@#', 'name_first':'Haydeen', 'name_last':'Everesst'})
    rego_3 = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token':rego_1['token'],\
    'name':'dankmemechannel', 'is_public':False})
    new_channel = r.json()
    requests.post(config.url + 'channel/invite/v2', json={'token': rego_1['token'],\
    'channel_id': new_channel['channel_id'] + 1, 'u_id':rego_2['auth_user_id']})
    
    messagecontent1 = "hello this is my new channel"

    r = requests.post(config.url + 'message/send/v2', json={'token': rego_1['token'], \
        'channel_id' : new_channel['channel_id'], 'message' : messagecontent1})

    # Query found
    r = requests.get(config.url + 'search/v2', params={'token': rego_1['token'],\
        'query_str': "my new"})
    assert r.status_code == 200

    # Too long search query
    r = requests.get(config.url + 'search/v2', params={'token': rego_1['token'],\
        'query_str': "a" * 1100})
    assert r.status_code == InputError().code

    # Matching string, but wrong user
    r = requests.get(config.url + 'search/v2', params={'token': rego_3['token'],\
        'query_str': "my new"})
    assert r.status_code == 200
