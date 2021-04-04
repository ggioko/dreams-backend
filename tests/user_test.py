import pytest

from src.other import clear_v1
from src.auth import auth_register_v2
from src.user import user_profile_v2
#from src.helper import get_token_user_id
from src.error import InputError, AccessError

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
    
