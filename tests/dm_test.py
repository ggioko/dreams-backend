import pytest
from src.error import InputError, AccessError

# Testing when an invalid token is used
# expected AccessError
def test_dm_details_invalid_token():
    

# Testing when an invalid DM ID is used
# expected InputError
def test_dm_details_invalid_dm_id():

# Testing when an authorised id is not a member of DM
# expected AcessError
def test_dm_details_invalid_authorised_member():