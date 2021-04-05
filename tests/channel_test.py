import pytest

from src.auth import auth_register_v1, auth_register_v2, auth_logout_v1
from src.channel import channel_messages_v1, channel_messages_v2
from src.channel import channel_join_v1, channel_join_v2, channel_invite_v2, channel_details_v2
from src.channel import channel_addowner_v1
from src.channels import channels_create_v1, channels_create_v2
from src.helper import generate_token, get_token_user_id, SECRET

from src.error import InputError, AccessError
from src.other import clear_v1

def test_channel_invite_valid():
    '''
    Tests channel_invite_v2 with all valid information
    '''
    clear_v1()

    auth_user_token = auth_register_v2('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')['token']
    userID = auth_register_v2('peasantuser@gmail.com', 'diffpassword!', 'Everest', 'Hayden')    
    channelID = channels_create_v2(auth_user_token, 'dankmemechannel', False)
    assert channel_invite_v2(auth_user_token, channelID['channel_id'], userID['auth_user_id']) == {}

def test_channel_invite_invalid_channel():
    '''
    Tests channel_invite_v2 with all valid information except for an invalid channel
    '''
    clear_v1()

    auth_user_token = auth_register_v2('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')['token']
    userID = auth_register_v2('peasantuser@gmail.com', 'diffpassword!', 'Everest', 'Hayden')    
    channelID = channels_create_v2(auth_user_token, 'dankmemechannel', False)
    
    with pytest.raises(InputError):
        channel_invite_v2(auth_user_token, channelID['channel_id'] + 1, userID['auth_user_id'])

def test_channel_invite_invalid_user():
    '''
    Tests channel_invite_v2 with all valid information except for an invalid userID
    '''
    clear_v1()

    auth_user_token = auth_register_v2('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')['token']
    userID = auth_register_v2('peasantuser@gmail.com', 'diffpassword!', 'Everest', 'Hayden')    
    channelID = channels_create_v2(auth_user_token, 'dankmemechannel', False)

    with pytest.raises(InputError):
        channel_invite_v2(auth_user_token, channelID['channel_id'], userID['auth_user_id'] + 1)

def test_channel_invite_invalid_authoriser():
    '''
    Tests channel_invite_v2 with all valid information except for the user inviting a new user
    not having the permissions to do so
    '''
    clear_v1()

    auth_user_token = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')['token']
    user1token = auth_register_v2('validemail2@gmail.com', '1234abc!@#', 'Haydenn', 'Everestt')['token']
    user2ID = auth_register_v2('validemail3@gmail.com', '123abcd!@#', 'Haydeen', 'Everesst')
    channelID = channels_create_v2(auth_user_token, 'DankMemeChannel', False) 

    with pytest.raises(AccessError):
        channel_invite_v2(user1token, channelID['channel_id'], user2ID['auth_user_id'])

def test_channel_invite_token_missing():
    '''
    Tests channel_invite_v2 with all valid information except that the authorised user has
    logged out
    '''
    clear_v1()

    auth_user_token = auth_register_v2('madladadmin@gmail.com', '123abc!@#', 'Hayden', 'Everest')['token']
    userID = auth_register_v2('peasantuser@gmail.com', 'diffpassword!', 'Everest', 'Hayden')    
    channelID = channels_create_v2(auth_user_token, 'dankmemechannel', False)
    auth_logout_v1(auth_user_token)
    
    with pytest.raises(AccessError):
        channel_invite_v2(auth_user_token, channelID['channel_id'], userID['auth_user_id'])

def channel_addowner_everything_correct():
    '''
    Tests channel_addowner_v1 with all valid information
    '''
    clear_v1()

    auth_user_token = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')['token']
    user2ID = auth_register_v2('validemail3@gmail.com', '123abcd!@#', 'Haydeen', 'Everesst')
    channelID = channels_create_v2(auth_user_token, 'dankmemechannel', False)
    
    assert channel_addowner_v1(auth_user_token, channelID, user2ID['auth_user_id']) == {}
    
def channel_addowner_invalid_channel():
    '''
    Tests channel_addowner_v1 with an invalid channel ID
    '''
    clear_v1()

    auth_user_token = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')['token']
    user2ID = auth_register_v2('validemail3@gmail.com', '123abcd!@#', 'Haydeen', 'Everesst')
    channelID = channels_create_v2(auth_user_token, 'dankmemechannel', False)
    with pytest.raises(InputError):
        channel_addowner_v1(auth_user_token, channelID['channel_id'] + 1, user2ID['auth_user_id'])
        
def channel_addowner_already_owner():
    '''
    Tests channel_addowner_v1 with u_id already an owner of the channel
    '''
    clear_v1()

    auth_user_token = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')['token']
    user2ID = auth_register_v2('validemail3@gmail.com', '123abcd!@#', 'Haydeen', 'Everesst')
    channelID = channels_create_v2(auth_user_token, 'dankmemechannel', False)
    channel_addowner_v1(auth_user_token, channelID, user2ID['auth_user_id'])
    with pytest.raises(InputError):
        channel_addowner_v1(auth_user_token, channelID, user2ID['auth_user_id'])
        
def channel_addowner_invalid_authoriser():
    '''
    Tests channel_addowner_v1 with the authorised user being invalid
    '''
    clear_v1()

    auth_user_token = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')['token']
    user1token = auth_register_v2('validemail2@gmail.com', '1234abc!@#', 'Haydenn', 'Everestt')['token']
    user2ID = auth_register_v2('validemail3@gmail.com', '123abcd!@#', 'Haydeen', 'Everesst')
    channelID = channels_create_v2(auth_user_token, 'dankmemechannel', False)
    with pytest.raises(AccessError):
        channel_addowner_v1(user1token, channelID, user2ID['auth_user_id'])

