import pytest

from src.auth import auth_register_v1, auth_register_v2
from src.channels import channels_create_v2, channels_listall_v2, channels_list_v1
from src.channel import channel_join_v1 
from src.auth import auth_register_v2, get_token
from src.other import clear_v1
from src.error import InputError, AccessError
from src.helper import generate_token

from src.data import data

# Test the case that Auth_user_id is invalid for channels create
# Expected AccessError
def test_channels_create_invalid_auth_user_id():
    clear_v1()
    invalid_token = generate_token(4)
    with pytest.raises(AccessError):
        assert channels_create_v2(invalid_token, 'channel1', True)

# Test the case where the channel name is more than 20 characters
# Expected InputError
def test_channels_create_invalid_channel_name():
    clear_v1()
    register1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):         
        assert channels_create_v2(register1['token'], 'Nameismorethan20characters', True) 

# Test the case where is_public is not of type bool
# Expected InputError
def test_channels_create_invalid_is_public():
    clear_v1()
    register1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):         
        assert channels_create_v2(register1['token'], 'channel', 20) 

def test_channels_listall_runs():
    """
    Test to make sure theres no errors when running list all with
    a valid token
    """
    clear_v1()
    auth = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    assert channels_listall_v2(auth['token'])

def test_channels_listall_check():
    """
    Test to make sure the function lists 2 given channels
    """
    clear_v1()
    auth = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    name = "My Channel"
    name2 = "My second Channel"
    channels_create_v2(auth['token'],name,True)
    channels_create_v2(auth['token'],name2,True)
    channels = [channels_listall_v2(auth['token'])['channels'][c]['name'] for c in range(len(channels_listall_v2(auth['token'])['channels']))]
    assert name in channels
    assert name2 in channels

def test_channels_listall_access_error():
    """
    Test to see if listall raises access error when passed in an invalid token
    """
    with pytest.raises(AccessError):
        assert channels_listall_v2(-1)

# Test the case where the channel name is less than 20 characters
# Expected autotest pass
def test_channels_create_valid_channel_name():
    clear_v1()
    register1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    valid = channels_create_v2(register1['token'], 'channel', True)
    assert valid['channel_id'] != None

# Test whether the channel id returned by channels_create is an integer
def test_channels_create_returns_integer():
    clear_v1()
    register1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    new_channel = channels_create_v2(register1['token'], 'channel', True)
    # Check if return type is an int
    assert isinstance(new_channel['channel_id'], int)
