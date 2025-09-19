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

    # Обращаемся через login_page.page.locator
    username_input = login_page.page.locator(LoginLocators.USERNAME_INPUT)
    username_class = username_input.get_attribute("class")

    assert (
        "is-invalid" in username_class
    ), "UserName input should have is-invalid class for blank"

    password_input = login_page.page.locator(LoginLocators.PASSWORD_INPUT)
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
    login_page.click_back_to_login()

def test_register_password_rules(login_page):
    login_page.click_new_user()
    login_page.fill_registration_form("John", "Doe", "johndoe123", "123")
    login_page.click_register_button()
    error = login_page.get_captcha_error()
    assert error == "Please verify reCaptcha to register!"
    time.sleep(1)
    login_page.click_back_to_login()


def test_valid_login(login_page):
    """
    СНАЧАЛА
    СОЗДАТЬ ПОЛЬЗОВАТЕЛЯ С УКАЗАННЫМИ КРЕДАМИ
    PLAYWRIGHT НЕ МОЖЕТ ОБОЙТИ КАПЧУ ПРИ РЕГИСТРАЦИИ
    """
    login_page.fill_login_form("asd", "Password123###")
    login_page.click_login()
    time.sleep(10)
    # Ждем, что пользователь залогинен и его имя отображается
    for _ in range(10):
        username = login_page.get_logged_in_username()
        if username:
            break
        time.sleep(1)
    assert username == "asd"

def test_go_to_book_store(login_page):
    """
    ТОЛЬКО ПОСЛЕ ТЕСТА test_valid_login ДЛЯ ЛОГИНА
    """

    # login_page.page.goto("https://demoqa.com/profile")
    login_page.page.click("button#gotoStore")
    login_page.page.wait_for_url("**/books")
    assert "books" in login_page.page.url

def test_search_book_and_go_back(login_page):
    """
        ТОЛЬКО ПОСЛЕ ТЕСТА test_valid_login ДЛЯ ЛОГИНА
    """
    # page = login_page.page
    login_page.page.goto("https://demoqa.com/books")

    login_page.page.fill("input#searchBox", "Git Pocket Guide")
    login_page.page.wait_for_selector(".rt-tbody .rt-tr-group")


    rows = login_page.page.locator(".rt-tbody .rt-tr")


    title = rows.nth(0).locator(".rt-td").nth(1).text_content()
    assert "Git Pocket Guide" in title

    login_page.page.goto("https://demoqa.com/profile")


def test_delete_account_cancel(login_page):
    """
        ТОЛЬКО ПОСЛЕ ТЕСТА test_valid_login ДЛЯ ЛОГИНА
    """

    def on_dialog(dialog):
        assert dialog.type == "confirm"
        dialog.dismiss()

    login_page.page.on("dialog", on_dialog)
    try:
        # login_page.page.click("div.buttonWrap button.btn-primary:has-text('Delete Account')")
        login_page.page.click("button:has-text('Delete Account')")
    except : pass


