import string
import pytest
import requests
import random
from faker import Faker

""" to do проставить каждому тесту степень важности--  
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.regression
и другое
"""

# регистрация со всеми заполненными валидными полями
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.regression
def test_user_registration_all_fields(faker_data, api_url):
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


# регистрация с существующими учетными данными
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.regression
def test_email_duplicate(api_url, registered_user_data, faker_data):
    user_data = {
        'email': registered_user_data['email'],
        'username': faker_data['name'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 400
    assert 'user with this email already exists.' in response.json()['email'][0], (
        'should be: "user with this email already exists"')


#-------------------------------------------------------------------------------------------------------------------

"""USERNAME BLOCK"""

#-------------------------------------------------------------------------------------------------------------------
# регистрация с минимальной длинной  юзернейма
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
@pytest.mark.smoke
@pytest.mark.regression
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

# регистрация с максимальной длинной  юзернейма
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


def value_exceeded(request):
    return [f'Ensure this field has no more than {request} characters.']


# регистрация с превышающей на 1 символ длинной юзернейма
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_username_exceeds_length(faker_data, api_url):
    username_length = 'b' * 256
    user_data = {
        'username': username_length,
        'email': faker_data['email'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 400
    assert response.json()['username'] == value_exceeded(255)



# регистрация с пустым юзернеймом
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_username_blank(faker_data, api_url, blank_field_error):
    username = ''
    user_data = {
        'username': username,
        'email': faker_data['email'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 400
    assert response.json()['username'] == blank_field_error
    # to do может имеет смысл вынести ['This field may not be blank.'] в фикстуру и тд.


# тест с регистрацией имени как последовательность пробелов
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_username_are_spaces(faker_data, api_url):
    spaces_name = ' ' * 5
    user_data = {
        'username': spaces_name,
        'email': faker_data['email'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 400
    assert 'username' in response.json()
    assert 'This field may not be blank.' in response.json()['username']


# регистрация с пробелом в начале, середине, конце имени
@pytest.mark.xfail(reason= 'возможен багфикс с изменением 500 статус кода на 400')
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
@pytest.mark.parametrize("name", [" sample", "При  мер", "sample "])
def test_in_username_are_spaces(api_url, faker_data, name, internal_error_text):
    user_data = {
        'username': name,
        'email': faker_data['email'],
        'password': faker_data['password']
    }
    response = requests.post(api_url, None, user_data)
    assert response.status_code == 500
    assert response.reason == internal_error_text



# регистрация с невалидным ключом usernam
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_user_registration_key_usernam(api_url, faker_data, required_field_error):
    user_data = {
        'usernam': faker_data['name'],
        'password': faker_data['password'],
        'email': faker_data['email']
    }
    response = requests.post(url=f'{api_url}/users/')
    assert response.status_code == 400
    for key in ['password', 'email', 'username']:
        assert response.json()[key][0] == required_field_error

#-------------------------------------------------------------------------------------------------------------------

"""EMAIL BLOCK"""

#-------------------------------------------------------------------------------------------------------------------
# регистрация с email в верхнем регистре
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.regression
def test_email_uppercase(api_url, faker_data):
    upper_case_email = faker_data['email'].upper()
    user_data = {
        'email': upper_case_email,
        'username': faker_data['name'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 201
    assert response.json()['email'].lower() == upper_case_email.lower(), (
        'email into request & into response should be comparison in the same case')


def generate_email_with_special_chars():
    spec_chars = ".!#$%^&_'/*-+`~{}?/|="
    user_part = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    for _ in range(random.randint(2,5)):
        new_char = random.choice(spec_chars)
        if  new_char == '.' == user_part[-1]:
            continue
        user_part += new_char

    if user_part[-1] == '.':
        user_part += 'a'
    return f'{user_part}@example.com'

'''to do узнавать на конкретном проекте валидны ли спец символы в почте, в каких местах валидны т.д.'''
# регистрация email со спец символами. Они имеют специфическое поведение, проверяем n_repeats раз для достоверности
n_repeats = 2
@pytest.mark.xfail(reason="может фейлится при специфических случаях генерации почты")
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.regression
@pytest.mark.parametrize("_, counter", [(1, i) for i in range(n_repeats)]) #experiment with "_"parameter in parametrizing
def test_email_with_special_chars(_, counter, api_url, faker_data):
    special_ch_email = generate_email_with_special_chars()
    user_data = {
        'email': special_ch_email,
        'username': faker_data['name'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    #print(response.json())
    assert response.status_code == 201
    assert response.json()['email'].lower() == special_ch_email.lower()


def generate_min_email():
    local_part = random.choice(string.ascii_lowercase)
    domain = random.choice(string.ascii_lowercase)
    tld = ''.join(random.sample(string.ascii_lowercase, 2))
    return f'{local_part}@{domain}.{tld}'

# регистрация с минимальной допустимой длинной почты
@pytest.mark.skip(reason='Запускать в крайнем случаи. К-во тест данных ограничено.')
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.smoke
@pytest.mark.user_registration
def test_email_min_length(faker_data, api_url):
    email = generate_min_email()
    user_data = {
        'username': faker_data['name'],
        'email': email,
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['email'] == email


# регистрация с максимальной длинной почты 50 символов
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
    assert response.json()['email'] == user_data['email']
    assert 'id' in response.json()


# регистрация почты с присутствием пробелов на краях (начале, конце), почта обрежется и пройдет регистрацию
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
@pytest.mark.parametrize("spaces_mail_index", [1, 2])
def test_in_mail_are_corner_spaces(faker_data, api_url, spaces_mail_index, internal_error_text):
    if spaces_mail_index == 1:
        spaced_email = f'  {faker_data['email']}'
    elif  spaces_mail_index == 2:
        spaced_email = f'{faker_data['email']}   '
    user_data = {
        'username': faker_data['name'],
        'email': spaced_email,
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    print()
    print(response.json())
    assert response.status_code == 201
    assert internal_error_text in response.json()['email']



# регистрация с превышающей на 1 символ длинной почты
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
@pytest.mark.xfail(reason='проверка коммента xfail')
def test_email_exceeds_length(faker_data, api_url):
    max_len_mail = (''.join(random.choices(string.ascii_lowercase, k=39)) + '@example.com')
    user_data = {
        'username': faker_data['name'],
        'email': max_len_mail,
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 400
    assert response.json()['email'] == value_exceeded(50)


# регистрация с короткой невалидной почтой
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_email_short_invalid(faker_data, api_url):
    short_mail = 'x@y.z'
    user_data = {
        'username': faker_data['name'],
        'email': short_mail,
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 400
    assert response.json()['email'][0] == 'Enter a valid email address.' #etc.


# регистрация с пустой почтой
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_email_blank(faker_data, api_url,blank_field_error):
    empty_mail = ''
    user_data = {
        'email': empty_mail,
        'username': faker_data['name'],
        'password': faker_data['password']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 400
    assert response.json()['email'][0] == blank_field_error[0] #проверил как работает ассерт через индекс списка в ответе


# регистрация почты с пропущенной доменной частью до точки
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_email_first_domain_blank(faker_data, api_url):
    invalid_email = 'lukjan1999@.com'
    user_data = {
        'email': invalid_email,
        'username': faker_data['name'],
        'password': faker_data['password']
    }
    response = requests.post(url= api_url + '/users/', json= user_data)
    assert response.status_code == 400
    assert 'Enter a valid email address.' in response.json()['email'][0]


# регистрация почты с пропущенной пользовательской частью
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_email_user_block_blank(faker_data, api_url):
    invalid_email = '@gmail.com'
    user_data = {
        'email': invalid_email,
        'username': faker_data['name'],
        'password': faker_data['password']
    }
    response = requests.post(url= api_url + '/users/', json= user_data)
    assert response.status_code == 400
    assert 'Enter a valid email address.' in response.json()['email'][0]


# регистрация почты с пропущенной доменной частью после точки
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_email_second_domain_blank(faker_data, api_url):
    invalid_email = 'lukjan1999@gmail.'
    user_data = {
        'email': invalid_email,
        'username': faker_data['name'],
        'password': faker_data['password']
    }
    response = requests.post(url= api_url + '/users/', json= user_data)
    assert response.status_code == 400
    assert 'Enter a valid email address.' in response.json()['email'][0]


# регистрация почты без @
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_email_missing_at_symbol_dog(faker_data, api_url):
    invalid_email = 'Template_invalid.com'
    user_data = {
        'email': invalid_email,
        'username': faker_data['name'],
        'password': faker_data['password']
    }
    response = requests.post(url= api_url + '/users/', json= user_data)
    assert response.status_code == 400
    assert 'Enter a valid email address.' in response.json()['email'][0]


# регистрация почты без точки
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_email_missing_at_symbol_dot(faker_data, api_url):
    invalid_email = 'Template@invalid_com'
    user_data = {
        'email': invalid_email,
        'username': faker_data['name'],
        'password': faker_data['password']
    }
    response = requests.post(url= api_url + '/users/', json= user_data)
    assert response.status_code == 400
    assert 'Enter a valid email address.' in response.json()['email'][0]


# регистрация почты с пробелами внутри почты
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_into_email_are_spaces(faker_data, api_url):
    invalid_email = list(faker_data['email'])
    invalid_email.insert(2, ' ')
    spaced_email = ''.join(invalid_email)

    user_data = {
        'email': spaced_email,
        'username': faker_data['name'],
        'password': faker_data['password']
    }
    response = requests.post(url= api_url + '/users/', json= user_data)
    assert response.status_code == 400
    assert response.json()['email'] == ['Enter a valid email address.']


# регистрация с невалидным ключом emal
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_user_registration_key_passwor(api_url, faker_data, required_field_error):
    user_data = {
        'username': faker_data['name'],
        'password': faker_data['password'],
        'emal': faker_data['email']
    }
    response = requests.post(url=f'{api_url}/users/')
    assert response.status_code == 400
    for key in ['password', 'email', 'username']:
        assert response.json()[key][0] == required_field_error
#-------------------------------------------------------------------------------------------------------------------

"""PASSWORD BLOCK"""

#-------------------------------------------------------------------------------------------------------------------
# регистрация с минимальной длинной пароля. (ограничения фреймворка- валидные от 8 символов)
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
def test_password_minimal_length(api_url, faker_data):
    minimal_pass_length = Faker('ru_RU')
    user_data = {
        'password': minimal_pass_length.password(length=8),
        'username': faker_data['name'],
        'email': faker_data['email']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 201
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']


# регистрация с минимальным набором из требований валидности пароля. (ограничения фреймворка- валидный пароль
# от 8 символов, из них: (надо ресерчить требования, исходя из опыта будет 1 прописная, 1 спецсимвол,
# 1 цифра, 1 заглавная)
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
def test_password_minimal_required(api_url, faker_data):
    minimal_pass_length = 'Aabcde1!'
    user_data = {
        'password': minimal_pass_length,
        'username': faker_data['name'],
        'email': faker_data['email']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 201
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']
    assert 'id' in response.json()



# регистрация с длинным паролем, явного ограничения нет.
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
def test_long_password(api_url, faker_data):
    minimal_pass_length = Faker('ru_RU')
    user_data = {
        'password': minimal_pass_length.password(length=60),
        'username': faker_data['name'],
        'email': faker_data['email']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 201
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']
    assert 'id' in response.json()

# регистрация с паролем только из букв нижнего регистра, латиница (to do дополнить кириллицей, если валидно).
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
def test_password_only_lower_case(api_url, faker_data):
    pass_lower_case = Faker('ru_RU')
    user_data = {
        'password': pass_lower_case.password(length=30, special_chars= False, upper_case= False,lower_case= True, digits= False),
        'username': faker_data['name'],
        'email': faker_data['email']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 201
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']
    assert 'id' in response.json()


# регистрация с паролем только из букв верхнего регистра, латиница (to do дополнить кириллицей, если валидно).
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
def test_password_only_upper_case(api_url, faker_data):
    pass_upper_case = Faker('ru_RU')
    user_data = {
        'password': pass_upper_case.password(length=30, special_chars= False, upper_case= True,lower_case= False, digits= False),
        'username': faker_data['name'],
        'email': faker_data['email']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 201
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']
    assert 'id' in response.json()

# регистрация с паролем только из спец-символов.
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
def test_password_only_special_chars(api_url, faker_data):
    pass_special_chars = Faker('ru_RU')
    user_data = {
        'password': pass_special_chars.password(length=30, special_chars= True, upper_case= False,lower_case= False, digits= False),
        'username': faker_data['name'],
        'email': faker_data['email']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    assert response.status_code == 201
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']
    assert 'id' in response.json()

# регистрация с пробелом в начале пароля
@pytest.mark.xfail(reason='надо глянуть проходет ли парольпосле создания или баг')
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
def test_in_password_are_spaces(faker_data, api_url, internal_error_text):
    spaced_password = f'   {faker_data['password']}'
    user_data = {
        'username': faker_data['name'],
        'email': faker_data['email'],
        'password': spaced_password
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 201
    assert response.reason == internal_error_text


# регистрация с пробелом в середине пароля
@pytest.mark.xfail(reason='надо глянуть проходет ли парольпосле создания или баг')
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
def test_into_password_are_spaces(faker_data, api_url, internal_error_text):
    password_template = list(faker_data['password'])
    password_template.insert(2, ' ')
    password_template.insert(6, ' ')

    spaced_password = ''.join(password_template)
    user_data = {
        'username': faker_data['name'],
        'email': faker_data['email'],
        'password': spaced_password
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 201
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']
    assert 'id' in response.json()


# регистрация с пробелом в конце пароля
@pytest.mark.xfail(reason='надо глянуть проходет ли парольпосле создания или баг')
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
def test_in_password_are_spaces(faker_data, api_url, internal_error_text):
    spaced_password = f'{faker_data['password']}  '
    user_data = {
        'username': faker_data['name'],
        'email': faker_data['email'],
        'password': spaced_password
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 201
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']
    assert 'id' in response.json()


# регистрация со слишком коротким не валидным паролем (ограничения фреймворка- валидные от 8 символов)
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_password_too_short(api_url, faker_data):
    minimal_pass_length = Faker('ru_RU')
    user_data = {
        'password': minimal_pass_length.password(length=7),
        'username': faker_data['name'],
        'email': faker_data['email']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    print(response.json())
    assert response.status_code == 400
    password_warning = 'This password is too short. It must contain at least 8 characters.'
    assert response.json()['password'][0] == password_warning

# регистрация с пустым паролем
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_password_blank(api_url, faker_data, blank_field_error):
    blank_pass = ''
    user_data = {
        'password': blank_pass,
        'username': faker_data['name'],
        'email': faker_data['email']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 201
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']
    assert 'id' in response.json()


# регистрация с паролем только из цифр.
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_password_only_digits(api_url, faker_data):
    fake = Faker('ru_RU')
    pass_only_digits = fake.password(length=10, special_chars=False, upper_case=False, lower_case=False, digits=True)
    user_data = {
        'password': pass_only_digits,
        'username': faker_data['name'],
        'email': faker_data['email']
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    print(response.json())
    assert response.status_code == 400
    assert response.json()['password'][0] == 'This password is entirely numeric.'


# тест с регистрацией пароля как последовательность пробелов
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_password_are_spaces(faker_data, api_url):
    spaces_password = ' ' * 15
    user_data = {
        'username': faker_data['name'],
        'email': faker_data['email'],
        'password': spaces_password
    }
    response = requests.post(f'{api_url}/users/', json=user_data)

    assert response.status_code == 400
    assert 'password' in response.json()
    assert 'This field may not be blank.' in response.json()['password']


# регистрация с невалидным ключом passwor
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_user_registration_key_passwor(api_url, faker_data, required_field_error):
    user_data = {
        'username': faker_data['name'],
        'passwor': faker_data['password'],
        'email': faker_data['email']
    }
    response = requests.post(url=f'{api_url}/users/')
    assert response.status_code == 400
    for key in ['password', 'email', 'username']:
        assert response.json()[key][0] == required_field_error
#-------------------------------------------------------------------------------------------------------------------

"""Общие тесты без конкретной привязки блока выполнения"""

#-------------------------------------------------------------------------------------------------------------------
# регистрация с отправкой пустых значений
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_all_fields_empty(api_url):
    user_data = {
        'password': '',
        'email': '',
        'username': ''
    }
    response = requests.post(f'{api_url}/users/', json=user_data)
    print(response.json())
    assert response.status_code == 400
    for key in ['password', 'email', 'username']:
        assert response.json()[key][0] == 'This field may not be blank.', "there is no error about empty input of required field"


# регистрация с пустым телом запроса
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_empty_body(api_url, required_field_error):
    user_data = {}
    response = requests.post(f'{api_url}/users/', json=user_data)
    print(response.json())
    assert response.status_code == 400
    for key in ['password', 'email', 'username']:
        assert response.json()[key][0] == required_field_error


# отправка запроса регистрации без тела
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_registration_with_skip_body(api_url, required_field_error):
    response = requests.post(url=f"""{api_url}/users/""")
    assert response.status_code == 400

    """(experiment) json->text and absolute comparison check with assert template """
    assert response.text == '''{"username":["This field is required."],"email":["This field is required."],"password":["This field is required."]}'''



# 1) регистрация с пропущенным ключом юзернейма в запросе
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_registration_skip_username_key(api_url, faker_data, required_field_error):
    user_data = {
        'email': faker_data['email'],
        'password': faker_data['password']
    }
    response = requests.post(json=user_data, url= api_url+'/users/')
    print()
    print(response.json())
    assert response.status_code == 400
    assert response.json()['username'][0] == required_field_error


# 2) регистрация с пропущенным ключом пароля в запросе
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_registration_skip_email_key(api_url, faker_data, required_field_error):
    user_data = {
        'password': faker_data['password'],
        'username': faker_data['name']
    }
    response = requests.post(api_url+'/users/', json=user_data)
    print()
    print(response.json())
    assert response.status_code == 400
    assert response.json()['email'][0] == required_field_error


# 3) регистрация с пропущенным ключом почты в запросе
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_registration_skip_email_key(api_url, faker_data, required_field_error):
    user_data = {
        'email': faker_data['email'],
        'username': faker_data['name']
    }
    response = requests.post(api_url+'/users/', json=user_data)
    print()
    print(response.json())
    assert response.status_code == 400
    assert response.json()['password'][0] == required_field_error


# 4) ошибочный метод запроса
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.user_registration
def test_registration_wrong_rest_method(faker_data, api_url, access_denied):
    user_data = {
        'username': faker_data['name'],
        'email': faker_data['email'],
        'password': faker_data['password']
    }
    response = requests.put(f'{api_url}/users/', json=user_data)
    print()
    print(response.json())
    assert response.status_code == 401
    assert 'detail' in response.json()
    assert access_denied in response.json()['detail']

"""To Do поробовать как на уроке сделать с хедером что жейсон шлем"""
# отправка запроса регистрации c данными текстом вместо json/словаря в теле
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
@pytest.mark.smoke
#@pytest.mark.High
@pytest.mark.regression
def test_user_registration_all_fields(faker_data, api_url):
    user_data_text = '''{
   'username': faker_data['name'],
   'password': faker_data['password'],
   'email': faker_data['email']
}'''
    headers = {'Content-Type': 'application/json'}

    response = requests.post(f'{api_url}/users/', user_data_text, headers=headers)
    assert response.status_code == 400
    assert response.json() == {'non_field_errors': ['Invalid data. Expected a dictionary, but got str.']}


# отправка невалидного json где пропущена запятая
@pytest.mark.api
@pytest.mark.positive
@pytest.mark.user_registration
@pytest.mark.regression
def test_user_registration_all_fields(faker_data, api_url):
    invalid_data_json = '''{
   'username': faker_data['name']
   'password': faker_data['password'],
   'email': faker_data['email']
}'''
    headers = {"Content-Type": "application/json"}

    response = requests.post(f'{api_url}/users/', invalid_data_json, headers=headers)
    assert response.status_code == 400
    assert 'detail' in response.json()
    assert 'JSON parse error' in response.json()['detail']