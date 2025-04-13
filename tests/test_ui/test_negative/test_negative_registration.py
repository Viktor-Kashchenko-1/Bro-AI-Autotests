import pytest
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

fake_element = Faker("ru_Ru")

"""нужно использовать для работы многопоточности с случайными параметризациями 
by faker/ ramdom"""
# seed = 1
# fake_element.seed_instance(seed)
# random.seed(seed)


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


@pytest.mark.ui
@pytest.mark.registration_negative


@pytest.mark.trying
@pytest.mark.parametrize("email, name, password", [
    ('user1@example.com', "UserOne", "Password123"),
    ('user2@example.com', "UserTwo", "SecurePass456"),
    ('user3@example.com', "UserThree", "StrongPass789")
])
def test_reg(email, name, password):
    pass