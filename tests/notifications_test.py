import pytest
from src.notifications import notifications_get_v1
from src.error import AccessError
from src.other import clear_v1
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.channel import channel_invite_v2
from src.message import message_senddm_v1, message_send_v2
from src.dm import dm_create_v1, dm_invite_v1

def test_notifications_invalid_token():
    '''
    Tests the invalid token exception for notifications_get_v1.
    Should return AccessError
    '''
    clear_v1()
    auth_register_v2('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(AccessError):
        assert notifications_get_v1('invalid_token')

def test_notifications_works():
    '''
    Tests to see that notifications_get_v1 operates correctly when valid
    info is passed in.
    Should return {notifications}
    '''
    clear_v1()
    # Register users
    user1 = auth_register_v2('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('second@gmail.com', '123abc!@#', 'Fred', 'Smith')
    
    # Have user1 create a channel and invite user2 to it.
    channel1 = channels_create_v2(user1['token'], 'Channel1', True)
    channel_invite_v2(user1['token'], channel1['channel_id'], user2['auth_user_id'])
    # Have user1 send a message in channel1 and tag user2 in it.
    message_send_v2(user1['token'], channel1['channel_id'], 'Hello @fredsmith, this is a channel')
    # Have user1 create a dm and invite user2 to it.
    dm1 = dm_create_v1(user1['token'], [user1['auth_user_id']])
    dm_invite_v1(user1['token'], dm1['dm_id'], user2['auth_user_id'])
    # Have user1 send a message in dm1 and tag user2 in it.
    message_senddm_v1(user1['token'], dm1['dm_id'], 'Hi, this is a dm tagging @fredsmith')
    
    
    notifs = notifications_get_v1(user2['token'])
    assert type(notifs) == list                     
    assert len(notifs) == 4
    # First notification                       
    assert notifs[3] ==  {'channel_id': channel1['channel_id'],
                         'dm_id': -1,
                         'notification_message': "haydeneverest added you to Channel1"
                        }
    # Most recent notification, this will also only show the first 20 characters of the message.
    assert notifs[0] == {'channel_id': -1,
                         'dm_id': dm1['dm_id'],
                         'notification_message': "haydeneverest tagged you in haydeneverest, haydeneverest: Hi, this is a dm tag"
                        }
    

                        
    