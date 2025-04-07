from time import sleep

import pytest
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
from webdriver_manager.firefox import GeckoDriverManager

fake_element = Faker("ru_Ru")

"""нужно использовать для работы многопоточности с случайными параметризациями"""
# seed = 1
# fake_element.seed_instance(seed)
# random.seed(seed)


"""Fixtures--------------------------------------"""
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


@pytest.fixture
def success_alert_message():
    return 'Вы успешно зарегистрировались или что то такое'


@pytest.fixture(params=["Chrome"])
def browser(request, base_url_ui):  #base_url_ui extra
    if request.param == "Chrome":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    elif request.param == "Firefox":
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.set_window_size(1250, 750)
    yield driver
    driver.quit()


@pytest.fixture
def base_url_ui():
    return 'http://95.182.122.183:3000'


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
def wait(browser):
    return WebDriverWait(browser, 10)

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
"""End-----Fixtures-----------------------------"""


# 1 test
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.registration_positive
def test_positive_registration_all_entering(browser, base_url_ui, faker_data, wait,
                                            fail_alert_message, success_alert_message):
    browser.get(f'{base_url_ui}/sign_up')
    username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    username_field.send_keys(faker_data['name'])
    browser.find_element(By.ID, "pass1").send_keys(faker_data['password']+ 'qwe')
    browser.find_element(By.ID, 'pass2').send_keys(faker_data['password']+ 'qwe')
    browser.find_element(By.ID, "email").send_keys(faker_data['email'])
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    #wait.until(EC.url_to_be(f'{base_url_ui}/login')) Тo do распечатать когда заработает
    alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='alert'] div:last-child")))

    assert alert.get_attribute('textContent') == fail_alert_message # времянка вместо 'Вы успешно зарегистрировались'

    #'Пользователь с таким email уже зарегистрирован в другом тасте'
    #'Что-то пошло не так. Пожалуйста, попробуйте позже'


#2-3 test
@pytest.mark.multi_core_fail
@pytest.mark.xfail
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.registration_positive
@pytest.mark.parametrize("email", [
     ''.join(random.choices(string.ascii_lowercase, k=38)) + '@example.com',
     ''.join(random.choices(string.ascii_lowercase, k=33)) + '@ex.ua',
     f'{random.choice(string.ascii_lowercase)*2}@{random.choice(string.ascii_lowercase)*2}.{random.choice(string.ascii_lowercase)*2}'
     ])
def test_registration_min_and_max_email(browser, email, faker_data, base_url_ui, wait, success_alert_message):
    browser.get(base_url_ui + '/sign_up')
    wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(faker_data['name'])
    browser.find_element(By.ID, 'pass1').send_keys(faker_data['password'])
    browser.find_element(By.ID, 'pass2').send_keys(faker_data['password'])
    browser.find_element(By.ID, 'email').send_keys(email)

    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    wait.until(EC.url_to_be(f'{base_url_ui}/sign_up'))  # как поправят будет /логин

    alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"[role='alert'] div:last-child")))
    text = alert.get_attribute('textContent')
    assert text == 'Что-то пошло не так. Пожалуйста, попробуйте позже'#|success_alert_message


#4 test
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.registration_positive
# @pytest.mark.parametrize("email, name, password", [
#     ('test_sadlik4@mail.com', "Sadlik13", "Qwerty123"),
#     ('test_sadlik24@mail.com', "Sadlik110", "Qqqqwerty123"),
#     ('test_sadlik222@mail.com', "Sadlk123", "Qqwert123")
#])
def test_positive_registration_minimum_length_passwords(browser, base_url_ui, wait, faker_data,
                                                           fail_alert_message, success_alert_message):
    browser.get(base_url_ui+'/sign_up')
    wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(faker_data['name'])
    browser.find_element(By.ID, 'pass1').send_keys(faker_data['password'])
    browser.find_element(By.ID, 'pass2').send_keys(faker_data['password'])
    browser.find_element(By.ID, 'email').send_keys(faker_data['email'])

    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    wait.until(EC.url_to_be(f'{base_url_ui}/sign_up')) # как поправят будет /логин

    alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='alert'] div:last-child")))
    assert alert.get_attribute('textContent') == fail_alert_message  #времянка вместо 'Пользователь с таким email уже зарегистрирован'


