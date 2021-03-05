from src.error import InputError
from src.data import data
import re

def auth_login_v1(email, password):
    # Given a registered users' email and password and returns their `auth_user_id` value

    # Check email syntax
    if not re.match('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$',email):
        raise InputError('Email entered is not a valid email')
    
    # Loop checking if email is not in list of registered users
    emails = [data['users'][c]['email'] for c in range(len(data['users']))]
    if email not in emails:
        raise InputError('Email entered does not belong to a user')
    
    if len(data['users']) != 0:
        # Loop until an email match
        for user in data['users']:
            if email == user['email']:
                # Copy the password and user_id for the email match
                reuser = {
                    'u_id' : user['u_id'],
                    'password' : user['password']
                }
                # Check if the passwords match
                if password == reuser.get('password'):
                    auth_user_id = reuser.get('u_id')
                    return auth_user_id
                else:
                    raise InputError('Password is not correct')
    else:
        raise InputError('No registered users detected')

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
