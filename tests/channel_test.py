import pytest

from src.auth import auth_register_v1
from src.channel import channel_invite_v1
from src.channels import channels_create_v1
from src.channel import channel_join_v1
from src.echo import echo
from src.error import InputError, AccessError
from src.other import clear_v1


def test_channel_invite_invalid_channel():
    pass

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

def test_channel_join_valid_join():
    pass

def test_channel_join_invalid_channel_id():
    clear_v1()
    id1 = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id2 = auth_register_v1('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    channelid1 = channels_create_v1(1, "Channel1", True)
    channelid2 = channels_create_v1(2, "Channel2", True)
    with pytest.raises(InputError):
        assert channel_join_v1(2, 7)

def test_channel_join_private_channel():
    clear_v1()
    id1 = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id2 = auth_register_v1('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    channelid1 = channels_create_v1(1, "Channel1", False)
    channelid2 = channels_create_v1(2, "Channel2", False)
    with pytest.raises(AccessError):
        assert channel_join_v1(2, 1)
        assert channel_join_v1(1, 2)
