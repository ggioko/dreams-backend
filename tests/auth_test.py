import pytest

from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.error import InputError
from src.other import clear_v1


def test_auth_register_valid():
    pass

def test_auth_register_invalid_email():
    pass

def test_auth_register_taken_email():
    pass

def test_auth_register_invalid_password():
    pass

def test_auth_register_invalid_firstname():
    pass

def test_auth_register_invalid_lastname():
    pass

def test_auth_login_valid_single_user():
    clear_v1
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    assert auth.auth_login('validemail@gmail.com', '123abc!@#')

def test_auth_login_valid_multiple_users():
    clear_v1
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    auth.auth_register('another@gmail.com', 'anoth432$%^', 'Random', 'Stranger')
    auth.auth_register('randomguy@gmail.com', 'abcEZ!123', 'Haydena', 'Friend')
    assert auth.auth_login('another@gmail.com', 'anoth432$%^') == 2
    assert auth.auth_login('randomguy@gmail.com', 'abcEZ!123') == 3

def test_auth_login_unregistered_email():
    clear_v1
    auth_register_v1('registered@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert auth.auth_login('unregistered@gmail.com', '123abc!@#')
        assert auth.auth_login('random@gmail.com', '123abc!@#')

def test_auth_login_invalid_password():
    clear_v1
    auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert auth.auth_login('validemail@gmail.com', 'abc')
        assert auth.auth_login('validemail@gmail.com', '123abc#@!')