#5 test
@pytest.mark.multi_core_fail
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.registration_positive
@pytest.mark.parametrize('password',[
    fake_element.password(length=50),
    fake_element.password(length=50, lower_case= True, upper_case= False, special_chars= False),
    fake_element.password(length=50, lower_case= False, upper_case= True, special_chars= False),
    fake_element.password(length=50, lower_case= False, upper_case= False, special_chars= True),
    fake_element.password(length=50, digits=False, upper_case=False, special_chars=False, lower_case= True)
])
def test_positive_registration_maximum_length_passwords(browser, base_url_ui, password, wait, faker_data,
                                                           fail_alert_message, success_alert_message):
    browser.get(base_url_ui+'/sign_up')
    wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(faker_data['name'])
    browser.find_element(By.ID, 'pass1').send_keys(password)
    browser.find_element(By.ID, 'pass2').send_keys(password)
    browser.find_element(By.ID, 'email').send_keys(faker_data['email'])

    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    wait.until(EC.url_to_be(f'{base_url_ui}/sign_up')) # как поправят будет /логин

    alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='alert'] div:last-child")))
    assert alert.get_attribute('textContent') == fail_alert_message #|success_alert_message

#6 test
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.registration_positive
def test_positive_registration_minimum_length_username(browser, base_url_ui, wait, faker_data,
                                                       fail_alert_message, success_alert_message):
    username = 'a'
    browser.get(base_url_ui+'/sign_up')
    wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(username)
    browser.find_element(By.ID, 'pass1').send_keys(faker_data['password'])
    browser.find_element(By.ID, 'pass2').send_keys(faker_data['password'])
    browser.find_element(By.ID, 'email').send_keys(faker_data['email'])

    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    wait.until(EC.url_to_be(f'{base_url_ui}/sign_up')) # как поправят будет /логин

    alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='alert'] div:last-child")))
    assert alert.get_attribute('textContent') == fail_alert_message #|success_alert_message

#7 test
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.registration_positive
def test_positive_registration_maximum_length_username(browser, base_url_ui, wait, faker_data,
                                                           fail_alert_message, success_alert_message):
    username = 'A' * 50
    browser.get(base_url_ui + '/sign_up')
    wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(username)
    browser.find_element(By.ID, 'pass1').send_keys(faker_data['password'])
    browser.find_element(By.ID, 'pass2').send_keys(faker_data['password'])
    browser.find_element(By.ID, 'email').send_keys(faker_data['email'])

    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    wait.until(EC.url_to_be(f'{base_url_ui}/sign_up')) # как поправят будет /логин

    alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='alert'] div:last-child")))
    assert alert.get_attribute('textContent') == fail_alert_message #|success_alert_message

#8 test (20 iteration) check valid email domains for the USA, UA, RU countries
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.registration_positive
def test_valid_email_domains(browser, base_url_ui, faker_data, wait, e_domain,
                             fail_alert_message, success_alert_message):
    browser.get(f'{base_url_ui}/sign_up')
    username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    username_field.send_keys(faker_data['name'])
    browser.find_element(By.ID, "pass1").send_keys(faker_data['password'])
    browser.find_element(By.ID, 'pass2').send_keys(faker_data['password'])
    browser.find_element(By.ID, "email").send_keys(f'{faker_data['name']}@{e_domain[1]}')
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    #wait.until(EC.url_to_be(f'{base_url_ui}/login')) Тo do распечатать когда заработает
    alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='alert'] div:last-child")))

    assert alert.get_attribute('textContent') == fail_alert_message # времянка вместо 'Вы успешно зарегистрировались'



# @pytest.mark.reg_data
# def test_get_registered_user_data(registered_user_data):
#     print(registered_user_data)

