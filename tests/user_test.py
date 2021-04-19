import pytest

from src.error import InputError, AccessError
from src.auth import auth_register_v2
from src.other import clear_v1
from src.user import users_all_v1, user_profile_v2, user_profile_setemail_v2, user_profile_setname_v2, user_profile_sethandle_v1
from src.helper import generate_token
from src.channels import channels_create_v2
from src.channel import channel_details_v2
from src.admin import user_remove_v1

def test_users_all_v1_successful():
    '''
    Registers some users and provides a valid token to users_all_v1 returning a list of all registered users
    '''
    clear_v1()
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth_register_v2('validemail22@gmail.com', '1234abc!@#', 'Haydennn', 'Everesttt')
    # uses the generate token helper that creates fake tokens for testing
    user_list = users_all_v1(user1['token'])
    assert user_list['users'] == [
        {'u_id': 1, 'email': 'validemail@gmail.com', 'name_first': 'Hayden', 'name_last': 'Everest', 'handle_str': 'haydeneverest'},
        {'u_id': 2, 'email': 'validemail22@gmail.com', 'name_first': 'Haydennn', 'name_last': 'Everesttt', 'handle_str': 'haydennneveresttt'}
    ]

def test_users_all_v1_invalid_token():
    '''
    Registers a user and provides an invalid token to users_all_v1 returning an AccessError
    '''
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    # uses the generate token helper that creates fake tokens for testing
    invalid_token = generate_token(4)
    with pytest.raises(AccessError):
        assert users_all_v1(invalid_token)

def test_user_profile_invalid_u_id():
    """
    Tests for an invalid user id, should return InputError.
    """
    clear_v1()
    user = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert user_profile_v2(user['token'], 'invalid_user_id')
    

def test_user_profile_invalid_token():
    """
    Tests for an invalid token, should return AccessError.
    """
    clear_v1()
    user = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(AccessError):
        assert user_profile_v2('invalid_token', user['auth_user_id'])

def test_user_profile():
    """
    Pass in a user with valid token and u_id.
    Output should have the user's correct info in a dictionary.
    """
    clear_v1()
    user = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_info  = user_profile_v2(user['token'], user['auth_user_id'])
    assert user_info == {'user': {
                             'u_id': user['auth_user_id'],
                             'email': 'validemail0@gmail.com',
                             'name_first': 'Hayden',
                             'name_last': 'Everest',
                             'handle_str': 'haydeneverest'          
    }}
    
def test_user_profile_other_user():
    """
    Pass in a user with valid token and other user's u_id.
    Output should have the other user's correct info in a dictionary.
    """
    clear_v1()
    user1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('validemail1@gmail.com', '123abc!@#', 'Fred', 'Smith')
    user_info  = user_profile_v2(user1['token'], user2['auth_user_id'])
    assert user_info == {'user': {
                             'u_id': user2['auth_user_id'],
                             'email': 'validemail1@gmail.com',
                             'name_first': 'Fred',
                             'name_last': 'Smith',
                             'handle_str': 'fredsmith'          
    }}
    
def test_user_profile_removed_user():
    """
    Pass in a user with valid token and u_id.
    Output should have the removed user's correct info in a dictionary.
    """
    clear_v1()
    user1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('validemail1@gmail.com', '123abc!@#', 'Fred', 'Smith')
    user_remove_v1(user1['token'], user2['auth_user_id'])
    user_info  = user_profile_v2(user1['token'], user2['auth_user_id'])
    assert user_info == {'user': {
                             'u_id': user2['auth_user_id'],
                             'email': 'validemail1@gmail.com',
                             'name_first': 'Removed',
                             'name_last': 'user',
                             'handle_str': 'fredsmith'          
    }}
    
    
def test_setemail():
    """
    Pass in a user with valid token and new email.
    The email in their data store should be replaced by the new email passed in.
    """ 
    clear_v1()
    user = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_profile_setemail_v2(user['token'], 'newemail@gmail.com')
    user_info  = user_profile_v2(user['token'], user['auth_user_id'])
    assert user_info == {'user': {
                             'u_id': user['auth_user_id'],
                             'email': 'newemail@gmail.com',
                             'name_first': 'Hayden',
                             'name_last': 'Everest',
                             'handle_str': 'haydeneverest'          
    }}
    
def test_setemail_channel_members():
    """
    Pass in a user with valid token and new email.
    If they are a member of a channel, their info in the channel should also be updated.
    """ 
    clear_v1()
    user = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_profile_setemail_v2(user['token'], 'newemail@gmail.com')
    channel_1 = channels_create_v2(user['token'], 'Channel1', True)
    channel_info = channel_details_v2(user['token'], channel_1['channel_id'])
    assert channel_info == {
        'name': 'Channel1',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'newemail@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Everest',
                'handle_str': 'haydeneverest',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'newemail@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Everest',
                'handle_str': 'haydeneverest',
            }
        ],
        
    }

