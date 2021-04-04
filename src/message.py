def message_send_v2(token, channel_id, message):
    return {
        'message_id': 1,
    }

def message_remove_v1(token, message_id):
    """
    Given a message_id for a message, this message is removed from the channel/DM

    Arguments:
        token (string)    - token
        message_id (int)    - messages id

    Exceptions:c
        InputError  - Occurs when the message_id no longer exists
        AccesError  - 

    Return Value:
        Returns {} - (empty dict) on success
    """
    return {
    }

def message_edit_v2(token, message_id, message):
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
    return {
    }