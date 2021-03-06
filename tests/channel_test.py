import pytest

from src.channel import channel_details_v1, channel_join_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError, AccessError

def test_channel_invite_invalid_channel():
    pass

def test_channel_invite_invalid_user():
    pass

def test_channel_invite_invalid_authoriser():
    pass


def test_channel_details_invalid_channel_id():
    clear_v1()
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert channel_details_v1(1, 'Invalid Channel') # Pass in string as channel_id 

def test_channel_details_unauthorised_user():
    clear_v1() # Clear data and register 2 new users.
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth_register_v1('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    channels_create_v1(1, 'Channel1', True) # User 1 is a member because they created Channel1.
    with pytest.raises(AccessError):
        assert channel_details_v1(2, 1)  # User 2 is not a member.      

# Throw access error if auth_user_id is invalid (Section 6.3)
def test_channel_details_invalid_user():
    clear_v1()
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channels_create_v1(1, 'Channel1', True) # Create a channel to make sure the error is arising from user id.               
    with pytest.raises(AccessError):
        # Pass a string into channels_list_v1 - should return access error.
        assert channel_details_v1('invalid', 1) # Invalid user id entered.
        
        
def test_channel_messages_invalid_id():
    pass

def test_channel_messages_invalid_start_pos():
    pass

def test_channel_messages_unauthorised_user():
    pass
