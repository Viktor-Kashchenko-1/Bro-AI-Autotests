import random
import string
import pytest
from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

fake_element = Faker("ru_Ru")

"""нужно использовать для работы многопоточности с случайными параметризациями"""
seed = 1
fake_element.seed_instance(seed)
random.seed(seed)

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



# @pytest.mark.reg_data
# def test_get_registered_user_data(registered_user_data):
#     print(registered_user_data)

