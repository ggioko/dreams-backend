import pytest

from src.channel import channel_invite_v1, channel_messages_v1, channel_join_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.echo import echo
from src.error import InputError, AccessError
from src.other import clear_v1

def test_channel_invite_invalid_channel():
    clear_v1()

    adminID = auth_register_v1('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    userID = auth_register_v1('peasantuser@gmail.com', 'diffpassword!', 'Everest', 'Hayden')    
    channelID = channels_create_v1(adminID['auth_user_id'], 'dankmemechannel', False)

    with pytest.raises(InputError):
        channel_invite_v1(adminID['auth_user_id'], channelID['channel_id'] + 1, userID['auth_user_id'])

def test_channel_invite_invalid_user():
    clear_v1()

    adminID = auth_register_v1('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    userID = auth_register_v1('peasantuser@gmail.com', 'diffpassword!', 'Everest', 'Hayden')    
    channelID = channels_create_v1(adminID['auth_user_id'], 'dankmemechannel', False)

    with pytest.raises(InputError):
        channel_invite_v1(adminID['auth_user_id'], channelID['channel_id'], userID['auth_user_id'] + 1)

def test_channel_invite_invalid_authoriser():
    clear_v1()

    adminID = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user1ID = auth_register_v1('validemail2@gmail.com', '1234abc!@#', 'Haydenn', 'Everestt')
    user2ID = auth_register_v1('validemail3@gmail.com', '123abcd!@#', 'Haydeen', 'Everesst')
    channelID = channels_create_v1(adminID['auth_user_id'], 'DankMemeChannel', False) 

    with pytest.raises(AccessError):
        channel_invite_v1(user1ID['auth_user_id'], channelID['channel_id'], user2ID['auth_user_id'])

def test_channel_details_invalid_id():
    pass

def test_channel_details_unauthorised_user():
    pass

# Test the case where auth_user_id is invalid for channel_messages
# Expected AccessError
def test_channel_messages_invalid_auth_user_id():
    clear_v1()
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v1(1, 'channel_1', True)
    with pytest.raises(AccessError):
        assert channel_messages_v1('invalid', channel_1['channel_id'], 0)
        
# Test the case where channels ID is not a valid channel
# Expected InputError
def test_channel_messages_invalid_id():
    clear_v1()   
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v1(1, 'channel_1', True)
    with pytest.raises(InputError):
        assert channel_messages_v1(1, 10, 0)

# Test the case where the start is greater than the total number of messages in the channel
# Expected InputError
def test_channel_messages_invalid_start_pos():
    clear_v1()   
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v1(1, 'channel_1', True)
    with pytest.raises(InputError):
        assert channel_messages_v1(1, channel_1['channel_id'], 100)

# Test the case Authorised user is not a member of channel
# Expected AccessError
def test_channel_messages_unauthorised_user():
    clear_v1()   
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v1(1, 'channel_1', True)
    with pytest.raises(AccessError):
        assert channel_messages_v1("invalid", channel_1['channel_id'], 0)
    pass

def test_channel_join_invalid_user_id():
    clear_v1()
    id1 = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id2 = auth_register_v1('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    channelid1 = channels_create_v1(1, "Channel1", True)
    channelid2 = channels_create_v1(2, "Channel2", True)
    with pytest.raises(AccessError):
        assert channel_join_v1(7, 1)
        assert channel_join_v1(8, 1)
        assert channel_join_v1(9, 1)

def test_channel_join_invalid_channel_id():
    clear_v1()
    id1 = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id2 = auth_register_v1('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    channelid1 = channels_create_v1(1, "Channel1", True)
    channelid2 = channels_create_v1(2, "Channel2", True)
    with pytest.raises(InputError):
        assert channel_join_v1(2, 7)
        assert channel_join_v1(1, 9)
        assert channel_join_v1(2, 20)

def test_channel_join_private_channel():
    clear_v1()
    id1 = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id2 = auth_register_v1('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    channelid1 = channels_create_v1(1, "Channel1", False)
    channelid2 = channels_create_v1(2, "Channel2", False)
    with pytest.raises(AccessError):
        assert channel_join_v1(2, 1)
        assert channel_join_v1(1, 2)
