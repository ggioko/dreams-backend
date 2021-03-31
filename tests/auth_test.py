import pytest

from src.auth import auth_login_v1
from src.auth import auth_register_v2
from src.other import clear_v1
from src.error import InputError
from src.other import clear_v1

def test_auth_register_valid():
    clear_v1()
    id1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id2 = auth_register_v2('valid2email@gmail.com', '123abc!@#', 'Haydens', 'Everests')
    assert id1['auth_user_id'] != id2['auth_user_id']
    assert id1['token'] != id2['token']

def test_auth_register_invalid_email():
    clear_v1()
    password = "Pass123"
    firstName = "John"
    lastName = "Smith"

    with pytest.raises(InputError):
        assert auth_register_v2("hayden@coolem@ildomail.com", password, firstName, lastName)
        assert auth_register_v2("@example.com", password, firstName, lastName)
        assert auth_register_v2("hi@!$%$#!!.com", password, firstName, lastName)
        assert auth_register_v2("ab@~`example.com", password, firstName, lastName)
        assert auth_register_v2("ab@example.!c!o!m", password, firstName, lastName)
        assert auth_register_v2("numbers@0934.23980477", password, firstName, lastName)
        assert auth_register_v2("numbers@0934.com", password, firstName, lastName)
        assert auth_register_v2("numbers@example.1337", password, firstName, lastName)
        assert auth_register_v2('invalidemailgmail.com', '1234567', 'Hayden', 'Everest')
        assert auth_register_v2('invalidemail@gmail', '7654321', 'Haydena', 'Everesta')

def test_auth_register_taken_email():
    clear_v1()
    assert auth_register_v2('taken@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert auth_register_v2('taken@gmail.com', '123aqwe#', 'Imposter', 'Red')

def test_auth_register_invalid_password():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v2('invalidpass@.com', 'abc', 'Hayden', 'Everest')

def test_auth_register_invalid_firstname():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v2('invalidfirstname@gmail.com', 'abc21312', '', 'Everest')
        assert auth_register_v2('invalidfirstname2@gmail.com', 'abc123123', 'asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2', 'Everest')

def test_auth_register_invalid_lastname():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v2('invalidlastname@gmail.com', 'abc123123', 'Everest', '')
        assert auth_register_v2('invalidlastname2@gmail.com', 'abc123123', 'Everest', 'asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2')

def test_auth_login_valid_single_user():
    clear_v1()
    id1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id2 = auth_login_v1('validemail@gmail.com', '123abc!@#')
    assert id1['auth_user_id'] == id2['auth_user_id']

def test_auth_login_valid_multiple_users():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id2 = auth_register_v2('another@gmail.com', 'anoth432$%^', 'Random', 'Stranger')
    id3 = auth_register_v2('randomguy@gmail.com', 'abcEZ!123', 'Haydena', 'Friend')
    id4 = auth_login_v1('another@gmail.com', 'anoth432$%^')
    id5 = auth_login_v1('randomguy@gmail.com', 'abcEZ!123')
    assert id2['auth_user_id'] == id4['auth_user_id']
    assert id3['auth_user_id'] == id5['auth_user_id']

def test_auth_login_invalid_email():
    clear_v1()
    password = "Pass123"
    
    with pytest.raises(InputError):
        assert auth_login_v1("hayden@coolem@ildomail.com", password)
        assert auth_login_v1("@example.com", password)
        assert auth_login_v1("hi@!$%$#!!.com", password)
        assert auth_login_v1("ab@~`example.com", password)
        assert auth_login_v1("ab@example.!c!o!m", password)
        assert auth_login_v1("numbers@0934.23980477", password)
        assert auth_login_v1("numbers@0934.com", password)
        assert auth_login_v1("numbers@example.1337", password)
        assert auth_login_v1('invalidemailgmail.com', password)
        assert auth_login_v1('invalidemail@gmail', password)

def test_auth_login_unregistered_email():
    clear_v1()
    auth_register_v2('registered@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert auth_login_v1('unregistered@gmail.com', '123abc!@#')
        assert auth_login_v1('random@gmail.com', '123abc!@#')

def test_auth_login_invalid_password():
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert auth_login_v1('validemail@gmail.com', 'abc')
        assert auth_login_v1('validemail@gmail.com', '123abc#@!')