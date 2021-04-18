import pytest

from src.other import clear_v1, search_v2
from src.error import InputError, AccessError
from src.channels import channels_create_v2
from src.channel import channel_messages_v2, channel_invite_v2
from src.auth import auth_register_v2, auth_logout_v1
from src.message import message_send_v2, message_senddm_v1


"""
Given a query string, return a collection of messages in all of the channels/DMs
that the user has joined that match the query
Arguments:
    token (str)        - The token of the user who wants to search their messages
    query_str (str)    - The string that the user wants to find matches of

Exceptions:
    InputError  - Occurs when the length of the query string is over 1000 characters

Return Value:
    Returns a dictionary of messages in channels and DMs that the user is a part of
"""

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


    message = "hello this is my new channel"
    message2 = "lennahc wen ym si siht olleh"

    message_1 = message_send_v2(user1['token'], channel_1['channel_id'], message)
    message_2 = message_send_v2(user1['token'], channel_1['channel_id'], message)
    
    matching = search_v2(user1['token'], "my new")
    assert matching['messages'][0]['message_id'] == message_1['message_id']


