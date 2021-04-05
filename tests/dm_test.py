import pytest
from src.error import InputError, AccessError
from src.dm import dm_create_v1, dm_details_v1, dm_remove_v1, dm_invite_v1, dm_leave_v1, dm_list_v1

from src.auth import auth_register_v2
from src.other import clear_v1


def test_dm_details():
    """
    Testing when valid infomation is passed through dm_details
    Expected: success
    """
    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('validemail1@gmail.com', '123abc!@#', 'Fred', 'Smith')
    user_3 = auth_register_v2('validemail2@gmail.com', '123abc!@#', 'Jimmy', 'Barnes')

    # get user ids
    u_id1 = user_2['auth_user_id']
    u_id2 = user_3['auth_user_id']

    # create a new DM
    dm_1 = dm_create_v1(user_1['token'], [u_id1, u_id2])
    dm_details_1 = dm_details_v1(user_1['token'], dm_1['dm_id'])
    assert dm_details_1['name'] == "fredsmith, haydeneverest, jimmybarnes"
    assert dm_details_1['members'] == [{'u_id': 1, 'email': 'validemail0@gmail.com', 'name_first': 'Hayden', 'name_last': 'Everest', 'handle_str': 'haydeneverest',},
                                        {'u_id': 2, 'email': 'validemail1@gmail.com', 'name_first': 'Fred', 'name_last': 'Smith', 'handle_str': 'fredsmith', },
                                        {'u_id': 3, 'email': 'validemail2@gmail.com', 'name_first': 'Jimmy', 'name_last': 'Barnes', 'handle_str': 'jimmybarnes',}]

def test_dm_details_invalid_token():
    """
    Testing when an invalid token is used
    Expected: AccessError
    """
    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('validemail1@gmail.com', '123abc!@#', 'Fred', 'Smith')
    user_3 = auth_register_v2('validemail2@gmail.com', '123abc!@#', 'Jimmy', 'Barnes')

    # get user ids
    u_id1 = user_2['auth_user_id']
    u_id2 = user_3['auth_user_id']

    # create a new DM
    dm_1 = dm_create_v1(user_1['token'], [u_id1, u_id2])

    with pytest.raises(AccessError):
        assert dm_details_v1(-1, dm_1['dm_id'])

def test_dm_details_invalid_dm_id():
    """
    Testing when an invalid DM ID is used
    Expected: InputError
    """
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')

    with pytest.raises(InputError):
        assert dm_details_v1(user_1['token'], 5)

def test_dm_details_invalid_authorised_member():
    """
    Testing when an authorised id is not a member of DM
    Expected: AcessError
    """

    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail0@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('validemail1@gmail.com', '123abc!@#', 'Fred', 'Smith')
    user_3 = auth_register_v2('validemail2@gmail.com', '123abc!@#', 'Jimmy', 'Barnes')
    user_4 = auth_register_v2('validemail3@gmail.com', '123abc!@#', 'Bob', 'Jones')

    # get user ids
    u_id1 = user_2['auth_user_id']
    u_id2 = user_3['auth_user_id']

    # create a new DM
    dm_1 = dm_create_v1(user_1['token'], [u_id1, u_id2])

    with pytest.raises(AccessError):
        assert dm_details_v1(user_4['token'], dm_1['dm_id'])

def test_dm_create_invalid_token():
    """
    Testing when an invalid token is used
    Expected: AccessError
    """

    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    u_id1 = user_1['auth_user_id']
    u_id2 = user_2['auth_user_id'] 
    with pytest.raises(AccessError):
        assert dm_create_v1(-1, [u_id1, u_id2])

def test_dm_create_invalid_u_id():
    """
    Testing for when an u_id does not refer to a valid member
    Expected: InputError
    """

    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    u_id1 = user_2['auth_user_id']
    u_id2 = 4
    with pytest.raises(InputError):
        assert dm_create_v1(user_1['token'], [u_id1, u_id2])

def test_dm_create_success():
    """
    Testing when valid information passed through dm_create
    Expected: success
    """

    # clear data and register members
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    user_3 = auth_register_v2('thirdemail@gmail.com', '321bca#@!', 'Bob', 'Jones')
    u_id1 = user_2['auth_user_id']
    u_id2 = user_3['auth_user_id']
    new_dm = dm_create_v1(user_1['token'], [u_id1, u_id2])
    assert new_dm['dm_id'] == 1
    assert new_dm['dm_name'] == "bobjones, fredsmith, haydeneverest"       


def test_dm_list_invalid_token():
    """
    Pass in an invalid token
    Should return AccessError
    """
    clear_v1()
    with pytest.raises(AccessError):
        assert dm_list_v1('invalid_token')
        
