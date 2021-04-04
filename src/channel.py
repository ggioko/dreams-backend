from src.error import InputError, AccessError
from src.data import data
from src.helper import get_token_user_id, check_token_valid, SECRET
import jwt
import hashlib

def channel_invite_v2(token, channel_id, u_id):
    '''
    channel_invite adds a user to a channel when an existing channel
    user invites them into the channel.

    Arguments:
        token (str)        - The token of the existing member of the channel
        channel_id (int)   - The ID of the channel that the new member is to join
        u_id (int)         - The ID of the user new to the channel

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
        AccessError - Occurs when channel_id refers to a channel that is private,
                      (where the authorised user is not a global owner)

    Return Value:
        Returns an empty dictionary when exceptions are not raised
    '''
    # Checks if the channel provided is a channel in the list
    foundChannel = {}
    for channel in data['channels']:
        if channel['id'] == channel_id:
            foundChannel = channel
            break
        print(channel['id'])
    if foundChannel == {}:
        raise InputError(description='Invalid channel ID provided')

    # Checks to see if invited user is a valid user of dreams
    userMatch = False
    for user in data['users']:
        print(user)
        if user['u_id'] == u_id:
            userMatch = True
            break
    if userMatch == False:
        raise InputError(description='Member to add not a valid user')

    # Checks to see if inviter is logged in
    token_active = False
    active_tokens = data['active_tokens']
    # Search through active tokens
    for x in active_tokens:
        if x == token:
            token_active = True
            break
    if (token_active == False):
        raise AccessError(description='Token invalid, user not logged in')
    
    # Gets ID of inviter
    decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
    auth_user_id = decoded_token['u_id']

    # Checks that inviter is authorised to invite new member
    userMatch = False
    for user in channel['all_members']:
        if user['u_id'] == auth_user_id:
            userMatch = True
            break
    if userMatch == False:
        raise AccessError(description='Authorised user not a channel member')

    # Add user to channel
    reuser = {}
    # Loop until u_id match
    for user in data['users']:
        if auth_user_id == user['u_id']:
            # Copy all the user data for easier access
            reuser = {
                'u_id': user['u_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
            }

    # Added user to all members for channel
    for channel in data['channels']:
        if channel['id'] == channel_id:
            channel['all_members'].append(reuser)
    
    return {
    }



def channel_details_v1(auth_user_id, channel_id):    
    '''
    channel_details_v1()

    Given a Channel with ID channel_id that the authorised user is part of, 
        provide basic details about the channel.

    Arguments: 
        auth_user_id (int), channel_id (int)
        
    Exception: 
        AccessError - Occurs when auth_user_id passed in is not a valid id.
        AccessError - Occurs when authorised user is not a member of channel with channel_id.
        InputError - Channel ID is not a valid channel.
        
    Return value: 
        {name, owner_members, all_members} on success
    '''
    # Check if auth_user_id matches a user in the database.
    user_valid = 0
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            user_valid = 1
    if user_valid == 0:
        raise AccessError("Error occurred auth_user_id is not valid")
        
    # Check to see if channel_id matches a channel in the database.
    channel_valid = 0
    for channel in data['channels']:
        if channel['id'] == channel_id:
            channel_valid = 1
    if channel_valid == 0:
        raise InputError("Error occurred channel_id is not valid")
        
    # Check to see if authorised user is a member of specified channel.
    authorisation = 0
    for channel in data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                authorisation = 1
    if authorisation == 0:
        raise AccessError("Error occurred authorised user is not a member of channel with channel_id")
    
    # Main functionality of channel_details_v1
    # Must append current member to channelDetails as well as all listed members.
    channelDetails = {}
    
    # Loop through each channel in data.
    for channel in data['channels']:
        if channel['id'] == channel_id: # Make sure we're on the right channel.
            channelDetails['name'] = channel['name']    
        # Check the all_members section of each channel.
            channelDetails['owner_members'] = []
            channelDetails['all_members'] = []
            for member in channel['owner_members']:
                channelDetails['owner_members'].append({
                    'u_id': member['u_id'],
                    'email': member['email'],
                    'name_first': member['name_first'],
                    'name_last': member['name_last'],
                    'handle_str': member['handle_str'],            
                })
            for member in channel['all_members']:
                channelDetails['all_members'].append({
                    'u_id': member['u_id'],
                    'email': member['email'],
                    'name_first': member['name_first'],
                    'name_last': member['name_last'],
                    'handle_str': member['handle_str'],            
                })
                
    return channelDetails
 
def channel_messages_v1(auth_user_id, channel_id, start):
    """
    Given a Channel with ID channel_id that the authorised user is part of, 
    return up to 50 messages between index "start" and "start + 50". 
    Message with index 0 is the most recent message in the channel. 

    Arguments:
        auth_user_id (int)    - Users id
        channel_id (int)    - Channel id
        start (int)    - Start of the messages

    Exceptions:
        InputError - Occurs when the channel ID is not a valid channel or start is 
                    greater than the total number of messages in the channel
        AccessError - Occurs when id is not in data or authorised user is not a 
                    member of channel with channel_id

    Return Value:
        Returns { messages, start, end } on success
    """
    # Check if auth_user_id matches a user in the database.
    user_valid = 0
    for user in data['users']:
        if user['u_id'] == auth_user_id:
            user_valid = 1
    if user_valid == 0:
        raise AccessError("Error occurred auth_user_id is not valid")

    # Check to see if channel_id matches a channel in the database.
    channel_valid = 0
    for channel in data['channels']:
        if channel['id'] == channel_id:
            channel_valid = 1
    if channel_valid == 0:
        raise InputError("Error occurred channel_id is not valid")

    # Check to see if authorised user is a member of specified channel.
    authorisation = 0
    for channel in data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                authorisation = 1
    if authorisation == 0:
        raise AccessError("Error occurred authorised user is not a member of channel with channel_id")

    # Gets a list of all the messages and also the length of the list
    for channel in data['channels']:
        if channel['id'] == channel_id:
            messages = list(channel['messages'])
            num_messages = len(messages)

    # No messages
    if num_messages == 0 and start == 0:
        return {
                'messages': [], 
                'start': start, 
                'end': -1
        }

    # If start is larger than number of items in messages
    # Raise inputError
    if start >= num_messages:
        raise InputError("Error Start value is larger than number of items in messages")
    
    # Loop through messages list, append messages to a list
    end = start + 50
    counter = 0
    messages = []
    
    while counter < 50:
        index = start + counter
        if index >= end or index >= num_messages:
            break

        new_message = {
                'message_id': messages[index].get('message_id'),
                'u_id': messages[index].get('user_id'),
                'message': messages[index].get('message_sent'),
                'time_created': messages[index].get('time_created'),
        }
        messages.append(new_message)
        counter += 1
    
    # If this function has returned the least recent messages in the channel, 
    # returns -1 in "end" to indicate there are no more messages to load after 
    # this return.           
    if counter < 50:
        end = -1

    return {
            'messages': messages, 
            'start': start, 
            'end': end
    }

def channel_messages_v2(token, channel_id, start):
    """
    Given a Channel with ID channel_id that the authorised user is part of, 
    return up to 50 messages between index "start" and "start + 50". 
    Message with index 0 is the most recent message in the channel. 

    Arguments:
        token (str)    - token
        channel_id (int)    - Channel id
        start (int)    - Start of the messages

    Exceptions:
        InputError - Occurs when the channel ID is not a valid channel or start is 
                    greater than the total number of messages in the channel
        AccessError - Occurs when u_id is not in data or authorised user is not a 
                    member of channel with channel_id

    Return Value:
        Returns { messages, start, end } on success
    """

    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description='Error Invalid token')

    # Check to see if channel_id matches a channel in the database.
    channel_valid = 0
    for channel in data['channels']:
        if channel['id'] == channel_id:
            channel_valid = 1
    if channel_valid == 0:
        raise InputError(description="Error occurred channel_id is not valid")
    
    # Get user id from token
    auth_user_id = get_token_user_id(token)

    # Check to see if authorised user is a member of specified channel.
    authorisation = 0
    for channel in data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                authorisation = 1
    if authorisation == 0:
        raise AccessError(description="Error occurred authorised user is not a member of channel with channel_id")

    # Gets a list of all the messages and also the length of the list
    for channel in data['channels']:
        if channel['id'] == channel_id:
            messages = list(channel['messages'])
            num_messages = len(messages)

    # No messages
    if num_messages == 0 and start == 0:
        return {
            'messages': [], 
            'start': start, 
            'end': -1
        }

    # If start is larger than number of items in messages
    # Raise inputError
    if start >= num_messages:
        raise InputError(description="Error Start value is larger than number of items in messages")
    
    # Loop through messages list, append messages to a list
    end = start + 50
    counter = 0
    output = []
    
    while counter < 50:
        index = start + counter
        if index >= end or index >= num_messages:
            break

        new_message = {
            'message_id': messages[index].get('message_id'),
            'u_id': messages[index].get('u_id'),
            'message': messages[index].get('message'),
            'time_created': messages[index].get('time_created'),
        }
        output.append(new_message)
        counter += 1
    
    # If this function has returned the least recent messages in the channel, 
    # returns -1 in "end" to indicate there are no more messages to load after 
    # this return.           
    if counter < 50:
        end = -1

    return {
        'messages': output,
        'start': start,
        'end': end,
    }

