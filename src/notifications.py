from src.helper import get_token_user_id
from src.data import data
from src.helper import check_token_valid
from src.error import AccessError

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
    
    # Check if token is valid
    if check_token_valid(token) == False:
        raise AccessError(description='invalid token')
    
    # Otherwise, run function.
    u_id = get_token_user_id(token)
    for user in data['users']:
        if user['u_id'] == u_id:
            notifs_list = user['notifications']
            
            if len(notifs_list) >= 20:
                notifications = notifs_list[::-1][0:20]
            else:
                notifications = notifs_list[::-1]
                
            return notifications