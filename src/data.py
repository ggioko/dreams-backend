# Data storage global variable
data = {
    'users': [
        {
            #'u_id': 1,
            #'email': 'cs1531@cse.unsw.edu.au',
            #'password': 'abc1234',
            #'name_first': 'Hayden',
            #'name_last': 'Jacobs',
            #'handle_str': 'haydenjacobs',
        },
    ],
    'removed_users': [
        {
            #'u_id': 1,
            #'email': 'cs1531@cse.unsw.edu.au',
            #'password': 'abc1234',
            #'name_first': 'Hayden',
            #'name_last': 'Jacobs',
            #'handle_str': 'haydenjacobs',
        },        
    ],
    'channels': [
        {
            #'id': 1,
            #'name' : 'channel1',
            #'is_public': True,
            'owner_members': [
                {
                    #'u_id': 1,
                    #'email': 'cs1531@cse.unsw.edu.au',
                    #'name_first': 'Hayden',
                    #'name_last': 'Jacobs',
                    #'handle_str': 'haydenjacobs',
                },
            ],
            'all_members': [
                {
                    #'u_id': 1,
                    #'email': 'cs1531@cse.unsw.edu.au',
                    #'name_first': 'Hayden',
                    #'name_last': 'Jacobs',
                    #'handle_str': 'haydenjacobs',
                },
            ],
            'messages' : [
                {
                    #'message_id': 1,
                    #'u_id': 1,
                    #'message': 'Hello world',
                    #'time_created': 1582426789,
                    'reacts' : [
                        {
                            #'react_id' : 1,
                            #'u_ids': [list of reacted u_id]
                            #'is_this_user_reacted': Boolean
                        },
                    ],
                    #'is_pinned' : Boolean,
                },
            ],
        },
    ],
    'dms' : [
        {
            #'dm_id': 1,
            #'name' : 'user_handles',
            'owner_members': [
                {
                    #'u_id': 1,
                    #'email': 'cs1531@cse.unsw.edu.au',
                    #'name_first': 'Hayden',
                    #'name_last': 'Jacobs',
                    #'handle_str': 'haydenjacobs',
                },
            ],
            'all_members': [
                {
                    #'u_id': 1,
                    #'email': 'cs1531@cse.unsw.edu.au',
                    #'name_first': 'Hayden',
                    #'name_last': 'Jacobs',
                    #'handle_str': 'haydenjacobs',
                },
            ],
            'messages' : [
                {
                    #'message_id': 1,
                    #'u_id': 1,
                    #'message': 'Hello world',
                    #'time_created': 1582426789,
                    'reacts' : [
                        {
                            #'react_id' : 1,
                            #'u_ids': [list of reacted u_id]
                            #'is_this_user_reacted': Booleanß
                        },
                    ],
                    #'is_pinned' : Boolean,
                },
            ],
        },
    ],
    'active_tokens' : [],
    'message_count' : 0,
}
