import pytest
import requests
import json
from src import config
from src.error import AccessError, InputError
    
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

def test_message_edit_http_valid_owner():
    '''
    Given a message, message id and token, checks if the message in message_id
    is replaced with the given message. 
    Test for channel owner
    '''
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id_1 = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id_1['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    message = "hello this is my new channel"
    edit = "This is an edited message"
    r = requests.post(config.url + 'message/send/v2', json={'token': id_1['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    message_id = r.json()
    assert requests.put(config.url + 'message/edit/v2', json={'token': id_1['token'], \
        'message_id' : message_id['message_id'], 'message' : edit})

def test_message_edit_http_valid_sender():
    '''
    Given a message, message id and token, checks if the message in message_id
    is replaced with the given message. 
    Test for channel sender but not a owner
    '''
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail2@gmail.com', \
    'password' : '1234abc!@#', 'name_first':'Haydenn', 'name_last':'Everestt'})
    id_2 = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id_1['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    message = "hello this is my new channel"
    edit = "This is an edited message"
    r = requests.post(config.url + 'channel/join/v2', json = {'token': id_2['token'], 'channel_id': channel['channel_id']})
    r = requests.post(config.url + 'message/send/v2', json={'token': id_2['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    message_id = r.json()
    assert requests.put(config.url + 'message/edit/v2', json={'token': id_2['token'], \
        'message_id' : message_id['message_id'], 'message' : edit})

def test_message_edit_http_invalid_editor():
    '''
    Given a message, message id and token, checks if an AccessError is raised
    as a person who is not the channel owner or sender tries to edit the message.
    '''
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail2@gmail.com', \
    'password' : '1234abc!@#', 'name_first':'Haydenn', 'name_last':'Everestt'})
    id_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail3@gmail.com', \
    'password' : '12345abc!@#', 'name_first':'Haydennn', 'name_last':'Everesttt'})
    id_3 = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id_1['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    message = "hello this is my new channel"
    edit = "This is an edited message"
    r = requests.post(config.url + 'channel/join/v2', json = {'token': id_2['token'], 'channel_id': channel['channel_id']})
    r = requests.post(config.url + 'channel/join/v2', json = {'token': id_3['token'], 'channel_id': channel['channel_id']})
    r = requests.post(config.url + 'message/send/v2', json={'token': id_2['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    message_id = r.json()
    r = requests.put(config.url + 'message/edit/v2', json={'token': id_3['token'], \
        'message_id' : message_id['message_id'], 'message' : edit})
    
    assert r.status_code == AccessError().code

def test_message_edit_http_invalid_message_length():
    '''
    Given a message, message id and token, checks if an InputError is rasied
    as the message that is to replace the og message longer than 1000 characters
    '''
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id = r.json()
    message = "hello this is my new channel"
    edit = "a"
    for i in range(1001):
        edit += f" {i}"
    r = requests.post(config.url + 'channels/create/v2', json={'token': id['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    r = requests.post(config.url + 'message/send/v2', json={'token': id['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    message_id = r.json()
    r = requests.put(config.url + 'message/edit/v2', json={'token': id['token'], \
        'message_id' : message_id['message_id'], 'message' : edit})
    
    assert r.status_code == InputError().code

def test_message_edit_http_invalid_message_id():
    '''
    Given a message, message id and token, checks an InputError is raised 
    as the message_id is invalid - either already been delted or not in list of messages
    '''
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    message = "hello this is my new channel"
    edit = "This is an edited message"
    r = requests.post(config.url + 'message/send/v2', json={'token': id['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    message_id = r.json()
    r = requests.delete(config.url + 'message/remove/v1', json={'token': id['token'], \
        'message_id' : message_id['message_id']})
    r = requests.put(config.url + 'message/edit/v2', json={'token': id['token'], \
        'message_id' : message_id['message_id'], 'message' : edit})
    
    assert r.status_code == InputError().code

def test_message_edit_http_invalid_token():
    '''
    Given a message, message id and token, checks and AccessError is raised
    as the token is invalid
    '''
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    message = "hello this is my new channel"
    edit = "This is an edited message"
    r = requests.post(config.url + 'message/send/v2', json={'token': id['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    message_id = r.json()
    r = requests.post(config.url + 'auth/logout/v1', json={'token': id['token']})
    r = requests.put(config.url + 'message/edit/v2', json={'token': id['token'], \
        'message_id' : message_id['message_id'], 'message' : edit})
    
    assert r.status_code == AccessError().code

def test_message_senddm():
    '''
    Given valid token, dm_id and message, run the message_senddm_v1 function.
    Function should return the message_id, and write the message details to data.
    '''
    # Clear data first
    # Register members
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'thirdemail@gmail.com',
    'password' : '321bca#@!', 'name_first':'Bob', 'name_last':'Jones'})
    user_3 = r.json()
    
    # Get u_ids 
    u_id2 = user_2['auth_user_id']
    u_id3 = user_3['auth_user_id']
    # Create two dm's
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id2, u_id3]})
    new_dm = r.json()
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id2]})
    new_dm_2 = r.json()    
    r = requests.post(config.url + 'message/senddm/v1', json={'token': user_1['token'],'dm_id': new_dm['dm_id'], 'message': 'test message'})
    send_dm = r.json()
    r = requests.post(config.url + 'message/senddm/v1', json={'token': user_1['token'],'dm_id': new_dm_2['dm_id'], 'message': 'test message'})
    
    r = requests.get(config.url + 'dm/messages/v1', params={'token': user_1['token'],'dm_id': new_dm['dm_id'], 'start': 0})
    output = r.json()

    message_list = output['messages']
    req_info = message_list[0]
    
    assert send_dm['message_id'] == req_info[0]['message_id']
    assert user_1['auth_user_id'] == req_info[0]['u_id']
    assert 'test message' == req_info[0]['message']
       

def test_message_senddm_errors():
    '''
    Testing InputError and AccessError cases for message_senddm_v1 function.
    '''
    # Clear data first
    # Register members
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'thirdemail@gmail.com',
    'password' : '321bca#@!', 'name_first':'Bob', 'name_last':'Jones'})
    user_3 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'fourthemail@gmail.com',
    'password' : '321bca#@!', 'name_first':'Billy', 'name_last':'Elliot'})
    user_4 = r.json()
    # Get u_ids 
    u_id2 = user_2['auth_user_id']
    u_id3 = user_3['auth_user_id']
    
    # Create a dm
    r1 = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id2, u_id3]})
    new_dm = r1.json()
    
    # Message more than 1000 chars - InputError
    long_string = 1001*'x'
    r = requests.post(config.url + 'message/senddm/v1', json={'token': user_1['token'],'dm_id': new_dm['dm_id'], 'message': long_string})
    assert r.status_code == InputError().code
    # Invalid token input - AccessError
    r = requests.post(config.url + 'message/senddm/v1', json={'token': 'invalid_token','dm_id': new_dm['dm_id'], 'message': 'test message'})
    assert r.status_code == AccessError().code
    # Unauthorised user - not member of dm
    r = requests.post(config.url + 'message/senddm/v1', json={'token': user_4['token'],'dm_id': new_dm['dm_id'], 'message': 'test message'})
    assert r.status_code == AccessError().code
    
def test_message_share_dm_invalid_token():
    '''
    Given an invalid token.
    AccessError is raised.
    '''
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    u_id2 = user_2['auth_user_id']
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id2]})
    new_dm = r.json()
    r = requests.post(config.url + 'message/senddm/v1', json={'token': user_1['token'],'dm_id': new_dm['dm_id'], 'message': 'Hello'})
    r = requests.post(config.url + 'message/share/v1', json={'token': 'random','og_message_id': new_dm['dm_id'],
    'message': 'test message', 'channel_id': -1, 'dm_id': new_dm['dm_id']})
    assert r.status_code == AccessError().code
    
def test_message_share_unauthorised_user_dm():
    '''
    User is not part of the DM that they are trying to share to.
    AccessError is raised.
    '''
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'thirdemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'John', 'name_last':'Jones'})
    user_3 = r.json()
    u_id2 = user_2['auth_user_id']
    u_id3 = user_3['auth_user_id']
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id2]})
    new_dm = r.json()
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id3]})
    new_dm_2 = r.json()
    r = requests.post(config.url + 'message/senddm/v1', json={'token': user_1['token'],'dm_id': new_dm['dm_id'], 'message': 'Hello'})
    message_1 = r.json()
    r = requests.post(config.url + 'message/share/v1', json={'token': user_2['token'],'og_message_id': message_1['message_id'],
    'message': 'test message', 'channel_id': -1, 'dm_id': new_dm_2['dm_id']})
    assert r.status_code == AccessError().code


