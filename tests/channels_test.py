import pytest

from src.channel import channel_join_v2  
from src.channels import channels_create_v1, channels_listall_v1, channels_list_v2, channels_create_v2
from src.auth import auth_register_v2
from src.other import clear_v1
from src.error import InputError, AccessError

from src.data import data

# Test the case that Auth_user_id is invalid for channels create
# Expected AccessError
def test_channels_create_invalid_Auth_user_id():
    clear_v1()
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(AccessError):
        assert channels_create_v1('invalid', 'invalid', True)

# Test the case where the channel name is more than 20 characters
# Expected InputError
def test_channels_create_invalid_channel_name():
    clear_v1()
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):         
        assert channels_create_v1(1, 'Nameismorethan20characters', True) 

# Test the case where is_public is of type bool
# Expected InputError
def test_channels_create_invalid_is_public():
    clear_v1()
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):         
        assert channels_create_v1(1, 'channel', 20) 

def test_channels_listall_runs():
    clear_v1()
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    assert channels_listall_v1(1)

def test_channels_listall_check():
    clear_v1()
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    name = "My Channel"
    name2 = "My second Channel"
    channels_create_v1(1,name,True)
    channels_create_v1(1,name2,True)
    channels = [channels_listall_v1(1)['channels'][c]['name'] for c in range(len(channels_listall_v1(1)['channels']))]
    assert name in channels
    assert name2 in channels

def test_channels_listall_access_error():
    with pytest.raises(AccessError):
        assert channels_listall_v1(-1)

# Test the case where the channel name is less than 20 characters
# Expected autotest pass
def test_channels_create_valid_channel_name():
    clear_v1()
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    valid = channels_create_v1(1, 'channel', True)
    assert valid['channel_id'] != None

# Test whether the channel id returned by channels_create is an integer
def test_channels_create_returns_integer():
    clear_v1()
    auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    new_channel = channels_create_v1(1, 'channel', True)
    # Check if return type is an int
    assert isinstance(new_channel['channel_id'], int)


def test_channels_list_access_error():
    """
    Pass an invalid token into channels_list_v2 - should return access error.
    """
    clear_v1()
    with pytest.raises(AccessError):
        assert channels_list_v2('invalid_token')
        
def test_channels_list_runs():
    """
    Test to see if channels_list_v2 runs.
    """
    clear_v1()
    user = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    assert channels_list_v2(user['token'])

def test_channels_list_no_channels():
    """
    Test for a user that is part of no channels. Should return empty list.
    """
    clear_v1() # Reset internal data to its initial state
    # Add new id to data set
    user = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    # Loop through all channels, make sure id is not found in the channels' data.
    assert channels_list_v2(user['token']) == {
        'channels': [
        ],
    }
                     
def test_channels_list_one_channel(): # COMMENTED OUT CHANNEL_1 AND CHANNEL_3 names as they are unused.
    """
    Test for user that is in one channel only.
    Output should be a dictionary {channels} with one set of data.
    """
    clear_v1() # Reset internal data to its initial state
    # Add 2 new id's to data set. (1st id required to make channels, 2nd required to test.)
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    #channel_1 = 
    channels_create_v2(user_1['token'], "Channel1", True) # User who created channel will be a member.
    channel_2 = channels_create_v2(user_1['token'], "Channel2", True)
    #channel_3 = 
    channels_create_v2(user_1['token'], "Channel3", True) 

    channel_join_v2(user_2['token'], channel_2['channel_id'])              
    
    assert channels_list_v2(user_2['token']) == {
        'channels': [
        {
            'channel_id': channel_2['channel_id'],
            	'name': 'Channel2',
        }     
        ],            
    }

    
def test_channels_list_multi_channels():   # COMMENTED OUT CHANNEL_2 AND CHANNEL_4 names as they are unused.
    """
    Test for user that is in multiple channels
    Output should be a dictionary {channels} with one set of data.
    """
    clear_v1() # Reset internal data to its initial state
    # Add new id to data set
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')                
    # Create 4 channels, and join 2 of them
    channel_1 = channels_create_v2(user_1['token'], "Channel1", True)
    #channel_2 = 
    channels_create_v2(user_1['token'], "Channel2", True)
    channel_3 = channels_create_v2(user_1['token'], "Channel3", True)
    #channel_4 = 
    channels_create_v2(1, "Channel4", True)
    channel_join_v2(user_2['token'], channel_1['channel_id'])     # WAITING ON CHANNEL_JOIN_V1
    channel_join_v2(user_2['token'], channel_3['channel_id'])    
    # Number of channels the user is found to be joined to.
    channelCount = 0    
    for k in range(len(channels_list_v2(user_2['token'])['channels'])):
        if channels_list_v2(user_2['token'])['channels'][k]['name'] == "Channel1":
            channelCount = channelCount + 1
        elif channels_list_v2(user_2['token'])['channels'][k]['name'] == "Channel3":
            channelCount = channelCount + 1         
    # User should be in 2 channels.
    assert channelCount == 2
    
