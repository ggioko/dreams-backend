import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v2
from src.dm import dm_create_v1
from src.other import clear_v1
from src.helper import generate_token, get_token_user_id

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