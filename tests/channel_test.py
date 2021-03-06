import pytest

from src.auth import auth_register_v1
from src.channel import channel_invite_v1
from src.channels import channels_create_v1
from src.echo import echo
from src.error import InputError
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
    pass

def test_channel_invite_invalid_authoriser():
    pass

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
