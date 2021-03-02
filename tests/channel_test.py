import pytest

from src.channel import channel_invite_v1
from src.echo import echo
from src.error import InputError

def test_channel_invite_invalid_channel():
    pass

def test_channel_invite_invalid_user():
    with pytest.raises(InputError):
        assert channel_invite_v1(1, 1, -5)

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
