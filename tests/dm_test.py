import pytest
from src.error import InputError, AccessError
from src.dm import dm_create_v1, dm_details_v1
from src.auth import auth_register_v2
from src.other import clear_v1
from src.helper import get_token_user_id, generate_token

# Testing when an invalid token is used
# expected AccessError
def test_dm_details_invalid_token():
    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('validemail1@gmail.com', '123abc!@#', 'Fred', 'Smith')
    user_3 = auth_register_v2('validemail2@gmail.com', '123abc!@#', 'Jimmy', 'Barnes')

    # get user id from token using helper function
    u_id1 = get_token_user_id(user_2['token'])
    u_id2 = get_token_user_id(user_3['token'])

    # create a new DM
    dm_1 = dm_create_v1(user_1['token'], [u_id1, u_id2])
    
    #generate invalid token using helper function
    invalid_token = generate_token(4)

    with pytest.raises(AccessError):
        assert dm_details_v1(invalid_token, dm_1['dm_id'])

# Testing when an invalid DM ID is used
# expected InputError
def test_dm_details_invalid_dm_id():
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')

    with pytest.raises(InputError):
        assert dm_details_v1(invalid_token, 5)

# Testing when an authorised id is not a member of DM
# expected AcessError
def test_dm_details_invalid_authorised_member():
    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('validemail1@gmail.com', '123abc!@#', 'Fred', 'Smith')
    user_3 = auth_register_v2('validemail2@gmail.com', '123abc!@#', 'Jimmy', 'Barnes')
    user_4 = auth_register_v2('validemail3@gmail.com', '123abc!@#', 'Bob', 'Jones')

    # get user id from token using helper function
    u_id1 = get_token_user_id(user_2['token'])
    u_id2 = get_token_user_id(user_3['token'])

    # create a new DM
    dm_1 = dm_create_v1(user_1['token'], [u_id1, u_id2])

    with pytest.raises(AccessError):
        assert dm_details_v1(user_4['token'], dm_1['dm_id'])