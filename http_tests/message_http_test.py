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

def test_http_message_remove_valid_owner():
    '''
    Given a message id and token, checks if the message is removed
    Test for channel owner
    '''
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    r = requests.post(config.url + 'message/send/v2', json={'token': id['token'], \
        'channel_id' : channel['channel_id'], 'message' : "my first message"})
    message = r.json()
    r = requests.delete(config.url + 'message/remove/v1', json={'token': id['token'], \
        'message_id' : message['message_id']})

    assert r.json() == {}

def test_http_message_remove_valid_sender():
    '''
    Given a message id and token, checks if the message is removed
    Test for channel sender but not a owner
    '''
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail2@gmail.com', \
    'password' : '1234abc!@#', 'name_first':'Haydenn', 'name_last':'Everestt'})
    id2 = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id1['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    r = requests.post(config.url + 'channel/join/v2', json = {'token': id2['token'], 'channel_id': channel['channel_id']})
    r = requests.post(config.url + 'message/send/v2', json={'token': id2['token'], \
        'channel_id' : channel['channel_id'], 'message' : "my first message"})
    message = r.json()
    r = requests.delete(config.url + 'message/remove/v1', json={'token': id2['token'], \
        'message_id' : message['message_id']})

    assert r.json() == {}

def test_http_message_remove_invalid_message_id():
    '''
    Given a invalid message id and token, raises InputError
    '''
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    r = requests.post(config.url + 'message/send/v2', json={'token': id['token'], \
        'channel_id' : channel['channel_id'], 'message' : "my first message"})
    message = r.json()
    r = requests.delete(config.url + 'message/remove/v1', json={'token': id['token'], \
        'message_id' : 145234234234234242})
    
    assert r.status_code == InputError().code

def test_http_message_remove_invalid_user_trying_to_delete():
    '''
    Given a message id and token, raises AccessError 
    since the user is not the sender or channel owner
    '''
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail2@gmail.com', \
    'password' : '1234abc!@#', 'name_first':'Haydenn', 'name_last':'Everestt'})
    id2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail3@gmail.com', \
    'password' : '12345abc!@#', 'name_first':'Haydennn', 'name_last':'Everesttt'})
    id3 = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id1['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    r = requests.post(config.url + 'channel/join/v2', json = {'token': id2['token'], 'channel_id': channel['channel_id']})
    r = requests.post(config.url + 'channel/join/v2', json = {'token': id3['token'], 'channel_id': channel['channel_id']})

    r = requests.post(config.url + 'message/send/v2', json={'token': id2['token'], \
        'channel_id' : channel['channel_id'], 'message' : "my first message"})
    message = r.json()
    r = requests.delete(config.url + 'message/remove/v1', json={'token': id3['token'], \
        'message_id' : message['message_id']})

    assert r.status_code == AccessError().code
