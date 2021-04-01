from src.data import data

def clear_v1():
    """
    Function to clear internal data
    """
    data['users'].clear()
    data['channels'].clear()

def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
