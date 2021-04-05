# Test commented out due to utilisng helper function. Could not be used 


import pytest
# import requests
# import json
# from src import config
# from src.error import AccessError, InputError

# from src.helper import no_check_dreams_change_permission


def test_userpermission_change():
    """
    Test to check if admin/userpermission/change/v1 works by passing in valid information.
    """
    pass

#     r = requests.delete(config.url + 'clear/v1')
#     r = requests.post(config.url + 'auth/register/v2', json={'email':'madladadmin@gmail.com',\
#     'password':'123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
#     rego_1 = r.json()
#     r = requests.post(config.url + 'auth/register/v2', json={'email':'peasantuser@gmail.com',\
#     'password':'diffpassword!', 'name_first':'Everest', 'name_last':'Hayden'})
#     rego_2 = r.json()
#     # print(data)
    
#     # Tests with a non-owner requesting a permission change
#     test_1 = requests.post(config.url + 'admin/userpermission/change/v1', json={ \
#     'token': rego_1['token'], 'u_id':rego_2['auth_user_id'], 'permission_id': 1})
#     assert test_1.status_code == AccessError().code
    
#     print("auth_user_id = " + str(rego_1['auth_user_id']))

#     # Call helper function to make user1 dreams owner
#     # Not a black box test, but no inbuilt functions allow for this to happen, so data
#     # must be modified directly
#     # If in a production system, the first owner would manually set thir permissions_id
#     no_check_dreams_change_permission(rego_1['auth_user_id'], 1)

#     # Tests a non-valid user being invited
#     test_2 = requests.post(config.url + 'admin/userpermission/change/v1', json={ \
#     'token': rego_1['token'], 'u_id':rego_2['auth_user_id'] + 1, 'permission_id': 1})
#     assert test_2.status_code == InputError().code

#     # Tests an invalid permission applied to rego_2
#     test_3 = requests.post(config.url + 'admin/userpermission/change/v1', json={ \
#     'token': rego_1['token'], 'u_id':rego_2['auth_user_id'], 'permission_id': 100})
#     assert test_3.status_code == InputError().code

#     # Tests valid request
#     test_4 = requests.post(config.url + 'admin/userpermission/change/v1', json={ \
#     'token': rego_1['token'], 'u_id':rego_2['auth_user_id'], 'permission_id': 1})
#     assert test_4.status_code == 200