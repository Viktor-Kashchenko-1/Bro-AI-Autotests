import pytest
from faker import Faker
import requests

fake = Faker('ru_RU')

@pytest.fixture()
def faker_data():
    return {
        'name': fake.first_name(),
        'password': fake.password(8, False, True),
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
