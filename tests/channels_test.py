import pytest

from src.channels import channels_create_v1
from src.error import InputError

def test_channels_create_invalid_channel_name():
    with pytest.raises(InputError):
        assert channels_create_v1(1, 'Nameismorethan20characters', 1)


