import pytest
from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.other import clear_v1
from src.error import InputError, AccessError

from src.data import data

# Test the case that Auth_user_id is invalid for channels create
# Expected AccessError
def test_channels_create_invalid_Auth_user_id():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(AccessError):
        assert channels_create_v1('invalid', 'invalid', True)

# Test the case where the channel name is more than 20 characters
# Expected InputError
def test_channels_create_invalid_channel_name():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):         
        assert channels_create_v2(1, 'Nameismorethan20characters', True) 

# Test the case where is_public is of type bool
# Expected InputError
def test_channels_create_invalid_is_public():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):         
        assert channels_create_v2(1, 'channel', 20) 

# Test the case where the channel name is less than 20 characters
# Expected autotest pass
def test_channels_create_valid_channel_name():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    valid = channels_create_v2(1, 'channel', True)
    assert valid['channel_id'] != None

# Test whether the channel id returned by channels_create is an integer
def test_channels_create_returns_integer():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    new_channel = channels_create_v2(1, 'channel', True)
    # Check if return type is an int
    assert isinstance(new_channel['channel_id'], int)
