from src.error import InputError, AccessError
from src.data import data
from src.helper import get_token, get_user_data, email_in_use, get_token_user_id
import re
import jwt
import hashlib
import smtplib
import uuid

def auth_login_v2(email, password):
    """
    Given a registered users' email and password and returns their `auth_user_id` value and 'token'

    Arguments:
        email (string)    - Users email
        password (string)    - Users password

    Exceptions:
        InputError  - Occurs when email has an incorrect format, email is not
                    registered or when the password does not match the given
                    email

    Return Value:
        Returns {'auth_user_id': id,} on success
        Returns {'token': token,} on success
    """
    # Check email syntax
    if not re.match('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$',email):
        raise InputError(description='Email entered is not a valid email')
    
    # Loop checking if email is not in list of registered users
    if email_in_use(email) == False:
        raise InputError(description='Email entered does not belong to a user')
    
    # Hashs the given password to check with list of hashed passwords in 'users' later
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
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
                if password_hash == reuser.get('password'):
                    auth_user_id = reuser.get('u_id')
                    # gets a token from help function
                    token = get_token(reuser)
                    return {
                        'token': token,
                        'auth_user_id':auth_user_id,
                    }
                else:
                    raise InputError(description='Password is not correct')
    else:
        raise InputError(description='No registered users detected')

def auth_register_v2(email, password, name_first, name_last):
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
        Returns {'token' : token, 'auth_user_id': id} on success
    """
    # Check if users data is empty
    if len(data['users']) != 0:
        
        # Email in use check
        if email_in_use(email) == True:
            raise InputError(description='Email already in use')

        # Gets a new id
        ids = get_user_data('u_id')
        
        for i in range(1,len(data['users']) + 2):
            if i not in ids:# and i not in data['removed_u_ids']:
                id = i
                break
            
        permission_id = 0
        # Creates a new handle
        handle = name_first + name_last
        handle = handle[0:20]
        handles = get_user_data('handle_str')
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
        permission_id = 1

    # Password size check
    if len(password) < 6:
        raise InputError(description='Password needs to be longer than 6 characters')

    # Name size check
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description='First name needs to be between 1 and 50 characters')
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(description='Last name needs to be between 1 and 50 characters')

    # Email syntax check
    if not re.match('^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$',email):
        raise InputError(description='Incorrect email format')

    # Change handle to all lowercase
    handle = handle.lower()
    
    
    # Saves user data
    user = {
        'u_id': id,
        'email': email,
        'password' : hashlib.sha256(password.encode()).hexdigest(),
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle,
        'permission_id': permission_id,
        'notifications': [],
    }
    data['users'].append(user)
    token = get_token(user)

    return {
        'token' : token,
        'auth_user_id' : id, 
    }

def auth_logout_v1(token):
    """
    Given an active token, invalidates the token to log the user out

    Arguments:
        token (string)    - Token to invalidate

    Exceptions:
        N/A

    Return Value:
        Returns {'is_success': True} on success
    """

    active_tokens = data['active_tokens']

    # Check given token is valid
    if token not in active_tokens:
        raise AccessError(description='Invalid token')

    # Search through active tokens
    for x in active_tokens:
        # Once the given token matches an active token it invalidates it,
        # by popping it from the list of active tokens
        if x == token:
            active_tokens.remove(x)
            return True
    return False

def auth_passwordreset_request(email):
    """
    Given an email address, sends the user an email with a password reset string
    that can be given to passwordreset_reset.
    Arguments:
        email (string)    - email to look through

    Exceptions:
        N/A

    Return Value:
        Returns { }
    """
    reset_code = uuid.uuid4().hex

    email_found = False
    if len(data['users']) != 0:
        for user in data['users']:
            if user['email'] == email:
                email_found = True
                data['active_reset_codes'].append(reset_code)
                break
    if not email_found:
        return {}
    
    email_cred_username = 'f11bdorito@gmail.com'
    email_cred_password = 'd0ritostastegood!'

    subject = 'Dreams Password Reset Code'
    body = "Your password reset code is as follows: " + reset_code

    email_content = f"From: {email_cred_username}\n"
    email_content += f"To: {email}\n"
    email_content += f"Subject: {subject}\n"
    email_content += f"\n{body}\n"

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(email_cred_username, email_cred_password)
    server.sendmail(email_cred_username, [email], email_content)
    server.close()

    return {}

def auth_passwordreset_reset(reset_code, new_password):
    """
    Given a reset code for a user, set that user's new 
    password to the password provided

    Arguments:
        reset_code (string)      - JWT code to validate user
        new_password (string)    - Users new password

    Exceptions:
        InputError  - Password shorter than 6 characters
        InputError  - reset_code not valid

    Return Value:
        Returns {} on success
    """
    # Check for password length
    if len(new_password) < 6:
        raise InputError(description='Password needs to be longer than 6 characters')

    # Check for valid reset code
    if reset_code not in data['active_reset_codes']:
        raise InputError(description='Reset code is not a valid reset code')
    
    # Gets user id from reset code
    id = get_token_user_id(reset_code)

    # Hashes new password in prepartion for saving
    password = hashlib.sha256(new_password.encode()).hexdigest()

    # Replaces old password with new password
    if len(data['users']) != 0:
        for user in data['users']:
            if id == user['u_id']:
                data['active_reset_codes'].remove(reset_code)
                user['password'] = password
    
    return {}



