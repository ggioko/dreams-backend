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
    with pytest.raises(InputError) as e:
        auth_register_v1("fold@home@stanford.edu", password, firstName, lastName)

    with pytest.raises(InputError) as e:
        auth_register_v1("hayden@coolem@ildomail.com", password, firstName, lastName)

    with pytest.raises(InputError) as e:
        auth_register_v1("@example.com", password, firstName, lastName)

    with pytest.raises(InputError) as e:
        auth_register_v1("hi@examp!e.com", password, firstName, lastName)

    with pytest.raises(InputError) as e:
        auth_register_v1("ab@~`example.com", password, firstName, lastName)

    with pytest.raises(InputError) as e:
        auth_register_v1("ab@example.!com", password, firstName, lastName)




def test_auth_register_taken_email():
    pass

def test_auth_register_invalid_password():
    pass

def test_auth_register_invalid_firstname():
    pass

def test_auth_register_invalid_lastname():
    pass