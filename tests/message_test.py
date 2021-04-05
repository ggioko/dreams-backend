import pytest
from src.auth import auth_login_v2, auth_register_v2, auth_logout_v1
from src.channels import channels_create_v2
from src.channel import channel_messages_v2, channel_join_v2
from src.message import message_send_v2, message_remove_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from src.helper import generate_token

def test_message_send_valid():
    '''
    Checks if when a user in the specified channel sends a short message.
    They can see the details from channel_messages
    '''
    clear_v1()
    id_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(id_1['token'], "MyChannel", True)
    message = "hello this is my new channel"
    message_1 = message_send_v2(id_1['token'], channel_1['channel_id'], message)
    result = channel_messages_v2(id_1['token'], channel_1['channel_id'], 0)
    assert result['messages'][0]['message_id'] == message_1['message_id']
    assert result['messages'][0]['u_id'] == id_1['auth_user_id']
    assert result['messages'][0]['message'] == message

def test_message_send_differnt_ids():
    '''
    Checks if message_send returns different ids
    '''
    clear_v1()
    id_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(id_1['token'], "MyChannel", True)
    channel_2 = channels_create_v2(id_1['token'], "MyChannel2", True)
    message = "hello this is my new channel"
    message_2 = 'hi this is my second channel'
    message_1 = message_send_v2(id_1['token'], channel_1['channel_id'], message)
    message_2 = message_send_v2(id_1['token'], channel_2['channel_id'], message_2)
    assert message_1['message_id'] != message_2['message_id']

def test_message_send_too_long():
    '''
    Checks if message_send raises an error if the message is too long
    '''
    clear_v1()
    id_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(id_1['token'], "MyChannel", True)
    message = "a"
    for i in range(1001):
        message += f" {i}"

    with pytest.raises(InputError):
        assert message_send_v2(id_1['token'], channel_1['channel_id'], message)

def test_message_send_user_not_a_member():
    '''
    Checks if message_send raises an error if the user is not a member
    of the channel
    '''
    clear_v1()
    id_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(id_1['token'], "MyChannel", True)
    id_2 = auth_register_v2('validemail2@gmail.com', '123abc!@#', 'Haydenn', 'Everestt')
    message = "Not my channel"

    with pytest.raises(AccessError):
        assert message_send_v2(id_2['token'], channel_1['channel_id'], message)

def test_message_remove_valid_owner():
    '''
    Given a message id and token, checks if the message is removed
    Test for channel owner
    '''
    clear_v1()
    id_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(id_1['token'], "MyChannel", True)
    message = "hello this is my new channel"
    message_1 = message_send_v2(id_1['token'], channel_1['channel_id'], message)
    result1 = channel_messages_v2(id_1['token'], channel_1['channel_id'], 0)
    message_remove_v1(id_1['token'], result1['messages'][0]['message_id'])
    result2 = channel_messages_v2(id_1['token'], channel_1['channel_id'], 0)
    assert result2['messages'] == []

def test_message_remove_valid_sender():
    '''
    Given a message id and token, checks if the message is removed
    Test for channel sender but not a owner
    '''
    clear_v1()
    id_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id_2 = auth_register_v2('validemail2@gmail.com', '123abc2!@#', 'Haydenn', 'Everestt')
    channel_1 = channels_create_v2(id_1['token'], "MyChannel", True)
    channel_2 = channels_create_v2(id_2['token'], "MyChannel2", True)
    message = "hello this is my new channel"
    channel_join_v2(id_2['token'], channel_1['channel_id'])
    message_1 = message_send_v2(id_2['token'], channel_1['channel_id'], message)
    result1 = channel_messages_v2(id_2['token'], channel_1['channel_id'], 0)
    message_remove_v1(id_2['token'], result1['messages'][0]['message_id'])
    result2 = channel_messages_v2(id_1['token'], channel_1['channel_id'], 0)
    assert result2['messages'] == []

def test_message_remove_invalid_message_id():
    '''
    Given a invalid message id and token, raises InputError
    '''
    clear_v1()
    id_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(id_1['token'], "MyChannel", True)
    message = "hello this is my new channel"
    message_1 = message_send_v2(id_1['token'], channel_1['channel_id'], message)
    result1 = channel_messages_v2(id_1['token'], channel_1['channel_id'], 0)
    # 145234234234234242 is a random channel id
    with pytest.raises(InputError):
        assert message_remove_v1(id_1['token'], 145234234234234242)

def test_message_remove_invalid_user_trying_to_delete():
    '''
    Given a message id and token, raises AccessError 
    since the user is not the sender or channel owner
    '''
    clear_v1()
    id_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id_2 = auth_register_v2('validemail2@gmail.com', '123abc2!@#', 'Haydenn', 'Everestt')
    id_3 = auth_register_v2('validemail3@gmail.com', '123abc2!@#', 'Haydennn', 'Everesttt')
    channel_1 = channels_create_v2(id_1['token'], "MyChannel", True)
    channel_2 = channels_create_v2(id_2['token'], "MyChannel2", True)
    message = "hello this is my new channel"
    channel_join_v2(id_2['token'], channel_1['channel_id'])
    channel_join_v2(id_3['token'], channel_1['channel_id'])
    message_1 = message_send_v2(id_2['token'], channel_1['channel_id'], message)
    result1 = channel_messages_v2(id_2['token'], channel_1['channel_id'], 0)
    with pytest.raises(AccessError):
        assert message_remove_v1(id_3['token'], result1['messages'][0]['message_id'])
