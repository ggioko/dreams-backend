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
    channelID = channels_create_v1(adminID, 'dankmemechannel', True)

    with pytest.raises(InputError):
        channel_invite_v1(adminID, channelID + 1, userID)


def test_channel_invite_invalid_user():
    clear_v1()

    adminID = auth_register_v1('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    userID = auth_register_v1('peasantuser@gmail.com', 'diffpassword!', 'Everest', 'Hayden')    
    channelID = channels_create_v1(adminID, 'dankmemechannel', True)

    with pytest.raises(InputError):
        channel_invite_v1(adminID, channelID, userID + 1)

def test_channel_invite_invalid_authoriser():
    clear_v1()

    adminID = auth_register_v1('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user1ID = auth_register_v1('peasantuser1@gmail.com', 'diffpassword!', 'Everest', 'Hayden')    
    user2ID = auth_register_v1('peasantuser2@gmail.com', 'diffpassword.', 'Hayrest', 'Everden')
    channelID = channels_create_v1(adminID, 'dankmemechannel', True)

    with pytest.raises(AccessError):
        channel_invite_v1(user1ID, channelID, user2ID)

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
