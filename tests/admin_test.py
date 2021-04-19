import pytest

from src.auth import auth_register_v2, auth_login_v2
from src.admin import userpermission_change_v1, user_remove_v1
from src.helper import no_check_dreams_change_permission
from src.user import user_profile_v2
from src.error import InputError, AccessError
from src.other import clear_v1

def test_admin_userpermission_invalid_token():
    '''
    Passes in an invalid token and valid u_id to admin_userpermission_change
    Should return AccessError
    '''
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('validemail2@gmail.com', '1234abc!@#', 'Haydenn', 'Everestt')
    with pytest.raises(AccessError):
        assert userpermission_change_v1('invalid_token', user2['auth_user_id'], 1)
        
def test_admin_userpermission_change_success():
    '''
    Tests userpermission_change_v1() with all correct information
    '''
    clear_v1()
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('validemail2@gmail.com', '1234abc!@#', 'Haydenn', 'Everestt')
    
    # Call helper function to make user1 dreams owner
    # Not a black box test, but no inbuilt functions allow for a dreams owner to be set without
    # there already being a dreams owner to make that change, so the data must be modified 
    # directly. This is done through a helper function in this case. If the system was deployed,
    # the owner would manually assign themselves this in the data structure before deployment.
    no_check_dreams_change_permission(user1['auth_user_id'], 1)

    assert userpermission_change_v1(user1['token'], user2['auth_user_id'], 1) == {}

def test_admin_userpermission_change_invalid_user():
    '''
    Tests userpermission_change_v1() with an invalid dreams ownership change
    '''
    clear_v1()
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    
    # Call helper function to make user1 dreams owner
    # Not a black box test, but no inbuilt functions allow for a dreams owner to be set without
    # there already being a dreams owner to make that change, so the data must be modified 
    # directly. This is done through a helper function in this case. If the system was deployed,
    # the owner would manually assign themselves this in the data structure before deployment.
    no_check_dreams_change_permission(user1['auth_user_id'], 1)

    with pytest.raises(InputError):
        userpermission_change_v1(user1['token'], user1['auth_user_id'] + 1, 1)

def test_admin_userpermission_change_invalid_permission():
    '''
    Tests userpermission_change_v1() with an invalid new dreams permission
    '''
    clear_v1()
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('validemail2@gmail.com', '1234abc!@#', 'Haydenn', 'Everestt')

    # Call helper function to make user1 dreams owner
    # Not a black box test, but no inbuilt functions allow for a dreams owner to be set without
    # there already being a dreams owner to make that change, so the data must be modified 
    # directly. This is done through a helper function in this case. If the system was deployed,
    # the owner would manually assign themselves this in the data structure before deployment.
    no_check_dreams_change_permission(user1['auth_user_id'], 1)

    with pytest.raises(InputError):
        userpermission_change_v1(user1['token'], user2['auth_user_id'], 100)

def test_admin_userpermission_change_nonowner_request():
    '''
    Tests userpermission_change_v1() with the request being added by a nonowner of **dreams**
    '''
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('validemail2@gmail.com', '1234abc!@#', 'Haydenn', 'Everestt')
    user3 = auth_register_v2('validemail3@gmail.com', '1234abc!@#', 'Fred', 'Smith')
    
    with pytest.raises(AccessError):
        userpermission_change_v1(user2['token'], user3['auth_user_id'], 1)

def test_admin_user_remove_invalid_token():
    '''
    Passes in an invalid token and valid u_id to admin_user_remove_v1
    Should return AccessError
    '''
    clear_v1()
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(AccessError):
        assert user_remove_v1('invalid_token', user1['auth_user_id'])

def test_admin_user_remove_invalid_uid():
    '''
    Passes in a valid token and invalid u_id to admin_user_remove_v1
    Should return InputError
    '''
    clear_v1()
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert user_remove_v1(user1['token'], -1)

def test_admin_user_remove_sole_owner():
    '''
    Passes in a valid token and valid u_id to admin_user_remove_v1
    Should return InputError, as the user is the only owner of Dreams.
    '''
    clear_v1()
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert user_remove_v1(user1['token'], user1['auth_user_id'])
        
def test_admin_user_remove_not_owner():
    '''
    Passes in a valid token and valid u_id to admin_user_remove_v1
    Should return AccessError, as the user trying to remove the other user is not an owner of Dreams.
    '''
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('validemail2@gmail.com', '1234abc!@#', 'Haydenn', 'Everestt')
    user3 = auth_register_v2('validemail3@gmail.com', '1234abc!@#', 'Haydennn', 'Everesttt')
    with pytest.raises(AccessError):
        assert user_remove_v1(user2['token'], user3['auth_user_id'])
        
def test_admin_user_remove_works():
    '''
    User1 passes in a valid token and user2's u_id to admin_user_remove_v1
    Upon removal of user2, user_profile_v2 will be called and should return
    their profile with 'Removed user' as the name.
    User2 will then attempt to log in - InputError should be returned.
    '''
    clear_v1()
    user1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    user2 = auth_register_v2('validemail2@gmail.com', '1234abc!@#', 'Haydenn', 'Everestt')
    user_remove_v1(user1['token'], user2['auth_user_id'])
    user_info = user_profile_v2(user1['token'], user2['auth_user_id'])
    assert user_info == {'user': {
                             'u_id': user2['auth_user_id'],
                             'email': 'validemail2@gmail.com',
                             'name_first': 'Removed',
                             'name_last': 'user',
                             'handle_str': 'haydenneverestt'          
    }}
    with pytest.raises(InputError):
        assert auth_login_v2('validemail2@gmail.com', '1234abc!@#')

   
    
        
        









    
    
    
    
    
    