from src.error import InputError
from src.data import data
import re

def auth_login_v1(email, password):
    # Given a registered users' email and password and returns their `auth_user_id` value

    if len(data['users']) != 0:
        # Check if email is registered
        email_registered = [data['users'][c]['email'] for c in range(len(data['users']))]
        if email in email_registered:
            # Check if the password given matches
            password_check = [data['users'][c]['password']]
            if password == password_check:
                get_id = int(data['users'][c]['u_id'])
                return {'auth_user_id': get_id}
    else:
        raise InputError

def auth_register_v1(email, password, name_first, name_last):
    return {
        'auth_user_id': 1,
    }
