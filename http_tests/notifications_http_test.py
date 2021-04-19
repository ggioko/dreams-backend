import pytest
import requests
import json
from src import config
from src.error import AccessError, InputError

def test_notifications_exceptions():
    """
    Test exception case for notifications/get/v1.
    """
    # Clear register first.
    requests.delete(config.url + 'clear/v1')
    
    # Pass in invalid token
    test = requests.get(config.url + 'notifications/get/v1', params = {'token': 'invalid_token'})
    assert test.status_code == AccessError().code


def test_notifications_get():
    """
    Test to check if notifications/get/v1 works by passing in valid information.
    """
    # Clear register first.
    requests.delete(config.url + 'clear/v1')
    # Create 3 users
    r = requests.post(config.url + 'auth/register/v2', json = {'email':'validemail@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    user1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json = {'email':'validemail1@gmail.com', \
    'password' : '123abc!@#', 'name_first':'Fred', 'name_last':'Smith'})
    user2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json = {'email':'validemail2@gmail.com', \
    'password' : '123abc!@#', 'name_first':'John', 'name_last':'Apple'})
    user3 = r.json()
    
    # Get user1 to create a channel and invite user3
    r = requests.post(config.url + 'channels/create/v2',  json={'token': user1['token'],\
    'name': 'channel1', 'is_public': True})
    new_channel = r.json()
    requests.post(config.url + 'channel/invite/v2', json={'token': user1['token'],\
    'channel_id': new_channel['channel_id'], 'u_id':user3['auth_user_id']})
    
    # Get user1 to create a DM and invite user3
    r = requests.post(config.url + 'dm/create/v1',  json={'token': user1['token'],\
    'u_ids': [user1['auth_user_id'], user2['auth_user_id']]})
    new_dm = r.json()
    requests.post(config.url + 'dm/invite/v1',  json={'token': user1['token'],\
    'dm_id' : new_dm['dm_id'] ,'u_id': user3['auth_user_id']})
    
    # Get user1 to tag user3 in a channel message
    message = "Hello @johnapple, how are you"
    requests.post(config.url + 'message/send/v2', json={'token': user1['token'],\
    'channel_id': new_channel['channel_id'], 'message': message})
    
    # Get user1 to tag user3 in a dm message
    requests.post(config.url + 'message/senddm/v1', json={'token': user1['token'],\
    'dm_id': new_dm['dm_id'], 'message': message})
    
    # Pass in valid params to notifications/get/v1
    test = requests.get(config.url + 'notifications/get/v1', params = {'token': user3['token']})
    notifs = test.json()
    assert type(notifs) == list                     
    assert len(notifs) == 4
    # First notification                       
    assert notifs[3] ==  {'channel_id': new_channel['channel_id'],
                         'dm_id': -1,
                         'notification_message': "haydeneverest added you to channel1",
                        }
    # Most recent notification, this will also only show the first 20 characters of the message.
    assert notifs[0] == {'channel_id': -1,
                         'dm_id': new_dm['dm_id'],
                         'notification_message': "haydeneverest tagged you in fredsmith, haydeneverest, haydeneverest: Hello @johnapple, ho",
                        }
    