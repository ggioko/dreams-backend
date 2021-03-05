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
from src.channels import channels_list_v1
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
# Output should be an empty dictionary.
def test_channels_list_no_channels():
    clear_v1() # Reset internal data to its initial state
    # Add new id to data set
    id = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    # Loop through all channels, make sure id is not found in the channels' data.
    emptyDict = {}
    assert channels_list_v1(id) == emptyDict
                        
