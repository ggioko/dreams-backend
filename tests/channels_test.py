'''
channels_test.py


z5205069 Julius Vandeleur
Tests for channnels_list()

Test 1: auth_user_id is invalid - throw AccessError (Section 6.3)

Test 2: channels_list runs when auth_user_id = 1

Test 3:  
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
        assert channels_list_v1(-1)
        
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
    channel1_name = "My Channel" 
    channel2_name = "Not My Channel"
    channels_create_v1(1, channel1_name, True)
    channels_create_v1(2, channel2_name, True)                  
    channel_join_v1(id, channel1_name)
    assert channels_list_v1(id) == {
        'channels': [
        {
            'channel_id': 1,
            	'name': 'My Channel',
        }     
        ],
            
    }
    
    
    
    
    
    
