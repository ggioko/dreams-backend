from src.error import InputError
import re

def isEmailValid(email):
    if re.match('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$', email):
	    return True
    return False

def auth_login_v1(email, password):
    email = email.lower()
    return {
        'auth_user_id': 1,
    }

def auth_register_v1(email, password, name_first, name_last):
    email = email.lower()
    if (isEmailValid(email) == False):
        raise InputError('Invalid email format')

    return {
        'auth_user_id': 1,
    }

if __name__ == "__main__":
    print(auth_register_v1("fold@home@stanford.edu", "Pass123", "John", "Smith"))
