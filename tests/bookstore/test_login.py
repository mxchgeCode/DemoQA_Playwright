import time

from locators.bookstore.login_locators import LoginLocators


def test_invalid_login(login_page):
    login_page.login("wrong_user", "wrong_password")
    error = login_page.get_error_message()
    assert (
            error == "Invalid username or password!"
    ), f"Expected error message, got: {error}"


def test_blank_login(login_page):
    login_page.login("", "")

    # Нажать кнопку входа уже делает метод login при клике без заполнения полей

    # Проверяем поле UserName на наличие класса is-invalid
    username_input = login_page.locator(LoginLocators.USERNAME_INPUT)
    username_class = username_input.get_attribute("class")
    assert (
            "is-invalid" in username_class
    ), "UserName input should have is-invalid class for blank"

    # Проверяем поле Password на наличие класса is-invalid
    password_input = login_page.locator(LoginLocators.PASSWORD_INPUT)
    password_class = password_input.get_attribute("class")
    assert (
            "is-invalid" in password_class
    ), "Password input should have is-invalid class for blank"


def test_new_user_register_empty_fields(login_page):
    login_page.click_new_user()
    assert login_page.get_header_text() == "Register"

    login_page.click_register_button()
    assert login_page.is_field_invalid(LoginLocators.FIRST_NAME_INPUT)
    assert login_page.is_field_invalid(LoginLocators.LAST_NAME_INPUT)
    assert login_page.is_field_invalid(LoginLocators.USER_NAME_INPUT_REG)
    assert login_page.is_field_invalid(LoginLocators.PASSWORD_INPUT_REG)
    time.sleep(1)

def test_register_password_rules(login_page):
    login_page.click_new_user()
    login_page.fill_registration_form("John", "Doe", "johndoe123", "123")
    login_page.click_register_button()
    error = login_page.get_captcha_error()
    assert error == "Please verify reCaptcha to register!"
    time.sleep(1)

def test_register_with_captcha_and_back_to_login(login_page, unique_username):
    login_page.fill_registration_form("asd", "asd", unique_username, "Password123###")
    login_page.check_captcha_checkbox()
    time.sleep(20)
    login_page.click_register_button()
    login_page.page.wait_for_selector("#gotologin", timeout=30000)
    login_page.click_back_to_login()
    assert login_page.get_header_text() == "Login"
    time.sleep(10)


def test_valid_login(login_page, unique_username):
    login_page.fill_login_form(unique_username, "Password123###")
    login_page.click_login()
    time.sleep(10)
    # Ждем, что пользователь залогинен и его имя отображается
    for _ in range(10):
        username = login_page.get_logged_in_username()
        if username:
            break
        time.sleep(1)

    assert username == unique_username

