import requests
import json
from src import config
from src.error import AccessError, InputError
from src.helper import generate_token
    
def test_message_send_runs():
    '''
    A check to see if message_send runs correctly by creating a user
    and channel then sending a message then printing all messages on that
    channel
    '''
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    token = json.loads(resp.text)
    message = "Hello this is a new message"
    name = "MyChannel"
    resp = requests.post(config.url + 'channels/create/v2', json={'token': token['token'], \
        'name' : name, 'is_public' : True})
    channel = json.loads(resp.text)
    requests.post(config.url + 'message/send/v2', json={'token': token['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    resp = requests.get(config.url + 'channel/messages/v2', params={'token': token['token'], \
        'channel_id' : channel['channel_id'], 'start' : 0})
    assert json.loads(resp.text)['messages'][0]['message'] == message

def test_message_send_http_too_long():
    '''
    A check to see if message_send runs correctly by creating a user
    and channel then sending a message then printing all messages on that
    channel
    '''
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    token = json.loads(resp.text)
    name = "My Channel"
    message = "a"
    for i in range(1001):
        message += f" {i}"

    resp = requests.post(config.url + 'channels/create/v2', json={'token': token['token'], \
        'name' : name, 'is_public' : True})
    channel = json.loads(resp.text)
    r = requests.post(config.url + 'message/send/v2', json={'token': token['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    
    assert r.status_code == InputError().code

def test_message_send_http_differnt_ids():
    '''
    A check to see if message_send runs correctly by creating a user
    and channel then sending a message then printing all messages on that
    channel
    '''
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    token = json.loads(resp.text)
    name = "My Channel"
    name_2 = "My Second Channel"
    message = "my first message"
    message_2 = "my second message"
    resp = requests.post(config.url + 'channels/create/v2', json={'token': token['token'], \
        'name' : name, 'is_public' : True})
    channel = json.loads(resp.text)
    resp = requests.post(config.url + 'channels/create/v2', json={'token': token['token'], \
        'name' : name_2, 'is_public' : True})
    channel_2 = json.loads(resp.text)
    resp = requests.post(config.url + 'message/send/v2', json={'token': token['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    resp_2 = requests.post(config.url + 'message/send/v2', json={'token': token['token'], \
        'channel_id' : channel_2['channel_id'], 'message' : message_2})
    
    assert json.loads(resp.text) != json.loads(resp_2.text)