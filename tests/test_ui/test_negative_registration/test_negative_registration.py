import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
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


# @pytest.fixture(params=[
#     {'email': 'test_sadlik1@mail.com',
#     'password': 'Qwerty123',
#     'name': 'Sadlik10'},
#     {'email': 'test_sadlik2@mail.com',
#     'password': '123Qwerty',
#     'name': 'Sadlik27'},
#     {'email': 'test_sadlik3@mail.com',
#     'password': 'qWerty123',
#     'name': 'Sadlik30'}
# ])
# def exist_users_data(request):
#     return request.param

# @pytest.mark.ui
# @pytest.mark.registration_positive
# def test_positive_registration_all_field_entering(browser, base_url_ui, faker_data, wait,
#                                                   fail_alert_message, success_alert_message):
#     browser.get(f'{base_url_ui}/sign_up')
#     username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
#     username_field.send_keys(faker_data['name'])
#     browser.find_element(By.ID, "pass1").send_keys(faker_data['password'])
#     browser.find_element(By.ID, 'pass2').send_keys(faker_data['password'])
#     browser.find_element(By.ID, "email").send_keys(faker_data['email'])
#     browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
#     #wait.until(EC.url_to_be(f'{base_url_ui}/login')) Тo do распечатать когда заработает
#     alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='alert'] div:last-child")))
#     #alert = browser.find_element(By.CSS_SELECTOR, "[role='alert'] div:last-child")
#     assert alert.get_attribute('textContent') == fail_alert_message # времянка вместо 'Вы успешно зарегистрировались'
#
#     #'Пользователь с таким email уже зарегистрирован в другом тасте'
#     #'Что-то пошло не так. Пожалуйста, попробуйте позже'
#
# @pytest.mark.ui
# @pytest.mark.registration_positive
# # @pytest.mark.parametrize("email, name, password", [
# #     ('test_sadlik4@mail.com', "Sadlik13", "Qwerty123"),
# #     ('test_sadlik24@mail.com', "Sadlik110", "Qqqqwerty123"),
# #     ('test_sadlik222@mail.com', "Sadlk123", "Qqwert123")
# #])
# def test_positive_registration_minimum_length_passwords(browser, base_url_ui, wait, faker_data,
#                                                            fail_alert_message, success_alert_message):
#     browser.get(base_url_ui+'/sign_up')
#     wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(faker_data['name'])
#     browser.find_element(By.ID, 'pass1').send_keys(faker_data['password'])
#     browser.find_element(By.ID, 'pass2').send_keys(faker_data['password'])
#     browser.find_element(By.ID, 'email').send_keys(faker_data['email'])
#     #///////////////////////////
#     browser.find_element(By.ID, 'email').clear()
#     browser.find_element(By.ID, 'email').send_keys(faker_data['email'])
#     #///////////////////////////
#     browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
#
#     wait.until(EC.url_to_be(f'{base_url_ui}/sign_up'))
#
#     alert = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='alert'] div:last-child")))
#     assert alert.get_attribute('textContent') == fail_alert_message  #времянка вместо 'Пользователь с таким email уже зарегистрирован'

@pytest.mark.ui
@pytest.mark.registration_negative
def test_negative_all_fields_empty(browser, base_url_ui, wait, requirement_field_error):
    print() # что бы отладочные выводы писались с новой строки
    browser.get(base_url_ui+'/sign_up')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.ui.button.blue'))).click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#email + div")))
    validation_error = browser.find_elements(By.CSS_SELECTOR, "input + div")
    assert validation_error.__len__() == 4
    for element in validation_error:
        assert element.get_attribute("textContent") == requirement_field_error #to do проверить по факту когда починят

@pytest.mark.ui
@pytest.mark.registration_negative
def test_negative_1_field_empty(browser, base_url_ui, wait, requirement_field_error,
                                   user_data_with_1_empty):
    print() # что бы отладочные выводы писались с новой строки
    browser.get(base_url_ui+'/sign_up')
    username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    username_field.send_keys(user_data_with_1_empty['name'])
    browser.find_element(By.ID, "pass1").send_keys(user_data_with_1_empty['pass1'])
    browser.find_element(By.ID, 'pass2').send_keys(user_data_with_1_empty['pass2'])
    browser.find_element(By.ID, "email").send_keys(user_data_with_1_empty['email'])
    browser.find_element(By.CSS_SELECTOR, '.ui.button.blue').click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input + div")))
    validation_errors = browser.find_elements(By.CSS_SELECTOR, "input + div")
    counter = 0
    for element in validation_errors: #именно тут можно просто асерт 1 штуку смотреть
        if  element.get_attribute("textContent") == requirement_field_error:
            counter += 1
    assert counter == 1

# @pytest.mark.parametrize("email, name, password", [
#     ('user1@example.com', "UserOne", "Password123"),
#     ('user2@example.com', "UserTwo", "SecurePass456"),
#     ('user3@example.com', "UserThree", "StrongPass789")
# ])
def test_reg():
    pass