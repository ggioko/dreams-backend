import pytest

from src.auth import auth_register_v1
from src.channel import channel_invite_v1
from src.channels import channels_create_v1
from src.echo import echo
from src.error import InputError, AccessError
from src.other import clear_v1

'''
InputError when any of:
channel_id does not refer to a valid channel.
u_id does not refer to a valid user

AccessError when any of:
the authorised user is not already a member of the channel
'''

def test_channel_invite_invalid_channel():
    clear_v1()

    adminID = auth_register_v1('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    userID = auth_register_v1('peasantuser@gmail.com', 'diffpassword!', 'Everest', 'Hayden')    
    channelID = channels_create_v1(adminID['auth_user_id'], 'dankmemechannel', False)

    with pytest.raises(InputError):
        channel_invite_v1(adminID['auth_user_id'], channelID['channel_id'] + 1, userID['auth_user_id'])


def test_channel_invite_invalid_user():
    clear_v1()

    adminID = auth_register_v1('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    userID = auth_register_v1('peasantuser@gmail.com', 'diffpassword!', 'Everest', 'Hayden')    
    channelID = channels_create_v1(adminID['auth_user_id'], 'dankmemechannel', False)

    with pytest.raises(InputError):
        channel_invite_v1(adminID['auth_user_id'], channelID['channel_id'], userID['auth_user_id'] + 1)

def test_channel_invite_invalid_authoriser():
    clear_v1()

    adminID = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user1ID = auth_register_v1('validemail2@gmail.com', '1234abc!@#', 'Haydenn', 'Everestt')
    user2ID = auth_register_v1('validemail3@gmail.com', '123abcd!@#', 'Haydeen', 'Everesst')
    channelID = channels_create_v1(adminID['auth_user_id'], 'DankMemeChannel', False) 

    with pytest.raises(AccessError):
        channel_invite_v1(user1ID['auth_user_id'], channelID['channel_id'], user2ID['auth_user_id'])

def test_channel_details_invalid_id():
    pass

def test_channel_details_unauthorised_user():
    pass

def test_channel_messages_invalid_id():
    pass

def test_channel_messages_invalid_start_pos():
    pass

def test_channel_messages_unauthorised_user():
    pass
