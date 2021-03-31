# Data storage global variable
data = {
    'users': [
        {
            'u_id': 1,
            'email': 'cs1531@cse.unsw.edu.au',
            'password': 'abc1234',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'handle_str': 'haydenjacobs',
        },
    ],
    'channels': [
        {
            'id': 1,
            'name' : 'channel1',
            'is_public': True,
            'owner_members': [
                {
                    'u_id': 1,
                    'email': 'cs1531@cse.unsw.edu.au',
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                    'handle_str': 'haydenjacobs',
                },
            ],
            'all_members': [
                {
                    'u_id': 1,
                    'email': 'cs1531@cse.unsw.edu.au',
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                    'handle_str': 'haydenjacobs',
                },
            ],
        },
        {
            'id': 2,
            'name' : 'channel2',
            'is_public': True,
            'owner_members': [
            ],
            'all_members': [
            ],
            'messages' : [
                {
                    'message_id': 1,
                    'u_id': 1,
                    'message': 'Hello world',
                    'time_created': 1582426789,
                }
        ],
        },
    ],
    'active_tokens' : []
}
