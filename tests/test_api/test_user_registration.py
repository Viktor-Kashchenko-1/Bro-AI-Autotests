import string
import pytest
import requests
import random

@pytest.mark.user_registration
def test_user_registration(faker_data, api_url):
    user_data = {
        'username': faker_data['name'],
        'password': faker_data['password'],
        'email': faker_data['email']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    print()
    print(response.json())
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']
    #assert response.json()['password'] == user_data['password']

@pytest.mark.user_registration
def test_username_min_length(faker_data, api_url):
    user_data ={
        'username': 'a',
        'email': faker_data['email'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['username'] == user_data['username']

@pytest.mark.user_registration
def test_username_max_length(faker_data, api_url):
    user_data = {
        'username': 'a'* 255,
        'email': faker_data['email'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['username'] == user_data['username']

@pytest.mark.parametrize('min_emails',['a@a.сс','a@bb.с', 'a@bb.сc', 'a@b.фы'])
#без фейка срабатывает единожды =( далее это уже существует
# далее по мнению аи валидные кейсы, система не ест  "1@1.1", 'a@io', '_@_.io', '-@-.ai', '@@@.@', '" "@x.y'
@pytest.mark.user_registration
def test_username_min_length(faker_data, api_url, min_emails):
    user_data = {
        'username': faker_data['name'],
        'email': min_emails,
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    print()
    print(response.json())
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['username'] == user_data['username']