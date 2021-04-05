import pytest

from src.auth import auth_register_v2
from src.admin import userpermission_change_v1
from src.data import data
from src.helper import no_check_dreams_make_owner

from src.error import InputError, AccessError
from src.other import clear_v1

def test_admin_userpermission_change_success():
    '''
    Tests userpermission_change_v1() with all correct information
    '''
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('validemail2@gmail.com', '1234abc!@#', 'Haydenn', 'Everestt')
    
    # Call helper function to make user1 dreams owner

    assert userpermission_change_v1(user1['token'], user2['u_id'], 1) == {}

def test_admin_userpermission_change_invalid_user():
    '''
    Tests userpermission_change_v1() with an invalid dreams ownership change
    '''
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    
    # Call helper function to make user1 dreams owner

    with pytest.raises(InputError):
        userpermission_change_v1(user1['token'], user1['u_id'] + 1, 1)

def test_admin_userpermission_change_invalid_permission():
    '''
    Tests userpermission_change_v1() with an invalid new dreams permission
    '''
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('validemail2@gmail.com', '1234abc!@#', 'Haydenn', 'Everestt')

    # Call helper function to make user1 dreams owner

    assert userpermission_change_v1(user1['token'], user2['u_id'], 100) == {}

def test_admin_userpermission_change_nonowner_request():
    '''
    Tests userpermission_change_v1() with the request being added by a nonowner of **dreams**
    '''
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('validemail2@gmail.com', '1234abc!@#', 'Haydenn', 'Everestt')

    assert userpermission_change_v1(user1['token'], user2['u_id'], 1) == {}
