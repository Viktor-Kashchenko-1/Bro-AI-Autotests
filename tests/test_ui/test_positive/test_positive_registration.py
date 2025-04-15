import random
import time
import os
import string
import pytest
from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


"""нужно использовать конкретное число для работы многопоточности с детерминированой параметризацией
без конфликтов, иначе сыпятся Different tests were collected between gwX and gwY ексепшены"""
#To do вынести на глобальный уровень инициализацию сидов обьектов с генераторами случайности
# def get_seeded_local_random_and_faker(seed: int = None):
#     """Создаёт random.Random и Faker с общим случайным сидом"""
#     if seed is None:
#         seed = int(time.time() * 1000) + os.getpid()
#     print(f"[DEBUG] Используемый сид: {seed}")
#
#     rnd = random.Random(seed)
#     fake = Faker()
#     fake.random = rnd
#     return fake    #rnd, fake

#fake_element = get_seeded_local_random_and_faker() # defined int 1,2,12534,etc. for multithreading case
fake_element = Faker()

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
    wait.until(EC.url_to_be(f'{base_url_ui}/login'))
    alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='alert'] div:last-child")))

    assert alert.get_attribute('textContent') == success_alert_message # времянка вместо 'Вы успешно зарегистрировались'

    # to do 'Пользователь с таким email уже зарегистрирован в другом тeсте'
    # to do 'Что-то пошло не так. Пожалуйста, попробуйте позже' if are places


#2-3 test
@pytest.mark.multi_core_fail
@pytest.mark.xfail
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.registration_positive
def test_registration_min_and_max_email(browser, faker_data, base_url_ui, wait, success_alert_message,
                                        random_min_and_max_email):
    browser.get(base_url_ui + '/sign_up')
    wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(faker_data['name'])
    browser.find_element(By.ID, 'pass1').send_keys(faker_data['password'])
    browser.find_element(By.ID, 'pass2').send_keys(faker_data['password'])
    browser.find_element(By.ID, 'email').send_keys(random_min_and_max_email)

    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    wait.until(EC.url_to_be(f'{base_url_ui}/sign_up'))  # как поправят будет /логин

    alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"[role='alert'] div:last-child")))
    text = alert.get_attribute('textContent')
    assert text == success_alert_message


#4 test
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.registration_positive
# @pytest.mark.parametrize("email, name, password", [
#     ('test_sadlik4@mail.com', "Sadlik13", "Qwerty123"),
#     ('test_sadlik24@mail.com', "Sadlik110", "Qqqqwerty123"),
#     ('test_sadlik222@mail.com', "Sadlk123", "Qqwert123")
#])
def test_positive_registration_minimum_length_passwords(browser, base_url_ui, wait, faker_data, success_alert_message):
    browser.get(base_url_ui+'/sign_up')
    wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(faker_data['name'])
    browser.find_element(By.ID, 'pass1').send_keys(faker_data['password'])
    browser.find_element(By.ID, 'pass2').send_keys(faker_data['password'])
    browser.find_element(By.ID, 'email').send_keys(faker_data['email'])

    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    wait.until(EC.url_to_be(f'{base_url_ui}/log_in'))

    alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='alert'] div:last-child")))
    assert alert.get_attribute('textContent') == success_alert_message #времянка вместо 'Пользователь с таким email уже зарегистрирован'


#5 test
@pytest.mark.multi_core_fail
@pytest.mark.ui
@pytest.mark.positive
@pytest.mark.registration_positive
@pytest.mark.parametrize('password',[  # to do по хорошему заменить лямбды на ленивые фикстуры или
    # сидирование генераторов + генерация постоянных данных
    lambda: fake_element.password(length=50),
    lambda: fake_element.password(length=50, lower_case= True, upper_case= False, special_chars= False),
    lambda: fake_element.password(length=50, lower_case= False, upper_case= True, special_chars= False),
    lambda: fake_element.password(length=50, lower_case= False, upper_case= False, special_chars= True),
    lambda: fake_element.password(length=50, digits=True , upper_case=False, special_chars=False, lower_case= False)
])
def test_positive_registration_maximum_length_passwords(browser, base_url_ui, password, wait, faker_data,
                                                           fail_alert_message, success_alert_message):
    browser.get(base_url_ui+'/sign_up')
    wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(faker_data['name'])
    current_password = password()
    browser.find_element(By.ID, 'pass1').send_keys(current_password)
    browser.find_element(By.ID, 'pass2').send_keys(current_password)
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
@pytest.mark.multi_core_fail
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


# @pytest.mark.ui
# @pytest.mark.positive
# @pytest.mark.reg_data
# def test_get_registered_user_data(registered_user_ui):
#     print(registered_user_data)

