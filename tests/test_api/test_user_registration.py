import string
import pytest
import requests
import random


def value_exceeded(request):
    return [f'Ensure this field has no more than {request} characters.']


@pytest.mark.api
@pytest.mark.positive
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


@pytest.mark.api
@pytest.mark.positive
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

@pytest.mark.api
@pytest.mark.positive
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

@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_username_exceed_length(faker_data, api_url):
    username_length = 'b' * 256
    user_data = {
        'username': username_length,
        'email': faker_data['email'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 400
    assert response.json()['username'] == value_exceeded(255)

@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_username_blank(faker_data, api_url, blank_field):
    username = ''
    user_data = {
        'username': username,
        'email': faker_data['email'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 400
    assert response.json()['username'] == blank_field
    # to do может имеет смысл вынести ['This field may not be blank.'] в фикстуру и тд.


@pytest.mark.api
@pytest.mark.positive
@pytest.mark.parametrize('min_emails',['@a.сс','@bb.с', '@bb.сc', '@b.фы', '@фы.фы'])
#без фейка срабатывает единожды =( далее это уже существует
# далее по мнению аи валидные кейсы, система не ест  "1@1.1", 'a@io', '_@_.io', '-@-.ai', '@@@.@', '" "@x.y'
@pytest.mark.user_registration
def test_email_min_length(faker_data, api_url, min_emails):
    user_data = {
        'username': faker_data['name'],
        'email': 'с' + min_emails, # 'b' костыль на изменение первого символа почты для оригинальности регистрации
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['username'] == user_data['username']


@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
def test_email_max_length(faker_data, api_url):
    max_len_mail = (''.join(random.choices(string.ascii_lowercase, k=38)) + '@example.com')
    user_data = {
        'username': faker_data['name'],
        'email': max_len_mail,
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    print()
    print(response.json())
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['username'] == user_data['username']

@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
@pytest.mark.xfail(reason='проверка коммента xfail')
def test_email_exceed_length(faker_data, api_url):
    max_len_mail = (''.join(random.choices(string.ascii_lowercase, k=39)) + '@example.com')
    user_data = {
        'username': faker_data['name'],
        'email': max_len_mail,
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 400
    assert response.json()['email'] == value_exceeded(50)

@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_email_exceed_length(faker_data, api_url, blank_field):
    blank_mail = ''
    user_data = {
        'username': faker_data['name'],
        'email': blank_mail,
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 400
    assert response.json()['email'] == blank_field