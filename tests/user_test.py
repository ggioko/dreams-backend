import pytest
#from src.helper import get_token_user_id
from src.error import InputError, AccessError
#from src.data import data
from src.auth import auth_register_v2
from src.other import clear_v1
from src.user import users_all_v1, user_profile_v2
from src.helper import generate_token

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
        {'u_id': 1, 'email': 'validemail@gmail.com', 'name_first': 'Hayden', 'name_last': 'Everest', 'handle_str': 'HaydenEverest'},
        {'u_id': 2, 'email': 'validemail22@gmail.com', 'name_first': 'Haydennn', 'name_last': 'Everesttt', 'handle_str': 'HaydennnEveresttt'}
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
                             'handle_str': 'HaydenEverest'          
          }}
    
