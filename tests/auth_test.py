import pytest

from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError
from src.other import clear_v1

def test_auth_register_valid():
    clear_v1()
    id1 = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id2 = auth_register_v1('valid2email@gmail.com', '123abc!@#', 'Haydens', 'Everests')
    assert id1 != id2

def test_auth_register_invalid_email():
    clear_v1()
    password = "Pass123"
    firstName = "John"
    lastName = "Smith"

    with pytest.raises(InputError):
        assert auth_register_v1("hayden@coolem@ildomail.com", password, firstName, lastName)
        assert auth_register_v1("@example.com", password, firstName, lastName)
        assert auth_register_v1("hi@!$%$#!!.com", password, firstName, lastName)
        assert auth_register_v1("ab@~`example.com", password, firstName, lastName)
        assert auth_register_v1("ab@example.!c!o!m", password, firstName, lastName)
        assert auth_register_v1("numbers@0934.23980477", password, firstName, lastName)
        assert auth_register_v1("numbers@0934.com", password, firstName, lastName)
        assert auth_register_v1("numbers@example.1337", password, firstName, lastName)
        assert auth_register_v1('invalidemailgmail.com', '1234567', 'Hayden', 'Everest')
        assert auth_register_v1('invalidemail@gmail', '7654321', 'Haydena', 'Everesta')

def test_auth_register_taken_email():
    clear_v1()
    assert auth_register_v1('taken@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert auth_register_v1('taken@gmail.com', '123aqwe#', 'Imposter', 'Red')

def test_auth_register_invalid_password():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v1('invalidpass@.com', 'abc', 'Hayden', 'Everest')

def test_auth_register_invalid_firstname():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v1('invalidfirstname@gmail.com', 'abc21312', '', 'Everest')
        assert auth_register_v1('invalidfirstname2@gmail.com', 'abc123123', 'asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2', 'Everest')

def test_auth_register_invalid_lastname():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v1('invalidlastname@gmail.com', 'abc123123', 'Everest', '')
        assert auth_register_v1('invalidlastname2@gmail.com', 'abc123123', 'Everest', 'asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2')
