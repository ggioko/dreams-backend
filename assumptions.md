# Assumptions

## General
* No assumptions made

## auth

### auth_login
* No assumptions made

### auth_register
* User ids start at index 1
* New user id is the lowest integer value not in use that is greater than or equal to 1

## channels
* In testing Auth_register is working correctly to store user with id 1

### channels_listall
* In testing Channels_create is working correctly

### channels_create
* Input error raised if is_public was not of type bool

### channels_list
* In testing channels_create and channel_join are working correctly

### channel_join
* No assumptions made
