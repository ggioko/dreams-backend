import pytest
from datetime import datetime, timedelta

from src.error import InputError, AccessError
from src.other import clear_v1
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1

def test_standup_start_invalid_channel_id():
    """
    Testing when an invalid channel ID is used
    Expected: InputError
    """
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')

    with pytest.raises(InputError):
        assert standup_start_v1(user_1['token'], 5, 60)

def test_standup_start_invalid_authorised_member():
    """
    Testing when an authorised id is not a member of channel
    Expected: AcessError
    """

    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('validemail1@gmail.com', '123abc!@#', 'Fred', 'Smith')

    channel_1 = channels_create_v2(user_1['token'], 'channel1', True)

    with pytest.raises(AccessError):
        assert standup_start_v1(user_2['token'], channel_1['channel_id'], 60)

def test_standup_start_invalid_token():
    """
    Testing for when the token is invalid
    Expected: AccessError
    """

    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(user_1['token'], 'channel1', True)

    invalid_token = -1

    with pytest.raises(AccessError):
        assert standup_start_v1(invalid_token, channel_1['channel_id'], 60)

def test_standup_start_standup_active():
    """
    Testing for when the standup in channel is already active
    Expected: InputError
    """

    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(user_1['token'], 'channel1', True)

    # Start a standup
    standup_start_v1(user_1['token'], channel_1['channel_id'], 60)

    with pytest.raises(InputError):
        assert standup_start_v1(user_1['token'], channel_1['channel_id'], 60)

def test_standup_active():
    """
    Testing for when the standup is active in channel
    Expected: success
    """
    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(user_1['token'], 'channel1', True)

    # Start a standup
    standup = standup_start_v1(user_1['token'], channel_1['channel_id'], 30)

    assert standup_active_v1(user_1['token'], channel_1['channel_id']) == {'is_active' : True, 'time_finish' : standup['time_finish']}

def test_standup_active_invalid_token():
    """
    Testing for when the standup active if given an invalid token
    Expected: AccessError
    """
    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(user_1['token'], 'channel1', True)

    invalid_token = -1

    with pytest.raises(AccessError):
        assert standup_active_v1(invalid_token, channel_1['channel_id'])

def test_standup_active_invalid_channel_id():
    """
    Testing for when the standup active if given an invalid channel id
    Expected: InputError
    """
    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')

    invalid_channel_id = 5

    with pytest.raises(InputError):
        assert standup_active_v1(user_1['token'], invalid_channel_id)

def test_standup_active_finish():
    """
    Testing for when the standup has finished in channel
    Expected: success
    """
    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(user_1['token'], 'channel1', True)

    # Start a standup
    standup_start_v1(user_1['token'], channel_1['channel_id'], 0)

    assert standup_active_v1(user_1['token'], channel_1['channel_id']) == {'is_active' : False, 'time_finish' : None}

def test_standup_send_invalid_token():
    """
    Testing for when the token is invalid
    Expected: AccessError
    """
    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(user_1['token'], 'channel1', True)

    invalid_token = -1

    with pytest.raises(AccessError):
        assert standup_send_v1(invalid_token, channel_1['channel_id'], 'hello')

def test_standup_send_invalid_channel_id():
    """
    Testing for when the channel id is invalid
    Expected: InputError
    """
    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')

    invalid_channel_id = 20

    with pytest.raises(InputError):
        assert standup_send_v1(user_1['token'], invalid_channel_id, 'hello')
    
def test_standup_send_invalid_message():
    """
    Testing for when the message is longer than 1000 characters
    Expected: InputError
    """
    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(user_1['token'], 'channel1', True)

    with pytest.raises(InputError):
        assert standup_send_v1(user_1['token'], channel_1['channel_id'], "a"*1100)

def test_standup_send_authorised_user():
    """
    Testing for when a authorised user is not a member of channel
    Expected: AccessError
    """
    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('validemail1@gmail.com', '123abc!@#', 'Fred', 'Smith')
    channel_1 = channels_create_v2(user_1['token'], 'channel1', True)

    with pytest.raises(AccessError):
        assert standup_send_v1(user_2['token'], channel_1['channel_id'], "hello")

def test_standup_send_active_not_running():
    """
    Testing for when a active standup is running in channel
    Expected: InputError
    """
    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(user_1['token'], 'channel1', True)

    standup_start_v1(user_1['token'], channel_1['channel_id'], 0)
    standup_active_v1(user_1['token'], channel_1['channel_id'])

    with pytest.raises(InputError):
        assert standup_send_v1(user_1['token'], channel_1['channel_id'], "hello")