def test_message_share_unauthorised_user_channel():
    '''
    User is not part of the channel that they are trying to share to.
    AccessError is raised.
    '''
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    id_2 = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id_1['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    message = "hello this is my new channel"
    optional = "a"
    r = requests.post(config.url + 'message/send/v2', json={'token': id_1['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    r = requests.get(config.url + 'channel/messages/v2', params={'token': id_1['token'], \
        'channel_id' : channel['channel_id'], 'start' : 0})
    result1 = r.json()
    r = requests.post(config.url + 'message/share/v1', json={'token': id_2['token'],'og_message_id': result1['messages'][0]['message_id'],
    'message': optional, 'channel_id': channel['channel_id'], 'dm_id': -1})
    assert r.status_code == AccessError().code


def test_message_share_long_optional_message():
    '''
    Checks if an InputError is rasied as optional message longer than 1000 characters
    '''
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id_1 = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id_1['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    message = "hello this is my new channel"
    optional = "a"
    for i in range(1001):
        optional += f" {i}"
    r = requests.post(config.url + 'message/send/v2', json={'token': id_1['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    r = requests.get(config.url + 'channel/messages/v2', params={'token': id_1['token'], \
        'channel_id' : channel['channel_id'], 'start' : 0})
    result1 = r.json()
    r = requests.post(config.url + 'message/share/v1', json={'token': id_1['token'],'og_message_id': result1['messages'][0]['message_id'],
    'message': optional, 'channel_id': channel['channel_id'], 'dm_id': -1})
    assert r.status_code == InputError().code

def test_message_react_dm():
    '''
    Given a token, message id and react_id checks if the message with message_id is reacted with react_id
    Test for message in dms
    '''
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    u_id2 = user_2['auth_user_id']
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id2]})
    new_dm = r.json()
    r = requests.post(config.url + 'message/senddm/v1', json={'token': user_1['token'],'dm_id': new_dm['dm_id'], 'message': 'test message'})
    message = r.json()
    assert requests.post(config.url + 'message/react/v1', json={'token': user_1['token'], \
        'message_id' : message['message_id'], 'react_id' : int(1)})

def test_message_react_channel():
    '''
    Given a token, message id and react_id checks if the message with message_id is reacted with react_id
    Test for message in channels
    '''
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id_1 = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id_1['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    message = "hello this is my new channel"
    r = requests.post(config.url + 'message/send/v2', json={'token': id_1['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    message_id = r.json()
    assert requests.post(config.url + 'message/react/v1', json={'token': id_1['token'], \
        'message_id' : message_id['message_id'], 'react_id' : int(1)})

def test_message_react_invalid_message_dm():
    '''
    Given a token, message id and react_id, checks if the inputerror is raised due to invalid message id
    Test for message in dms
    '''
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    u_id2 = user_2['auth_user_id']
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id2]})
    new_dm = r.json()
    r = requests.post(config.url + 'message/senddm/v1', json={'token': user_1['token'],'dm_id': new_dm['dm_id'], 'message': 'test message'})
    r = requests.post(config.url + 'message/react/v1', json={'token': user_1['token'], 'message_id' : int(40), 'react_id' : int(1)})
    assert r.status_code == InputError().code

def test_message_react_invalid_message_channel():
    '''
    Given a token, message id and react_id, checks if the inputerror is raised due to invalid message id
    Test for message in channels
    '''
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id_1 = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id_1['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    message = "hello this is my new channel"
    r = requests.post(config.url + 'message/send/v2', json={'token': id_1['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    r = requests.post(config.url + 'message/react/v1', json={'token': id_1['token'], 'message_id' : int(40), 'react_id' : int(1)})
    assert r.status_code == InputError().code

def test_message_react_dm_already_reacted():
    '''
    Given a token, message id and react_id, raises an InputError as the message is already reacetd to
    Test for message in dms
    '''
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    u_id2 = user_2['auth_user_id']
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id2]})
    new_dm = r.json()
    r = requests.post(config.url + 'message/senddm/v1', json={'token': user_1['token'],'dm_id': new_dm['dm_id'], 'message': 'test message'})
    message = r.json()
    r = requests.post(config.url + 'message/react/v1', json={'token': user_1['token'], \
        'message_id' : message['message_id'], 'react_id' : int(1)})
    r = requests.post(config.url + 'message/react/v1', json={'token': user_1['token'], \
        'message_id' : message['message_id'], 'react_id' : int(1)})
    assert r.status_code == InputError().code

def test_message_react_channel_already_reacted():
    '''
    Given a token, message id and react_id, raises an InputError as the message is already reacetd to
    Test for message in channels
    '''
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id_1 = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id_1['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    message = "hello this is my new channel"
    r = requests.post(config.url + 'message/send/v2', json={'token': id_1['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    message_id = r.json()
    requests.post(config.url + 'message/react/v1', json={'token': id_1['token'], \
        'message_id' : message_id['message_id'], 'react_id' : int(1)})
    r = requests.post(config.url + 'message/react/v1', json={'token': id_1['token'], \
        'message_id' : message_id['message_id'], 'react_id' : int(1)})
    assert r.status_code == InputError().code

def test_message_react_dm_invalid_react_id():
    '''
    Given a token, message id and react_id, raises an InputError as the react_id is invalid
    Test for message in dms
    '''
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    u_id2 = user_2['auth_user_id']
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id2]})
    new_dm = r.json()
    r = requests.post(config.url + 'message/senddm/v1', json={'token': user_1['token'],'dm_id': new_dm['dm_id'], 'message': 'test message'})
    message = r.json()
    r =  requests.post(config.url + 'message/react/v1', json={'token': user_1['token'], \
        'message_id' : message['message_id'], 'react_id' : int(-99)})
    assert r.status_code == InputError().code

def test_message_react_channel_invalid_react_id():
    '''
    Given a token, message id and react_id, raises an InputError as the react_id is invalid
    Test for message in channels
    '''
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id_1 = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id_1['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    message = "hello this is my new channel"
    r = requests.post(config.url + 'message/send/v2', json={'token': id_1['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    message_id = r.json()
    r = requests.post(config.url + 'message/react/v1', json={'token': id_1['token'], \
        'message_id' : message_id['message_id'], 'react_id' : int(-99)})
    assert r.status_code == InputError().code

def test_message_react_dm_not_a_member():
    '''
    Given a token, message id and react_id, raises AccessError at the user is not a dm member
    Test for message in dms
    '''
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail33@gmail.com',
    'password' : '32331cba#@!', 'name_first':'Freddy', 'name_last':'Smitthh'})
    user_3 = r.json()
    u_id2 = user_2['auth_user_id']
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id2]})
    new_dm = r.json()
    r = requests.post(config.url + 'message/senddm/v1', json={'token': user_1['token'],'dm_id': new_dm['dm_id'], 'message': 'test message'})
    message = r.json()
    r = requests.post(config.url + 'message/react/v1', json={'token': user_3['token'], \
        'message_id' : message['message_id'], 'react_id' : int(1)})
    assert r.status_code == AccessError().code

def test_message_react_channel_not_a_member():
    '''
    Given a token, message id and react_id, raises AccessError at the user is not a channel member
    Test for message in channels
    '''
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    id_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail2@gmail.com', \
    'password' : '1234abc!@#', 'name_first':'Haydenn', 'name_last':'Everestt'})
    id_2 = r.json()
    r = requests.post(config.url + 'channels/create/v2', json={'token': id_1['token'], \
        'name' : "My Channel", 'is_public' : True})
    channel = r.json()
    message = "hello this is my new channel"
    r = requests.post(config.url + 'message/send/v2', json={'token': id_1['token'], \
        'channel_id' : channel['channel_id'], 'message' : message})
    message_id = r.json()
    r = requests.post(config.url + 'message/react/v1', json={'token': id_2['token'], \
        'message_id' : message_id['message_id'], 'react_id' : int(1)})
    assert r.status_code == AccessError().code

def test_message_react_invalid_token():
    '''
    Given a token, message id and react_id, checks if an AccessError is raised when an invalid token is given 
    '''
    r = requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'validemail@gmail.com',
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'secondemail@gmail.com',
    'password' : '321cba#@!', 'name_first':'Fred', 'name_last':'Smith'})
    user_2 = r.json()
    u_id2 = user_2['auth_user_id']
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user_1['token'], 'u_ids': [u_id2]})
    new_dm = r.json()
    r = requests.post(config.url + 'message/senddm/v1', json={'token': user_1['token'],'dm_id': new_dm['dm_id'], 'message': 'test message'})
    message = r.json()
    r = requests.post(config.url + 'auth/logout/v1', json={'token': user_1['token']})
    r = requests.post(config.url + 'message/react/v1', json={'token': user_1['token'], 'message_id' : message['message_id'], 'react_id' : int(1)})
    assert r.status_code == AccessError().code
