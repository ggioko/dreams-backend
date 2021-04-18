import pytest

from src.auth import auth_login_v2, auth_register_v2, auth_logout_v1
from src.other import clear_v1
from src.error import InputError, AccessError


def test_auth_register_valid():
    '''
    Registers two different users and checks that they have different user_ids and tokens given to them
    '''
    clear_v1()
    id1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id2 = auth_register_v2('valid2email@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    assert id1['auth_user_id'] != id2['auth_user_id']
    assert id1['token'] != id2['token']

def test_auth_register_invalid_email():
    '''
    Passes in emails with invalid syntax to test if InputError is raised
    Inlad emails are not in the form of '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    '''
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
    '''
    Tests that an email that is already registered in the database isnt going to registered again
    should raise an InputError if so. 
    '''
    clear_v1()
    assert auth_register_v2('taken@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert auth_register_v2('taken@gmail.com', '123aqwe#', 'Imposter', 'Red')

def test_auth_register_invalid_password():
    '''
    If the password entered is less than 6 characters long it raises an InputError
    '''
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v2('invalidpass@.com', 'abc', 'Hayden', 'Everest')

def test_auth_register_invalid_firstname():
    '''
    Tests thatname_first is between 1 and 50 characters inclusively in length
    '''
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v2('invalidfirstname@gmail.com', 'abc21312', '', 'Everest')
        assert auth_register_v2('invalidfirstname2@gmail.com', 'abc123123', 'asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2', 'Everest')

def test_auth_register_invalid_lastname():
    '''
    Tests that name_last is between 1 and 50 characters inclusively in length
    '''
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v2('invalidlastname@gmail.com', 'abc123123', 'Everest', '')
        assert auth_register_v2('invalidlastname2@gmail.com', 'abc123123', 'Everest', 'asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2asdvsdwu8d2')

def test_auth_login_valid_single_user():
    '''
    Tests if a valid user can login and ensure user_ids match
    '''
    clear_v1()
    id1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id2 = auth_login_v2('validemail@gmail.com', '123abc!@#')
    assert id1['auth_user_id'] == id2['auth_user_id']

def test_auth_login_valid_multiple_users():
    '''
    Tests that multiple users can logout with different u_ids
    '''
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    id2 = auth_register_v2('another@gmail.com', 'anoth432$%^', 'Random', 'Stranger')
    id3 = auth_register_v2('randomguy@gmail.com', 'abcEZ!123', 'Haydena', 'Friend')
    id4 = auth_login_v2('another@gmail.com', 'anoth432$%^')
    id5 = auth_login_v2('randomguy@gmail.com', 'abcEZ!123')
    assert id2['auth_user_id'] == id4['auth_user_id']
    assert id3['auth_user_id'] == id5['auth_user_id']

def test_auth_login_invalid_email():
    '''
    Passes in emails with invalid syntax to test if InputError is raised
    Inlad emails are not in the form of '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    '''
    clear_v1()
    password = "Pass123"
    with pytest.raises(InputError):
        assert auth_login_v2("hayden@coolem@ildomail.com", password)
        assert auth_login_v2("@example.com", password)
        assert auth_login_v2("hi@!$%$#!!.com", password)
        assert auth_login_v2("ab@~`example.com", password)
        assert auth_login_v2("ab@example.!c!o!m", password)
        assert auth_login_v2("numbers@0934.23980477", password)
        assert auth_login_v2("numbers@0934.com", password)
        assert auth_login_v2("numbers@example.1337", password)
        assert auth_login_v2('invalidemailgmail.com', password)
        assert auth_login_v2('invalidemail@gmail', password)

def test_auth_login_unregistered_email():
    '''
    Passes in a valid unregistered email into login. This should raise the exception - InputError.
    '''
    clear_v1()
    auth_register_v2('registered@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert auth_login_v2('unregistered@gmail.com', '123abc!@#')
        assert auth_login_v2('random@gmail.com', '123abc!@#')

def test_auth_login_invalid_password():
    '''
    Passes in a valid email and invalid password into login. This should raise the exception - InputError
    as the password given and the one in the database do not match.
    '''
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    with pytest.raises(InputError):
        assert auth_login_v2('validemail@gmail.com', 'abc')
        assert auth_login_v2('validemail@gmail.com', '123abc#@!')

def test_auth_logout_valid_token():
    '''
    Registers a user then logouts them out returning true
    '''
    clear_v1()
    id1 = auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    assert auth_logout_v1(id1['token']) == True

def test_auth_logout_invalid_token():
    '''
    Registers a user and provides an invalid token to logout returning false
    '''
    clear_v1()
    auth_register_v2('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    # uses the generate token helper that creates fake tokens for testing
    invalid_token = -1
    with pytest.raises(AccessError):
        assert auth_logout_v1(invalid_token)

def test_auth_passwordreset_reset_invalid_code():
    '''
    Given an incorrect reset code raises InputError
    '''
    clear_v1()
    with pytest.raises(InputError):
        auth_passwordreset_reset('abcd', '1234abc!@#')

def test_auth_passwordreset_reset_invalid_password():
    '''
    Given an incorrect password raises InputError
    '''
    clear_v1()
    with pytest.raises(InputError):
        auth_passwordreset_reset('abcd', '1')