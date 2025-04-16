import pytest
from faker import Faker
import requests

fake = Faker('ru_RU')

@pytest.fixture()
def faker_data():
    return {
        'name': fake.first_name(),
        'password': fake.password(14),
        'email': fake.ascii_free_email()
    }


@pytest.fixture
def base_url():
    return 'http://95.182.122.183'


@pytest.fixture
def api_url(base_url):
    return f'{base_url}:8000/api/v1'


@pytest.fixture
def correct_response():
    pass

@pytest.fixture
def registered_user_data(api_url, faker_data):
    user_data = {
        'username': faker_data['name'],
        'password': faker_data['password'],
        'email': faker_data['email']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 201
    return user_data


@pytest.fixture
def auth_token(api_url, registered_user_data):
    auth_data ={
        'email': registered_user_data['email'],
        'password': registered_user_data['password']
    }
    response = requests.post(f'{api_url}/jwt/create/', json=auth_data)
    assert response.status_code == 200
    return response.json()['access']

@pytest.fixture
def auth_header(auth_token):
    return {'Autorization': f'Bearer {auth_token}'}


@pytest.fixture()
def blank_field_error():
    return ['This field may not be blank.']


@pytest.fixture()
def required_field_error():
    return 'This field is required.'


@pytest.fixture()
def access_denied():
    return 'Authentication credentials were not provided.'


@pytest.fixture()
def internal_error_text():
    return "Internal Server Error"