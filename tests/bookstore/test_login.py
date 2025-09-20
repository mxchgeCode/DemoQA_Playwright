"""
Тесты авторизации и регистрации пользователей BookStore.
Включает проверку валидации, успешного входа и зависимых от авторизации тестов.
"""

import time
import pytest
import allure
from playwright.sync_api import expect
from data import TestData

from locators.bookstore.login_locators import LoginLocators


@allure.epic("BookStore")
@allure.feature("Authentication")
@allure.story("Invalid login attempts")
def test_invalid_login(login_page):
    """
    Тест входа с неверными учетными данными.
    Проверяет отображение корректного сообщения об ошибке.
    """
    with allure.step("Попытка входа с неверными данными"):
        login_page.login("wrong_user", "wrong_password")

    with allure.step("Проверка сообщения об ошибке"):
        error = login_page.get_error_message()
        assert (
            error == "Invalid username or password!"
        ), f"Expected error message, got: {error}"


@allure.epic("BookStore")
@allure.feature("Authentication")
@allure.story("Form validation")
def test_blank_login(login_page):
    """
    Тест валидации формы при пустых полях входа.
    Проверяет появление класса валидационной ошибки.
    """
    with allure.step("Попытка входа с пустыми полями"):
        login_page.login("", "")

    with allure.step("Проверка валидации поля username"):
        username_input = login_page.page.locator(LoginLocators.USERNAME_INPUT)
        username_class = username_input.get_attribute("class")
        assert (
            "is-invalid" in username_class
        ), "UserName input should have is-invalid class"

    with allure.step("Проверка валидации поля password"):
        password_input = login_page.page.locator(LoginLocators.PASSWORD_INPUT)
        password_class = password_input.get_attribute("class")
        assert (
            "is-invalid" in password_class
        ), "Password input should have is-invalid class"


@allure.epic("BookStore")
@allure.feature("Registration")
@allure.story("Form validation")
def test_new_user_register_empty_fields(login_page):
    """
    Тест валидации формы регистрации при пустых обязательных полях.
    """
    with allure.step("Переход к форме регистрации"):
        login_page.click_new_user()
        assert login_page.get_header_text() == "Register"

    with allure.step("Отправка формы с пустыми полями"):
        login_page.click_register_button()

    with allure.step("Проверка валидации всех обязательных полей"):
        assert login_page.is_field_invalid(LoginLocators.FIRST_NAME_INPUT)
        assert login_page.is_field_invalid(LoginLocators.LAST_NAME_INPUT)
        assert login_page.is_field_invalid(LoginLocators.USER_NAME_INPUT_REG)
        assert login_page.is_field_invalid(LoginLocators.PASSWORD_INPUT_REG)

    with allure.step("Возврат к форме входа"):
        time.sleep(1)
        login_page.click_back_to_login()


@allure.epic("BookStore")
@allure.feature("Registration")
@allure.story("CAPTCHA validation")
def test_register_password_rules(login_page):
    """
    Тест валидации reCAPTCHA при регистрации пользователя.
    """
    with allure.step("Переход к форме регистрации"):
        login_page.click_new_user()

    with allure.step("Заполнение формы регистрации"):
        login_page.fill_registration_form("John", "Doe", "johndoe123", "123")

    with allure.step("Отправка формы без решения CAPTCHA"):
        login_page.click_register_button()

    with allure.step("Проверка ошибки CAPTCHA"):
        error = login_page.get_captcha_error()
        assert error == "Please verify reCaptcha to register!"

    with allure.step("Возврат к форме входа"):
        time.sleep(1)
        login_page.click_back_to_login()


@pytest.mark.dependency()
@allure.epic("BookStore")
@allure.feature("Authentication")
@allure.story("Successful login")
def test_valid_login(login_page):
    """
    Базовый тест успешного входа в систему.
    ПРЕДВАРИТЕЛЬНО СОЗДАТЬ ПОЛЬЗОВАТЕЛЯ С УКАЗАННЫМИ КРЕДАМИ
    PLAYWRIGHT НЕ МОЖЕТ ОБОЙТИ КАПЧУ ПРИ РЕГИСТРАЦИИ.
    """
    p = TestData.USERS.test_user

    with allure.step("Делаем логин с валидными данными"):
        login_page.login(p.username, p.password)

    with allure.step("Ожидание и проверка успешной авторизации"):
        expect(login_page.get_logged_in_username().to_have_text(p.username))



@pytest.mark.dependency(depends=["test_valid_login"])
@allure.epic("BookStore")
@allure.feature("Navigation")
@allure.story("Go to book store")
def test_go_to_book_store(login_page):
    """
    Тест перехода в книжный магазин после успешной авторизации.
    Зависит от test_valid_login.
    """
    with allure.step("Нажатие кнопки перехода в магазин"):
        login_page.page.click("button#gotoStore")

    with allure.step("Ожидание загрузки страницы книг"):
        login_page.page.wait_for_url("**/books")

    with allure.step("Проверка URL страницы книг"):
        assert "books" in login_page.page.url


@pytest.mark.dependency(depends=["test_valid_login"])
@allure.epic("BookStore")
@allure.feature("Book Search")
@allure.story("Search and navigation")
def test_search_book_and_go_back(login_page):
    """
    Тест поиска книги и навигации.
    ТОЛЬКО ПОСЛЕ ТЕСТА test_valid_login ДЛЯ ЛОГИНА.
    """
    with allure.step("Переход на страницу книг"):
        login_page.page.goto("https://demoqa.com/books")

    with allure.step("Поиск книги 'Git Pocket Guide'"):
        login_page.page.fill("input#searchBox", "Git Pocket Guide")
        login_page.page.wait_for_selector(".rt-tbody .rt-tr-group")

    with allure.step("Проверка результатов поиска"):
        rows = login_page.page.locator(".rt-tbody .rt-tr")
        title = rows.nth(0).locator(".rt-td").nth(1).text_content()
        assert (
            "Git Pocket Guide" in title
        ), f"Expected 'Git Pocket Guide' in title, got: {title}"

    with allure.step("Переход в профиль пользователя"):
        login_page.page.goto("https://demoqa.com/profile")


@pytest.mark.dependency(depends=["test_valid_login"])
@allure.epic("BookStore")
@allure.feature("Account Management")
@allure.story("Delete account confirmation")
def test_delete_account_cancel(login_page):
    """
    Тест отмены удаления учетной записи.
    Проверяет корректную обработку диалогового окна подтверждения.
    """

    def on_dialog(dialog):
        """Обработчик диалогового окна подтверждения."""
        assert dialog.type == "confirm", f"Expected confirm dialog, got: {dialog.type}"
        dialog.dismiss()

    with allure.step("Настройка обработчика диалогового окна"):
        login_page.page.on("dialog", on_dialog)

    with allure.step("Нажатие кнопки удаления аккаунта"):
        login_page.page.click("button:has-text('Delete Account')")
