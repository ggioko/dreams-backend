import pytest

from src.auth import auth_login_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError


def test_auth_register_valid():
    pass

def test_auth_register_invalid_email():
    clear_v1()

    password = "Pass123"
    firstName = "John"
    lastName = "Smith"

    '''
    result = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError) as e:
        auth.auth_login('didntusethis@gmail.com', '123abcd!@#') # Expect fail since never registered

    '''

    with pytest.raises(InputError):
        assert auth_register_v1("hayden@coolem@ildomail.com", password, firstName, lastName)
        assert auth_register_v1("@example.com", password, firstName, lastName)
        assert auth_register_v1("hi@!$%$#!!.com", password, firstName, lastName)
        assert auth_register_v1("ab@~`example.com", password, firstName, lastName)
        assert auth_register_v1("ab@example.!c!o!m", password, firstName, lastName)
        assert auth_register_v1("numbers@0934.23980477", password, firstName, lastName)
        assert auth_register_v1("numbers@0934.23980477", password, firstName, lastName)
        assert auth_register_v1("numbers@0934.com", password, firstName, lastName)
        assert auth_register_v1("numbers@example.1337", password, firstName, lastName)

def test_auth_register_taken_email():
    pass

def test_auth_register_invalid_password():
    pass

def test_auth_register_invalid_firstname():
    pass

def test_auth_register_invalid_lastname():
    pass