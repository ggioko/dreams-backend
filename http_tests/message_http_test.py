import requests
import json
from src import config
from src.error import AccessError, InputError
from src.helper import generate_token
from src.channels import channels_create_v2
    
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
    channel_id = channels_create_v2(token['token'], name, True)
    requests.post(config.url + 'message/send/v2', json={'token': token['token'], \
        'channel_id' : channel_id['channel_id'], 'message' : message})
    resp = requests.get(config.url + 'channel/messages/v2', params={'token': token['token'], \
        'channel_id' : channel_id['channel_id'], 'start' : 0})
    assert json.loads(resp.text) == message

    

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

    channel_id = channels_create_v2(token['token'], name, True)
    r = requests.post(config.url + 'message/send/v2', json={'token': token['token'], \
        'channel_id' : channel_id['channel_id'], 'message' : message})
    
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
    channel_id = channels_create_v2(token['token'], name, True)
    channel_id_2 = channels_create_v2(token['token'], name_2, True)
    resp = requests.post(config.url + 'message/send/v2', json={'token': token['token'], \
        'channel_id' : channel_id['channel_id'], 'message' : message})
    resp_2 = requests.post(config.url + 'message/send/v2', json={'token': token['token'], \
        'channel_id' : channel_id_2['channel_id'], 'message' : message_2})
    
    assert json.loads(resp.text) != json.loads(resp_2.text)