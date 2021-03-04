# Data storage global variable
data = {
    'users': [
        {
            'u_id': 1,
            'email': 'cs1531@cse.unsw.edu.au',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle_str': 'haydenjacobs',
        },
    ],
    'channels': [
        {
            'id': 1,
            'name' : 'channel1',
        },
        {
            'id': 2,
            'name' : 'channel2',
        },
    ],
}

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }


def auth_register_v1(email, password, name_first, name_last):
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
    

    # Saves user data
    user = {
        'u_id': id,
        'email': email,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle,
    }

    data['users'].append(user)
    
    print(data['users'])
    print(f"id: {id}    handle: {handle}")

    return {
        'auth_user_id': id,
    }

if __name__ == "__main__":
    auth_register_v1("a@gmail.com", "password","123456789012345678901","user")
