import pytest

from src.auth import auth_register_v2, auth_logout_v1
from src.channels import channels_create_v2
from src.channel import channel_messages_v2, channel_join_v2
from src.message import message_send_v2, message_remove_v1, message_edit_v2, message_share_v1
from src.other import clear_v1
from src.error import InputError, AccessError

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
    message_send_v2(id_1['token'], channel_1['channel_id'], message)
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
    channels_create_v2(id_2['token'], "MyChannel2", True)
    message = "hello this is my new channel"
    channel_join_v2(id_2['token'], channel_1['channel_id'])
    message_send_v2(id_2['token'], channel_1['channel_id'], message)
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
    message_send_v2(id_1['token'], channel_1['channel_id'], message)
    channel_messages_v2(id_1['token'], channel_1['channel_id'], 0)
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
    channels_create_v2(id_2['token'], "MyChannel2", True)
    message = "hello this is my new channel"
    channel_join_v2(id_2['token'], channel_1['channel_id'])
    channel_join_v2(id_3['token'], channel_1['channel_id'])
    message_send_v2(id_2['token'], channel_1['channel_id'], message)
    result1 = channel_messages_v2(id_2['token'], channel_1['channel_id'], 0)
    with pytest.raises(AccessError):
        assert message_remove_v1(id_3['token'], result1['messages'][0]['message_id'])

def test_message_edit_valid_owner():
    '''
    Given a message, message id and token, checks if the message in message_id
    is replaced with the given message. 
    Test for channel owner
    '''
    clear_v1()
    id_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(id_1['token'], "MyChannel", True)
    message = "hello this is my new channel"
    edit = "This is an edited message"
    message_send_v2(id_1['token'], channel_1['channel_id'], message)
    result1 = channel_messages_v2(id_1['token'], channel_1['channel_id'], 0)
    assert result1['messages'][0]['message'] == message
    message_edit_v2(id_1['token'], result1['messages'][0]['message_id'], edit)
    result2 = channel_messages_v2(id_1['token'], channel_1['channel_id'], 0)
    assert result2['messages'][0]['message'] == edit

def test_message_edit_valid_sender():
    '''
    Given a message, message id and token, checks if the message in message_id
    is replaced with the given message. 
    Test for channel sender but not a owner
    '''
    clear_v1()
    id_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id_2 = auth_register_v2('validemail2@gmail.com', '123abc2!@#', 'Haydenn', 'Everestt')
    channel_1 = channels_create_v2(id_1['token'], "MyChannel", True)
    channels_create_v2(id_2['token'], "MyChannel2", True)
    message = "hello this is my new channel"
    edit = "This is an edited message"
    channel_join_v2(id_2['token'], channel_1['channel_id'])
    message_send_v2(id_2['token'], channel_1['channel_id'], message)
    result1 = channel_messages_v2(id_2['token'], channel_1['channel_id'], 0)
    assert result1['messages'][0]['message'] == message
    message_edit_v2(id_2['token'], result1['messages'][0]['message_id'], edit)
    result2 = channel_messages_v2(id_1['token'], channel_1['channel_id'], 0)
    assert result2['messages'][0]['message'] == edit

def test_message_edit_invalid_editor():
    '''
    Given a message, message id and token, checks if an AccessError is raised
    as a person who is not the channel owner or sender tries to edit the message.
    '''
    clear_v1()
    id_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id_2 = auth_register_v2('validemail2@gmail.com', '123abc2!@#', 'Haydenn', 'Everestt')
    id_3 = auth_register_v2('validemail3@gmail.com', '1233abc2!@#', 'Haydennn', 'Everesttt')
    channel_1 = channels_create_v2(id_1['token'], "MyChannel", True)
    message = "hello this is my new channel"
    edit = "This is an edited message"
    channel_join_v2(id_2['token'], channel_1['channel_id'])
    channel_join_v2(id_3['token'], channel_1['channel_id'])
    message_send_v2(id_2['token'], channel_1['channel_id'], message)
    result1 = channel_messages_v2(id_2['token'], channel_1['channel_id'], 0)
    assert result1['messages'][0]['message'] == message
    with pytest.raises(AccessError):
        message_edit_v2(id_3['token'], result1['messages'][0]['message_id'], edit)

def test_message_edit_invalid_message_length():
    '''
    Given a message, message id and token, checks if an InputError is rasied
    as the message that is to replace the og message longer than 1000 characters
    '''
    clear_v1()
    id_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(id_1['token'], "MyChannel", True)
    message = "hello this is my new channel"

    edit = "a"
    for i in range(1001):
        edit += f" {i}"

    message_send_v2(id_1['token'], channel_1['channel_id'], message)
    result1 = channel_messages_v2(id_1['token'], channel_1['channel_id'], 0)
    assert result1['messages'][0]['message'] == message
    with pytest.raises(InputError):
        message_edit_v2(id_1['token'], result1['messages'][0]['message_id'], edit)

def test_message_edit_invalid_message_id():
    '''
    Given a message, message id and token, checks an InputError is raised 
    as the message_id is invalid - either already been delted or not in list of messages
    '''
    clear_v1()
    id_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(id_1['token'], "MyChannel", True)
    message = "hello this is my new channel"
    edit = "This is an edited message"
    message_send_v2(id_1['token'], channel_1['channel_id'], message)
    result1 = channel_messages_v2(id_1['token'], channel_1['channel_id'], 0)
    assert result1['messages'][0]['message'] == message
    message_remove_v1(id_1['token'], result1['messages'][0]['message_id'])
    with pytest.raises(InputError):
        message_edit_v2(id_1['token'], result1['messages'][0]['message_id'], edit)

def test_message_edit_invalid_token():
    '''
    Given a message, message id and token, checks and AccessError is raised
    as the token is invalid
    '''
    clear_v1()
    id_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(id_1['token'], "MyChannel", True)
    message = "hello this is my new channel"
    edit = "This is an edited message"
    message_send_v2(id_1['token'], channel_1['channel_id'], message)
    result1 = channel_messages_v2(id_1['token'], channel_1['channel_id'], 0)
    assert result1['messages'][0]['message'] == message
    auth_logout_v1(id_1['token'])
    with pytest.raises(AccessError):
        message_edit_v2(id_1['token'], result1['messages'][0]['message_id'], edit)