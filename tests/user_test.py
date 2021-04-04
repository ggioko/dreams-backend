import pytest
from src.data import data
from src.auth import auth_register_v2
from src.other import clear_v1, users_all_v1
from src.error import InputError, AccessError
from src.helper import generate_token

def test_users_all_v1_successful():
    '''
    Registers some users and provides a valid token to users_all_v1 returning a list of all registered users
    '''
    clear_v1()
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('validemail22@gmail.com', '1234abc!@#', 'Haydennn', 'Everesttt')
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