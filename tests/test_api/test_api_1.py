import pytest
import requests
import string
import random


@pytest.fixture
def base_url():
    return "http://95.182.122.183"

@pytest.fixture
def api_url():
    return ""

@pytest.fixture
def correct_response():
    pass