def test_channel_details_invalid_channel_id():
    """
    Test for an invalid channel_id - should return InputError
    """
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest') 
    with pytest.raises(InputError):
        assert channel_details_v2(user_1['token'], 'Invalid Channel') #Pass in string as channel_id 

def test_channel_details_unauthorised_user():
    """
    Test for an unauthorised user - should return AccessError
    """
    clear_v1() # Clear data and register 2 new users.
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    channel_1 = channels_create_v2(user_1['token'], 'Channel1', True) # User 1 is a member because they created Channel1.
    with pytest.raises(AccessError):
        assert channel_details_v2(user_2['token'], channel_1['channel_id']) # User 2 is not a member.

def test_channel_details_invalid_user():
    """
    Test for an invalid token - should return AccessError
    """
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(user_1['token'], 'Channel1', True)
    with pytest.raises(AccessError):
        # Pass a non-existent token into channel_details_v2 - should return access error.
        assert channel_details_v2('invalid_token', channel_1['channel_id']) # Invalid token entered.
        
def test_channel_details_runs():
    """
    Test to see if channel_details carries out basic functionality.
    """
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel_1 = channels_create_v2(user_1['token'], 'Channel1', True)
    assert channel_details_v2(user_1['token'],channel_1['channel_id']) == {
        'name': 'Channel1',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'validemail@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Everest',
                'handle_str': 'HaydenEverest',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'validemail@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Everest',
                'handle_str': 'HaydenEverest',
            }
        ],
    }

def test_channel_details_multiple_members():
    """
    Test to see if channel_details will list a channel with multiple members.
    """
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('validemail1@gmail.com', '123abc!@#', 'Fred', 'Smith')
    user_3 = auth_register_v2('validemail2@gmail.com', '123abc!@#', 'Jimmy', 'Barnes')
    user_4 = auth_register_v2('validemail3@gmail.com', '123abc!@#', 'Angus', 'Young')
    
    channel_1 = channels_create_v2(user_1['token'], 'Channel1', True)
    channel_join_v2(user_2['token'], channel_1['channel_id'])       
    channel_join_v2(user_3['token'], channel_1['channel_id'])
    channel_join_v2(user_4['token'], channel_1['channel_id'])
    
    correct = 0
    if channel_details_v2(user_1['token'],channel_1['channel_id'])['name'] == 'Channel1':
        if len(channel_details_v2(user_1['token'],channel_1['channel_id'])['owner_members']) == 1:
            if len(channel_details_v2(user_1['token'],channel_1['channel_id'])['all_members']) == 4:
                correct = 1
           
    assert correct == 1     

# Test the case where token is invalid for channel_messages
# Expected AccessError
def test_channel_messages_invalid_token():
    clear_v1()
    register1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel1 = channels_create_v2(register1['token'], 'channel_1', True)
    invalid_token = generate_token(4)
    with pytest.raises(AccessError):
        assert channel_messages_v2(invalid_token, channel1['channel_id'], 0)
        
# Test the case where channels ID is not a valid channel
# Expected InputError
def test_channel_messages_invalid_id():
    clear_v1()   
    register1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert channel_messages_v2(register1['token'], 10, 0)

# Test the case where the start is greater than the total number of messages in the channel
# Expected InputError
def test_channel_messages_invalid_start_pos():
    clear_v1()   
    register1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel1 = channels_create_v2(register1['token'], 'channel_1', True)
    with pytest.raises(InputError):
        assert channel_messages_v2(register1['token'], channel1['channel_id'], 100)

# Test the case Authorised user is not a member of channel
# Expected AccessError
def test_channel_messages_unauthorised_user():
    clear_v1()   
    register1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    register2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    channel1 = channels_create_v2(register1['token'], 'channel_1', True)
    with pytest.raises(AccessError):
        assert channel_messages_v2(register2['token'], channel1['channel_id'], 0)

def test_channel_join_invalid_token():
    '''
    Tests if an AccessError is raised when an invalid token is passed in
    '''
    clear_v1()
    valid_token1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    valid_token2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    invalid_token1 = generate_token(4)
    invalid_token2 = generate_token(7)
    channels_create_v2(valid_token1['token'], "Channel1", True)
    channels_create_v2(valid_token2['token'], "Channel2", True)
    with pytest.raises(AccessError):
        assert channel_join_v2(invalid_token1, 1)
        assert channel_join_v2(invalid_token2, 1)

def test_channel_join_invalid_channel_id():
    '''
    Tests if an InputError is raised if a wrong channel_id is given
    '''
    clear_v1()
    id1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    channels_create_v2(id1['token'], "Channel1", True)
    channels_create_v2(id2['token'], "Channel2", True)
    with pytest.raises(InputError):
        assert channel_join_v2(id1['token'], 7)
        assert channel_join_v2(id1['token'], 9)
        assert channel_join_v2(id2['token'], 20)

def test_channel_join_private_channel():
    '''
    Tests if an AccessError is raised when trying to join a private channel
    '''
    clear_v1()
    id1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    cid1 = channels_create_v2(id1['token'], "Channel1", False)
    cid2 = channels_create_v2(id2['token'], "Channel2", False)
    with pytest.raises(AccessError):
        assert channel_join_v2(id1['token'], cid1['channel_id'])
        assert channel_join_v2(id2['token'], cid2['channel_id'])
