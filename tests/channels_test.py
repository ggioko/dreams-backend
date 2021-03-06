import pytest

from src.channels import channels_create_v1, channels_listall_v1, channels_create_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError

def test_channels_create_invalid_channel_name():
    pass

def test_channels_listall_runs():
    clear_v1()
    id = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    assert channels_listall_v1(id['auth_user_id'])

def test_channels_listall_check():
    clear_v1()
    id = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    name = "My Channel"
    channels_create_v1(id['auth_user_id'],name,True)
    channels = [channels_listall_v1(id['auth_user_id'])['channels'][c]['name'] for c in range(len(channels_listall_v1(1)['channels']))]
    assert name in channels

def test_channels_listall_access_error():
    with pytest.raises(AccessError):
        assert channels_listall_v1(-1)

