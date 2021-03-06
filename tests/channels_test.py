'''
channels_test.py


z5205069 Julius Vandeleur
Tests for channnels_list_v1()

'''

import pytest

#from src.error import InputError
from src.error import AccessError
from src.channels import channels_list_v1, channels_create_v1
from src.channel import channel_join_v1
from src.auth import auth_register_v1
from src.other import clear_v1




# Throw access error if auth_user_id is invalid (Section 6.3)
def test_channels_list_access_error():
    with pytest.raises(AccessError):
        # Pass a string into channels_list_v1 - should return access error.
        assert channels_list_v1('invalid')
        
# Do we need this??
def test_channels_list_runs():
    assert channels_list_v1(1)

# Test for user that is not in any channel.
# Output should be an empty list.
def test_channels_list_no_channels():
    clear_v1() # Reset internal data to its initial state
    # Add new id to data set
    id = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    # Loop through all channels, make sure id is not found in the channels' data.
    assert channels_list_v1(id) == {
        'channels': [
        ],
    }
                     
# Test for user that is in one channel only.
# Output should be a dictionary {channels} with one set of data.
def test_channels_list_one_channel():
    clear_v1() # Reset internal data to its initial state
    # Add new id to data set
    id = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel1Name = "My Channel" 
    channel2Name = "Not My Channel"
    channels_create_v1(1, channel1Name, True)
    channels_create_v1(2, channel2Name, True)                  
    channel_join_v1(id, channel1Name)
    assert channels_list_v1(id) == {
        'channels': [
        {
            'channel_id': 1,
            	'name': 'My Channel',
        }     
        ],            
    }
    
# Test for user that is in multiple channels
# Output should be a dictionary {channels} with one set of data.
def test_channels_list_multi_channels():
    clear_v1() # Reset internal data to its initial state
    # Add new id to data set
    id = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    channel1Name = "Channel1" 
    channel2Name = "Channel2"
    channel3Name = "Channel3"
    channel4Name = "Channel4"
    # Create 4 channels, and join 2 of them
    channels_create_v1(1, channel1Name, True)
    channels_create_v1(2, channel2Name, True)
    channels_create_v1(3, channel3Name, True)
    channels_create_v1(4, channel4Name, True)                    
    channel_join_v1(id, channel1Name)
    channel_join_v1(id, channel3Name)
    
    # Number of channels the user is found to be joined to.
    channelCount = 0    
    for channel in channels_list_v1(id):
        if channel1Name == channel['name']:
            ++channelCount
        elif channel2Name == channel['name']:
            ++channelCount
            
    # User should be in 2 channels.
    assert channelCount == 2
       
    
    
    
    