# Not required for iteration 1
def channel_leave_v1(auth_user_id, channel_id):
    return {
    }

def channel_join_v1(auth_user_id, channel_id):
    """
    Given a channel_id of a channel that the authorised user can join, adds them to that channel

    Arguments:
        auth_user_id (integer)    - Users id
        channel_id (integer)    - Users set password

    Exceptions:
        InputError  - Occurs when channel_id is not a valid channel
        AccessError  - Occurs when channel_id refers to a channel that is private (when
                        the authorised user is not a global owner)

    Return Value:
        Returns {}
    """
    # Under 6.3 of the spec raise an assesserror if the auth_user_id is invalid
    ids = [data['users'][c]['u_id'] for c in range(len(data['users']))]
    if auth_user_id not in ids:
        raise AccessError('Invalid auth_user_id')

    reuser = {}
    # Loop until u_id match
    for user in data['users']:
        if auth_user_id == user['u_id']:
            # Copy all the user data for easier access
            reuser = {
                'u_id': user['u_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
            }

    # Check if channel_id is in the database
    channel_valid = 0
    data_copy = {}
    for channel in data['channels']:
        if channel['id'] == channel_id:
            channel_valid = 1
            data_copy = {
                'name' : channel['name'],
                'is_public': channel.get('is_public'),
            }
    
    if channel_valid == 0:
        raise InputError("Invalid channel_id")

    if data_copy.get('is_public') == True:
        # Added user to all members for channel
        for channel in data['channels']:
            if channel['id'] == channel_id:
                channel['all_members'].append(reuser)
    else:
        raise AccessError('The channel you are trying to join is private')
    
    return {}

def channel_join_v2(token, channel_id):
    """
    Given a channel_id of a channel that the authorised user can join, adds them to that channel

    Arguments:
        token (string)    - Token
        channel_id (integer)    - Users set password

    Exceptions:
        InputError  - Occurs when channel_id is not a valid channel
        AccessError  - Occurs when channel_id refers to a channel that is private (when
                        the authorised user is not a global owner)

    Return Value:
        Returns {}
    """

    # Check if token is valid using helper
    if check_token_valid(token) == False:
        raise AccessError(description='Invalid token')

    # Get u_id from valid token
    auth_user_id = get_token_user_id(token)

    # Raise an assesserror if the auth_user_id is invalid
    ids = [data['users'][c]['u_id'] for c in range(len(data['users']))]
    if auth_user_id not in ids:
        raise AccessError(description='Invalid auth_user_id')

    reuser = {}
    # Loop until u_id match
    for user in data['users']:
        if auth_user_id == user['u_id']:
            # Copy all the user data for easier access
            reuser = {
                'u_id': user['u_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
            }

    # Check if channel_id is in the database
    channel_valid = 0
    data_copy = {}
    for channel in data['channels']:
        if channel['id'] == channel_id:
            channel_valid = 1
            data_copy = {
                'name' : channel['name'],
                'is_public': channel.get('is_public'),
            }
    
    if channel_valid == 0:
        raise InputError(description="Invalid channel_id")

    if data_copy.get('is_public') == True:
        # Added user to all members for channel
        for channel in data['channels']:
            if channel['id'] == channel_id:
                channel['all_members'].append(reuser)
    else:
        raise AccessError(description='The channel you are trying to join is private')
    
    return {}

# Not required for iteration 1
def channel_addowner_v1(auth_user_id, channel_id, u_id):
    return {
    }

# Not required for iteration 1
def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    return {
    }