def test_setemail_invalid_email():
    """
    Pass in a user with valid token but invalid email.
    Should return InputError
    """ 
    clear_v1()
    user = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert user_profile_setemail_v2(user['token'], 'invalidemail.com')

def test_setemail_already_used():
    """
    Pass in a user with valid token but email already taken by someone else.
    Should return InputError
    """ 
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth_register_v2('usedemail@gmail.com', '123abc!@#', 'Fred', 'Smith')
    with pytest.raises(InputError):                        
        assert user_profile_setemail_v2(user_1['token'], 'usedemail@gmail.com')
    
def test_setemail_invalid_token():
    """
    Pass in a user with invalid token and valid email.
    Should return AccessError
    """ 
    clear_v1()
    auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(AccessError):                        
        assert user_profile_setemail_v2('invalid_token', 'newemail@gmail.com')

    
def test_setname():
    """
    Pass in a user with valid token and new name.
    The name in their data store should be replaced by the new name passed in.
    """
    clear_v1()
    user = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_profile_setname_v2(user['token'], 'Fred', 'Smith')
    user_info  = user_profile_v2(user['token'], user['auth_user_id'])
    assert user_info == {'user': {
                             'u_id': user['auth_user_id'],
                             'email': 'validemail0@gmail.com',
                             'name_first': 'Fred',
                             'name_last': 'Smith',
                             'handle_str': 'haydeneverest'          
    }}

def test_setname_channel_members():    
    """
    Pass in a user with valid token and new name.
    If they are a member of a channel, their info in the channel should also be updated.
    """ 
    clear_v1()
    user = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_profile_setname_v2(user['token'], 'Fred', 'Smith')
    channel_1 = channels_create_v2(user['token'], 'Channel1', True)
    channel_info = channel_details_v2(user['token'], channel_1['channel_id'])
    assert channel_info == {
        'name': 'Channel1',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'validemail@gmail.com',
                'name_first': 'Fred',
                'name_last': 'Smith',
                'handle_str': 'haydeneverest',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'validemail@gmail.com',
                'name_first': 'Fred',
                'name_last': 'Smith',
                'handle_str': 'haydeneverest',
            }
        ],
        
    }
    

def test_setname_invalid_firstname():
    """
    Pass in a user with valid token and but invalid first name.
    Should return AccessError
    """
    clear_v1()
    user = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):                        
        assert user_profile_setname_v2(user['token'], 'asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2', 'Smith')
        
def test_setname_invalid_lastname():
    """
    Pass in a user with valid token but invalid last name.
    Should return AccessError
    """
    clear_v1()
    user = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):                        
        assert user_profile_setname_v2(user['token'], 'Fred', 'asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2')
                
def test_setname_invalid_token():
    """
    Pass in a user with invalid token and valid new name.
    Should return AccessError
    """
    clear_v1()
    auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(AccessError):                        
        assert user_profile_setname_v2('invalid_token', 'Fred', 'Smith')

def test_sethandle():
    """
    Pass in a user with valid token and new handle.
    The handle in their data store is now replaced with this new handle.
    """
    clear_v1()
    user = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_profile_sethandle_v1(user['token'], 'newhandle')
    user_info  = user_profile_v2(user['token'], user['auth_user_id'])
    assert user_info == {'user': {
                             'u_id': user['auth_user_id'],
                             'email': 'validemail0@gmail.com',
                             'name_first': 'Hayden',
                             'name_last': 'Everest',
                             'handle_str': 'newhandle'          
    }}
    
def test_sethandle_channel_members():    
    """
    Pass in a user with valid token and new handle.
    If they are a member of a channel, their info in the channel should also be updated.
    """ 
    clear_v1()
    user = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_profile_sethandle_v1(user['token'], 'newhandle')
    channel_1 = channels_create_v2(user['token'], 'Channel1', True)
    channel_info = channel_details_v2(user['token'], channel_1['channel_id'])
    assert channel_info == {
        'name': 'Channel1',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'validemail@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Everest',
                'handle_str': 'newhandle',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'validemail@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Everest',
                'handle_str': 'newhandle',
            }
        ],
        
    }
    
def test_sethandle_invalid_token():
    """
    Pass in a user with invalid token and valid handle.
    """
    clear_v1()
    auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(AccessError):                        
        assert user_profile_sethandle_v1('invalid_token', 'newhandle')

def test_sethandle_invalid_handle():
    """
    Pass in a user with valid token but invalid handle.
    Should return InputError
    """
    clear_v1()
    user = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert user_profile_sethandle_v1(user['token'], 'thishandleislongerthantwentycharacters')

def test_sethandle_already_used():
    """
    Pass in a user with valid token but email already taken by someone else.
    Should return InputError
    """
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth_register_v2('usedemail@gmail.com', '123abc!@#', 'Fred', 'Smith')
    with pytest.raises(InputError):                        
        assert user_profile_sethandle_v1(user_1['token'], 'fredsmith')
    
