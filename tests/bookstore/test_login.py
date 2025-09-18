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
