import pytest

from src.channel import channel_invite_v1, channel_messages_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.echo import echo
from src.error import InputError, AccessError

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

# Test the case where auth_user_id is invalid for channel_messages
# Expected AccessError
def test_channel_messages_invalid_auth_user_id():
    clear_v1()
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v1(1, 'channel_1', True)
    with pytest.raises(AccessError):
        assert channel_messages_v1('invalid', channel_1['channel_id'], 0)
        
# Test the case where channels ID is not a valid channel
# Expected InputError
def test_channel_messages_invalid_id():
    clear_v1()   
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v1(1, 'channel_1', True)
    with pytest.raises(InputError):
        assert channel_messages_v1(1, 10, 0)

# Test the case where the start is greater than the total number of messages in the channel
# Expected InputError
def test_channel_messages_invalid_start_pos():
    clear_v1()   
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v1(1, 'channel_1', True)
    with pytest.raises(InputError):
        assert channel_messages_v1(1, channel_1['channel_id'], 100)

# Test the case Authorised user is not a member of channel
# Expected AccessError
def test_channel_messages_unauthorised_user():
    clear_v1()   
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v1(1, 'channel_1', True)
    with pytest.raises(AccessError):
        assert channel_messages_v1("invalid", channel_1['channel_id'], 0)
