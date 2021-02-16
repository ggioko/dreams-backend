def user_profile_v1(auth_user_id, u_id):
    return {
        'user': {
            'u_id': 1,
            'email': 'cs1531@cse.unsw.edu.au',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle_str': 'haydenjacobs',
        },
    }

def user_profile_setname_v1(auth_user_id, name_first, name_last):
    return {
    }

def user_profile_setemail_v1(auth_user_id, email):
    return {
    }

def user_profile_sethandle_v1(auth_user_id, handle_str):
    return {
    }