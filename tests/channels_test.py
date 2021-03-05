import pytest

from src.channels import channels_create_v1
from src.error import InputError

# Test the case where the channel name is more than 20 characters
# Expected InputError
def test_channels_create_invalid_channel_name():
    with pytest.raises(InputError):         
        assert channels_create_v1(1, 'Nameismorethan20characters', 1) 

# Test the case where the channel name is less than 20 characters
# Expected autotest pass
def test_channels_create_valid_channel_name():
    valid = channels_create_v1(1, 'channel', 1)
    assert valid['channel_id'] != None

# Test whether the channel id returned by channels_create is an integer
def test_channels_create_returns_integer():
    new_channel = channel_create_v1(1, 'channel', 1)
    # Check if return type is an int
    assert isinstance(new_channel['channel_id'], int)