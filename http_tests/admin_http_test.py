# HTTP tests theoretically written, but not working due to reliance on a helper function.
# The helper function was necessary in this case as there is no inbuilt way to make a new
# owner of dreams without already having an existing owner's token, hence the data has to
# be modified directly. This works (although is not black box) in standard pytest, however
# this data is not passed correctly when run through HTTP.

import pytest
import requests
import json
from src import config
from src.error import AccessError, InputError

#from src.helper import no_check_dreams_change_permission

def test_userpermission_change_exceptions():
    """
    Test exception cases for admin/userpermission/change/v1.
    """

    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'madladadmin@gmail.com',\
    'password':'123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    rego_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'peasantuser@gmail.com',\
    'password':'diffpassword!', 'name_first':'Everest', 'name_last':'Hayden'})
    rego_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'thirduser@gmail.com',\
    'password':'123password!', 'name_first':'John', 'name_last':'Smith'})
    rego_3 = r.json()
    
    # Tests with a non-owner requesting a permission change
    test_1 = requests.post(config.url + 'admin/userpermission/change/v1', json={ \
    'token': rego_2['token'], 'u_id':rego_3['auth_user_id'], 'permission_id': 1})
    assert test_1.status_code == AccessError().code
    
#    # Call helper function to make user1 dreams owner, read comment at top of file for info
#    no_check_dreams_change_permission(rego_1['auth_user_id'], 1)

    # Tests a non-valid user being invited
    test_2 = requests.post(config.url + 'admin/userpermission/change/v1', json={ \
    'token': rego_1['token'], 'u_id':rego_2['auth_user_id'] + 5, 'permission_id': 1})
    assert test_2.status_code == InputError().code
    
    # Tests an invalid permission applied to rego_2
    test_3 = requests.post(config.url + 'admin/userpermission/change/v1', json={ \
    'token': rego_1['token'], 'u_id':rego_2['auth_user_id'], 'permission_id': 100})
    assert test_3.status_code == InputError().code
    
    
def test_userpermission_change():
    """
    Test to check if admin/userpermission/change/v1 works by passing in valid information.
    """   
    
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'madladadmin@gmail.com',\
    'password':'123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    rego_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'peasantuser@gmail.com',\
    'password':'diffpassword!', 'name_first':'Everest', 'name_last':'Hayden'})
    rego_2 = r.json()
    # Tests valid request
    test_4 = requests.post(config.url + 'admin/userpermission/change/v1', json={ \
    'token': rego_1['token'], 'u_id':rego_2['auth_user_id'], 'permission_id': 1})
    assert test_4.status_code == 200
    
def test_user_remove_exceptions():
    """
    Test exception cases for admin/user/remove/v1
    """   
    
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'madladadmin@gmail.com',\
    'password':'123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    rego_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'peasantuser@gmail.com',\
    'password':'diffpassword!', 'name_first':'Everest', 'name_last':'Hayden'})
    rego_2 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'thirduser@gmail.com',\
    'password':'123password!', 'name_first':'John', 'name_last':'Smith'})
    rego_3 = r.json()
    
    # Invalid token of user calling function
    test = requests.delete(config.url + 'admin/user/remove/v1', json={ \
    'token': 'invalid_token', 'u_id': rego_2['auth_user_id']})
    assert test.status_code == AccessError().code
    
    # Invalid u_id of user getting removed
    test = requests.delete(config.url + 'admin/user/remove/v1', json={ \
    'token': rego_1['token'], 'u_id': rego_2['auth_user_id']+5})   
    assert test.status_code == InputError().code
    
    # User calling the function is the only Dreams owner
    test = requests.delete(config.url + 'admin/user/remove/v1', json={ \
    'token': rego_1['token'], 'u_id': rego_1['auth_user_id']})
    assert test.status_code == InputError().code
    
    # User calling the function is not a Dreams owner
    test = requests.delete(config.url + 'admin/user/remove/v1', json={ \
    'token': rego_2['token'], 'u_id': rego_3['auth_user_id']})
    assert test.status_code == AccessError().code


def test_user_remove():
    """
    Test to check if admin/user/remove/v1 works by passing in valid information.
    """   
    
    requests.delete(config.url + 'clear/v1')
    r = requests.post(config.url + 'auth/register/v2', json={'email':'madladadmin@gmail.com',\
    'password':'123abc!@#', 'name_first':'Hayden', 'name_last':'Everest'})
    rego_1 = r.json()
    r = requests.post(config.url + 'auth/register/v2', json={'email':'peasantuser@gmail.com',\
    'password':'diffpassword!', 'name_first':'Everest', 'name_last':'Hayden'})
    rego_2 = r.json()
    
    # User calling the function is the only Dreams owner
    test = requests.delete(config.url + 'admin/user/remove/v1', json={ \
    'token': rego_1['token'], 'u_id': rego_2['auth_user_id']})
    assert test.status_code == 200