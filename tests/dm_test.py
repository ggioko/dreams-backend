import pytest
from src.error import InputError, AccessError
from src.dm import dm_create_v1, dm_details_v1, dm_leave_v1
from src.auth import auth_register_v2
from src.other import clear_v1
from src.helper import get_token_user_id, generate_token

# Testing when valid infomation is passes throught dm_leave
# expected success
def test_dm_details():
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
    dm_details_1 = dm_details_v1(user_1['token'], dm_1['dm_id'])
    assert dm_details_1['name'] == "fredsmith, haydeneverest, jimmybarnes"
    assert dm_details_1['members'] == [{'u_id': 1, 'email': 'validemail0@gmail.com', 'name_first': 'Hayden', 'name_last': 'Everest', 'handle_str': 'haydeneverest',},
                                        {'u_id': 2, 'email': 'validemail1@gmail.com', 'name_first': 'Fred', 'name_last': 'Smith', 'handle_str': 'fredsmith', },
                                        {'u_id': 3, 'email': 'validemail2@gmail.com', 'name_first': 'Jimmy', 'name_last': 'Barnes', 'handle_str': 'jimmybarnes',}]

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
    
    # generate invalid token using helper function
    invalid_token = generate_token(4)

    with pytest.raises(AccessError):
        assert dm_details_v1(invalid_token, dm_1['dm_id'])

# Testing when an invalid DM ID is used
# expected InputError
def test_dm_details_invalid_dm_id():
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')

    with pytest.raises(InputError):
        assert dm_details_v1(user_1['token'], 5)

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

# Testing when an invalid token is used
# expected AccessError
def test_dm_create_invalid_token():
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    u_id1 = get_token_user_id(user_1['token'])
    u_id2 = get_token_user_id(user_2['token'])       
    invalid_token = generate_token(4)
    with pytest.raises(AccessError):
        assert dm_create_v1(invalid_token, [u_id1, u_id2])

# Testing when an u_id does not refer to a valid member
# expected InputError
def test_dm_create_invalid_u_id():
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    u_id1 = get_token_user_id(user_2['token'])      
    u_id2 = 4
    with pytest.raises(InputError):
        assert dm_create_v1(user_1['token'], [u_id1, u_id2])

# Testing when creating a DM create is successful
def test_dm_create_success():
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    user_3 = auth_register_v2('thirdemail@gmail.com', '321bca#@!', 'Bob', 'Jones')
    u_id1 = get_token_user_id(user_2['token'])
    u_id2 = get_token_user_id(user_3['token'])
    new_dm = dm_create_v1(user_1['token'], [u_id1, u_id2])
    assert new_dm['dm_id'] == 1
    assert new_dm['dm_name'] == "bobjones, fredsmith, haydeneverest"       

# Testing dm_remove for error handling
def test_dm_leave_errors():
    # Clear data
    clear_v1()
    # Register members and setup data
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    user_3 = auth_register_v2('thirdemail@gmail.com', '321bca#@!', 'Bob', 'Jones')
    u_id1 = user_2['auth_user_id']
    new_dm = dm_create_v1(user_1['token'], [u_id1])

    # Testing when an invalid token is used
    # expected AccessError
    with pytest.raises(AccessError):
        assert dm_leave_v1(-1, new_dm['dm_id'])

    # Testing when an invalid DM ID is used
    # expected InputError
    with pytest.raises(InputError):
        assert dm_leave_v1(user_1['token'], 10)

    # Testing when an authorised id is not a member of DM
    # expected AcessError
    with pytest.raises(AccessError):
        assert dm_leave_v1(user_3['token'], new_dm['dm_id'])

# Testing when valid infomation is passes through dm_leave
# expected success
def test_dm_leave():
    # Clear data
    clear_v1()
    # Register members and setup data
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    user_3 = auth_register_v2('thirdemail@gmail.com', '321bca#@!', 'Bob', 'Jones')

    # get user ids of members
    u_id1 = user_2['auth_user_id']
    u_id2 = user_3['auth_user_id']

    # create a new dm
    new_dm = dm_create_v1(user_1['token'], [u_id1, u_id2])
    # remove user_2
    dm_leave_v1(user_3['token'], new_dm['dm_id'])
    # get details of dm
    dm_details = dm_details_v1(user_1['token'], new_dm['dm_id'])
    assert dm_details['members'] == [{'u_id': 1, 'email': 'validemail@gmail.com', 'name_first': 'Hayden', 'name_last': 'Everest', 'handle_str': 'haydeneverest',},
                        {'u_id': 2, 'email': 'secondemail@gmail.com', 'name_first': 'Fred', 'name_last': 'Smith', 'handle_str': 'fredsmith', },]


