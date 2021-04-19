from src.helper import get_token_user_id
from src.data import data


def notifications_get_v1(token):
    """
    Returns the user's 20 most recent notifications.

    Arguments:
        token (string)    - Token

    Exceptions:
        AccessError  - Invalid token

    Return Value:
        Returns {notifications} on success.
    """
    u_id = get_token_user_id(token)
    
    for user in data['users']:
        if user['u_id'] == u_id:
            notifs_list = user['notifications']
            
        if len(notifs_list) >= 20:
            notifications = notifs_list[::-1][0:20]
        else:
            notifications = notifs_list[::-1]
        return notifications