import pytest

from src.other import clear_v1, search_v2
from src.error import InputError, AccessError
from src.channels import channels_create_v2
from src.channel import channel_invite_v2
from src.auth import auth_register_v2
from src.message import message_send_v2, message_senddm_v1
from src.dm import dm_create_v1

def test_search_channel_messages_v2_valid():
    """
    Checks if correct messages retuned with valid parameters when searching
    with search_v2()
    """
    clear_v1()

    user1 = auth_register_v2('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('peasantuser@gmail.com', 'diffpassword!', 'Everest', 'Hayden')    
    channel_1 = channels_create_v2(user1['token'], 'dankmemechannel', False)
    channel_invite_v2(user1['token'], channel_1['channel_id'], user2['auth_user_id'])


    messagecontent1 = "hello this is my new channel"
    messagecontent2 = "lennahc wen ym si siht olleh"

    message_1 = message_send_v2(user1['token'], channel_1['channel_id'], messagecontent1)
    message_send_v2(user1['token'], channel_1['channel_id'], messagecontent2)
    
    matching = search_v2(user1['token'], "my new")
    print(matching)
    assert matching['messages'][0]['message_id'] == message_1['message_id']


def test_search_channel_v2_too_long_input():
    """
    Checks if input error is raised with a character input that is too long in
    search_v2()
    """
    clear_v1()

    user1 = auth_register_v2('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    
    with pytest.raises(InputError):
        assert search_v2(user1['token'], "a" * 1100)

def test_search_channel_messages_v2_not_in_channel():
    """
    Checks if user can't see messages when they're not in the channel
    with search_v2()
    """
    clear_v1()

    user1 = auth_register_v2('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('peasantuser@gmail.com', 'diffpassword!', 'Everest', 'Hayden')    
    channel_1 = channels_create_v2(user1['token'], 'dankmemechannel', False)

    messagecontent1 = "hello this is my new channel"
    messagecontent2 = "lennahc wen ym si siht olleh"

    message_send_v2(user1['token'], channel_1['channel_id'], messagecontent1)
    message_send_v2(user1['token'], channel_1['channel_id'], messagecontent2)
    
    matching = search_v2(user2['token'], "my new")
    assert matching['messages'] == []

def test_search_dms_v2_valid():
    """
    Checks if correct messages retuned with valid parameters when searching
    with search_v2() for DMs
    """
    clear_v1()

    user1 = auth_register_v2('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('peasantuser@gmail.com', 'diffpassword!', 'Everest', 'Hayden')    

    messagecontent1 = "hello this is my new channel"
    messagecontent2 = "lennahc wen ym si siht olleh"

    new_dm = dm_create_v1(user1['token'], [user2['auth_user_id']])
    print(new_dm)

    dm_1 = message_senddm_v1(user1['token'], new_dm['dm_id'], messagecontent1)
    message_senddm_v1(user1['token'], new_dm['dm_id'], messagecontent2)
    
    matching = search_v2(user1['token'], "my new")
    assert matching['messages'][0]['message_id'] == dm_1['message_id']

def test_search_dms_v2_invaliduser():
    """
    Checks if correct messages retuned with matches not from the user's dms
    with search_v2() for DMs
    """
    clear_v1()

    user1 = auth_register_v2('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('peasantuser@gmail.com', 'diffpassword!', 'Everest', 'Hayden')    
    user3 = auth_register_v2('thirdemail@gmail.com', '321bca#@!', 'Bob', 'Jones')

    messagecontent1 = "hello this is my new channel"
    messagecontent2 = "lennahc wen ym si siht olleh"

    new_dm = dm_create_v1(user1['token'], [user2['auth_user_id']])

    message_senddm_v1(user1['token'], new_dm['dm_id'], messagecontent1)
    message_senddm_v1(user1['token'], new_dm['dm_id'], messagecontent2)
    
    matching = search_v2(user3['token'], "my new")
    assert matching['messages'] == []
