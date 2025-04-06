import string
import pytest
import requests
import random

@pytest.mark.user_registration
def test_user_registration(faker_data, api_url):
    user_data = {
        'username': faker_data['name'],
        'password': faker_data['password'],
        'email': faker_data['mail']
    }
    response = requests.post(f'{api_url}/users/', json='user_data')

    assert response.status_code == 201
    assert 'id' in response.json()