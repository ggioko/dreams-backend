import pytest

from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.error import InputError

def test_auth_register_valid():
    result = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    assert result == "haydeneverest"
    result2 = auth_register_v1('validemail2@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    assert result2 == "haydeneverest0"

def test_auth_register_invalid_email():
    with pytest.raises(InputError):
        assert auth_register_v1('invalidemailgmail.com', '1234567', 'Hayden', 'Everest')
        assert auth_register_v1('invalidemail@gmail', '7654321', 'Haydena', 'Everesta')

def test_auth_register_taken_email():
    assert auth_register_v1('taken@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert auth_register_v1('taken@gmail.com', '123aqwe#', 'Imposter', 'Red')

def test_auth_register_invalid_password():
    with pytest.raises(InputError):
        assert auth_register_v1('invalidpass@.com', 'abc', 'Hayden', 'Everest')

def test_auth_register_invalid_firstname():
    with pytest.raises(InputError):
        assert auth_register_v1('invalidfirstname@gmail.com', 'abc21312', '', 'Everest')
        assert auth_register_v1('invalidfirstname2@gmail.com', 'abc123123', 'asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2', 'Everest')

def test_auth_register_invalid_lastname():
    with pytest.raises(InputError):
        assert auth_register_v1('invalidlastname@gmail.com', 'abc123123', 'Everest', '')
        assert auth_register_v1('invalidlastname2@gmail.com', 'abc123123', 'Everest', 'asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2')