def test_dm_list_success():
    """
    Pass in a valid token from a user.
    Should return list of DM's that the user is a member of.
    Output: {dms} - {dm_id, name}
    """
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    user_3 = auth_register_v2('thirdemail@gmail.com', '321bca#@!', 'Bob', 'Jones')
    u_id1 = user_1['auth_user_id']
    u_id2 = user_2['auth_user_id']
    u_id3 = user_3['auth_user_id']
    new_dm = dm_create_v1(user_1['token'], [u_id2, u_id3])
    new_dm_2 = dm_create_v1(user_2['token'], [u_id1])
    dms = dm_list_v1(user_1['token'])
    assert dms == {
        'dms': [
        {
                'dm_id': new_dm['dm_id'], 
                'name': new_dm['dm_name']
        },
        {
                'dm_id': new_dm_2['dm_id'],
                'name': new_dm_2['dm_name']
        }
        ],
    }

    
def test_dm_leave_errors():
    """
    Testing dm_leave for errors
    """

    # Clear data
    clear_v1()
    # Register members and setup data
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    user_3 = auth_register_v2('thirdemail@gmail.com', '321bca#@!', 'Bob', 'Jones')
    u_id1 = user_2['auth_user_id']
    new_dm = dm_create_v1(user_1['token'], [u_id1])

    # Testing when an invalid token is used
    # Expected: AccessError
    with pytest.raises(AccessError):
        assert dm_leave_v1(-1, new_dm['dm_id'])

    # Testing when an invalid DM ID is used
    # Expected: InputError
    with pytest.raises(InputError):
        assert dm_leave_v1(user_1['token'], 10)

    # Testing when an authorised id is not a member of DM
    # Expected: AcessError
    with pytest.raises(AccessError):
        assert dm_leave_v1(user_3['token'], new_dm['dm_id'])

def test_dm_leave():
    """
    Testing when valid infomation is passes through dm_leave
    Expected: success
    """

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


    assert new_dm['dm_name'] == "bobjones, fredsmith, haydeneverest"

def test_dm_remove_valid():
    """
    Test to see if dm removes when the owner calls the function
    DM details is expected to return an error from not being able to find
    the DM
    """
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    dm = dm_create_v1(user_1['token'], [user_2['auth_user_id']])
    assert dm_details_v1(user_1['token'], dm['dm_id'])
    dm_remove_v1(user_1['token'], dm['dm_id'])
    with pytest.raises(InputError):
        assert dm_details_v1(user_1['token'], dm['dm_id'])

def test_dm_remove_invalid_dm_id():
    """
    Test to see if dm raises input error from invalid dm_id
    """
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert dm_remove_v1(user_1['token'], -1)

def test_dm_remove_non_creator():
    """
    Test to see if dm raises access error when user is not dm owner
    """
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    dm = dm_create_v1(user_1['token'], [user_2['auth_user_id']])
    with pytest.raises(AccessError):
        assert dm_remove_v1(user_2['token'], dm['dm_id'])


def test_dm_invite_valid():
    """
    Test to see if dm invite works by inviting a user then
    them calling dm_details 
    """
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    user_3 = auth_register_v2('thirdemail@gmail.com', '321bca#@!', 'Bob', 'Jones')
    dm = dm_create_v1(user_1['token'], [user_2['auth_user_id']])
    dm_invite_v1(user_1['token'], dm['dm_id'], user_3['auth_user_id'])

    assert dm_details_v1(user_3['token'], dm['dm_id'])

def test_dm_invite_invalid_dm_id():
    """
    Test to see if dm invite raises input error by passing in
    an invalid DM ID 
    """
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    user_3 = auth_register_v2('thirdemail@gmail.com', '321bca#@!', 'Bob', 'Jones')
    dm_create_v1(user_1['token'], [user_2['auth_user_id']])

    with pytest.raises(InputError):
        assert dm_invite_v1(user_1['token'], 33, user_3['auth_user_id'])

def test_dm_invite_invalid_u_id():
    """
    Test to see if dm invite raises input error by passing in
    an invalid User ID 
    """
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    auth_register_v2('thirdemail@gmail.com', '321bca#@!', 'Bob', 'Jones')
    dm = dm_create_v1(user_1['token'], [user_2['auth_user_id']])

    with pytest.raises(InputError):
        assert dm_invite_v1(user_1['token'], dm['dm_id'], 33)

def test_dm_invite_invalid_token():
    """
    Test to see if dm invite raises access error by passing in
    an invalid token
    """
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    user_3 = auth_register_v2('thirdemail@gmail.com', '321bca#@!', 'Bob', 'Jones')
    dm = dm_create_v1(user_1['token'], [user_2['auth_user_id']])

    with pytest.raises(AccessError):
        assert dm_invite_v1(33, dm['dm_id'], user_3['auth_user_id'])

def test_dm_invite_non_member():
    """
    Test to see if dm invite raises access error when a user
    who is not a member of the dm tries to invite someone
    """
    clear_v1()
    user_1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user_2 = auth_register_v2('secondemail@gmail.com', '321cba#@!', 'Fred', 'Smith')
    user_3 = auth_register_v2('thirdemail@gmail.com', '321bca#@!', 'Bob', 'Jones')
    dm = dm_create_v1(user_1['token'], [user_2['auth_user_id']])

    with pytest.raises(AccessError):
        assert dm_invite_v1(user_3['token'], dm['dm_id'], user_3['auth_user_id'])
