# Assumptions

## General
* No assumptions made

## auth

### auth_login
* No assumptions made

### auth_register
* User ids start at index 1
* New user id is the lowest integer value not in use that is greater than or equal to 1

### auth_logout
* It is assumed that the false case is never returned as any invalid tokens will raise an AccessError

## channels
* In testing Auth_register is working correctly to store user with id 1

### channels_listall
* In testing Channels_create is working correctly

### channels_create
* Input error raised if is_public was not of type bool

### channels_list
* In testing channels_create and channel_join are working correctly

## channel
* In testing Auth_register is working correctly to store user with id 1

### channel_join
* No assumptions made

### channel_details
* In testing, channels_create and channel_join are working correctly

### dm_leave
* If owner leaves the DM, the owner still remain as the owner (creator of the DM), 
  just not a member of the DM anymore and cannot use the DM or access it unless they rejoin. 

### channel_leave
* If a channel owner leaves the channel, they will no longer be an owner of the channel, unless they are the only owner where they will still be an owner of the channel.

## dm
* DM name is set when dm_invite is used and does not change when members are added
or removed

## Messages

### message_share_v1
* Assume that the optional message is also less than 1000 characters
* Raise input error is og_message_id is invalid
* Raise an AccessError if the user_id is not in the same channel/dm as og_message_id