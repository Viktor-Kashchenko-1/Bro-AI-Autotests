import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


@pytest.fixture
def faker_data():
    fake= Faker("ru_Ru")
    return {
        'email': fake.ascii_free_email(),
        'name': fake.first_name(),
        'password': fake.password(length=8, upper_case=True, lower_case=False)
    }


@pytest.fixture
def fail_alert_message():
    return 'Что-то пошло не так. Пожалуйста, попробуйте позже'

#
@pytest.fixture
def requirement_field_error():
    return 'Это поле обязательно'


@pytest.fixture
def success_alert_message():
    return 'Вы успешно зарегистрировались// или что то такое'


@pytest.fixture(params=["Chrome"])
def browser(request, base_url_ui):  #base_url_ui extra
    if request.param == "Chrome":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    elif request.param == "Firefox":
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.set_window_size(1100, 700)
    yield driver
    driver.quit()


@pytest.fixture
def base_url_ui():
    return 'http://95.182.122.183:3000'


@pytest.fixture
def wait(browser):
    return WebDriverWait(browser, 10)


# *существующие* почты
@pytest.fixture(params=[
    {'email': 'test_sadlik1@mail.com',
    'password': 'Qwerty123',
    'name': 'Sadlik10'},
    {'email': 'test_sadlik2@mail.com',
    'password': '123Qwerty',
    'name': 'Sadlik27'},
    {'email': 'test_sadlik3@mail.com',
    'password': 'qWerty123',
    'name': 'Sadlik30'}
])
def login_data(request):
    return request.param


# Варианты валидных доменов
@pytest.fixture(params=[
    ("США", "gmail.com"),
    ("США", "yahoo.com"),
    ("США", "outlook.com"),
    ("США", "hotmail.com"),
    ("США", "aol.com"),
    ("США", "icloud.com"),
    ("Россия", "mail.ru"),
    ("Россия", "yandex.ru"),
    ("Россия", "bk.ru"),
    ("Россия", "inbox.ru"),
    ("Россия", "list.ru"),
    ("Россия", "rambler.ru"),
    ("Украина", "ukr.net"),
    ("Украина", "i.ua"),
    ("Украина", "meta.ua"),
    ("Украина", "email.ua"),
    ("Украина", "bigmir.net"),
    ("Украина", "gmail.com"),
    ("Украина", "yahoo.com"),
    ("Украина", "outlook.com"),
])
def e_domain(request):
    return request.param


@pytest.fixture
def registered_user_data(browser, base_url_ui, faker_data, wait, success_alert_message, fail_alert_message):
    browser.get(f'{base_url_ui}/sign_up')
    username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    username_field.send_keys(faker_data['name'])
    browser.find_element(By.ID, "pass1").send_keys(faker_data['password'])
    browser.find_element(By.ID, 'pass2').send_keys(faker_data['password'])
    browser.find_element(By.ID, "email").send_keys(faker_data['email'])
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()

    alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='alert'] div:last-child")))
    assert alert.get_attribute('textContent') == success_alert_message

    return faker_data


@pytest.fixture(params=[
    {'email': '',
    'pass1': '123Qwerty',
    'pass2': '123Qwerty',
    'name': 'Sadlik30'},
    {'email': 'test_sadlik3@mail.com',
    'pass1': '',
    'pass2': '123Qwerty',
    'name': 'Sadlik30'},
    {'email': 'test_sadlik2@mail.com',
    'pass1': '123Qwerty',
    'pass2': '',
    'name': 'Sadlik27'},
    {'email': 'test_sadlik3@mail.com',
     'pass1': '123Qwerty',
     'pass2': '123Qwerty',
     'name': ''}
])
def user_data_with_1_empty(request):
    return request.param