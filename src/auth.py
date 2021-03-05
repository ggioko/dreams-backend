from src.error import InputError
from src.data import data
import re

def auth_login_v1(email, password):
    # Given a registered users' email and password and returns their `auth_user_id` value
    # Loop checking if email in list of registered users
    for user in data['users']:
        if email in user['email']:
            reuser = {
                'u_id' : user['u_id'],
                'password' : user['password']
            }
            # Check if the passwords match
            if password == reuser.get('password'):
                auth_user_id = reuser.get('u_id')
                return auth_user_id
            else:
                raise InputError
        else:
            raise InputError

    '''
    if len(data['users']) != 0:
        # Check if email is registered
        email_registered = [data['users'][c]['email'] for c in range(len(data['users']))]
        if email not in email_registered:
            raise InputError
        elif email in email_registered:
            # Check if the password given matches
            password_check = [data['users'][c]['password']for c in range(len(data['users']))]
            if password not in password_check: 
                raise InputError
            elif password in password_check:
                get_id = int(data['users'][c]['u_id'])
                return {'auth_user_id': get_id}
    '''

"""
Registers the user and puts their information into a database

Arguments:
    email (string)    - Users email
    password (string)    - Users set password
    name_first (string)    - Users first name
    name_last (string)    - Users last name

Exceptions:
    InputError  - Occurs when email in use, password shorter than 6 characters
                first name or last name not within 1-50 characters, incorrect 
                email format

Return Value:
    Returns {'auth_user_id': id,} on sucess

"""

def auth_register_v1(email, password, name_first, name_last):
    # Check if users data is empty
    if len(data['users']) != 0:
        # Email in use check
        emails = [data['users'][c]['email'] for c in range(len(data['users']))]
        if email in emails:
            raise InputError('Email already in use')

        # Gets a new id
        ids = [data['users'][c]['u_id'] for c in range(len(data['users']))]
        for i in range(1,len(data['users']) + 2):
            if i not in ids:
                id = i
                break

        # Creates a new handle
        handle = name_first + name_last
        handle = handle[0:20]
        handles = [data['users'][c]['handle_str'] for c in range(len(data['users']))]
        duplicate = True
        count = 0
        while duplicate:
            if handle in handles:
                handle += str(count)
                count += 1
            else:
                duplicate = False
    else:
        id = 1
        handle = name_first + name_last
        handle = handle[0:20]

    # Password size check
    if len(password) < 6:
        raise InputError('Password needs to be longer than 6 characters')

    # Name size check
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError('First name needs to be between 1 and 50 characters')
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError('Last name needs to be between 1 and 50 characters')

    # Email syntax check
    if not re.match('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$',email):
        raise InputError('Incorrect email format')
  
    # Saves user data
    user = {
        'u_id': id,
        'email': email,
        'password' : password,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle,
    }
    data['users'].append(user)

    return id
