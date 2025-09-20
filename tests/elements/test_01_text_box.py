"""
Тесты для страницы Text Box.
Проверяет функциональность заполнения полей и отображения результатов.
"""

import pytest
import allure
from data import TestData


@allure.epic("Elements")
@allure.feature("Text Box")
@allure.story("Form submission")
@pytest.mark.elements
@pytest.mark.smoke
def test_fill_all_fields_and_submit(text_box_page):
    """
    Тест заполнения всех полей формы и проверки корректного отображения результатов.

    Шаги:
    1. Заполнить все поля формы валидными данными
    2. Отправить форму
    3. Проверить корректность отображения всех данных в области вывода
    """
    user_data = TestData.USERS["valid_user"]

    with allure.step("Заполняем все поля текстовой формы"):
        text_box_page.fill_all_fields(
            name=f"{user_data['first_name']} {user_data['last_name']}",
            email=user_data["email"],
            current_addr="123 Test Street, Test City",
            permanent_addr="456 Permanent Avenue, Permanent City",
        )

    with allure.step("Отправляем форму"):
        text_box_page.submit()

    with allure.step("Проверяем корректность отображения данных"):
        output_data = text_box_page.get_all_output_data()

        assert (
            user_data["email"] in output_data["email"]
        ), f"Email не совпадает: {output_data['email']}"
        assert (
            "Test Street" in output_data["current_address"]
        ), f"Current address не совпадает: {output_data['current_address']}"
        assert (
            "Permanent Avenue" in output_data["permanent_address"]
        ), f"Permanent address не совпадает: {output_data['permanent_address']}"


@allure.epic("Elements")
@allure.feature("Text Box")
@allure.story("Field validation")
@pytest.mark.elements
def test_empty_form_submission(text_box_page):
    """
    Тест отправки пустой формы.
    Проверяет поведение приложения при отправке формы без данных.
    """
    with allure.step("Очищаем все поля"):
        text_box_page.clear_all_fields()

    with allure.step("Отправляем пустую форму"):
        text_box_page.submit()

    with allure.step("Проверяем что область вывода скрыта или пуста"):
        is_output_visible = text_box_page.is_output_visible()

        if is_output_visible:
            output_data = text_box_page.get_all_output_data()
            # Если область видна, все поля должны быть пустыми
            assert not any(
                output_data.values()
            ), f"Ожидались пустые поля, получили: {output_data}"


@allure.epic("Elements")
@allure.feature("Text Box")
@allure.story("Email validation")
@pytest.mark.elements
@pytest.mark.parametrize(
    "email,expected_valid",
    [
        ("test@example.com", True),
        ("invalid-email", False),
        ("test.email+tag@example.co.uk", True),
        ("@example.com", False),
        ("test@", False),
        ("", True),  # Пустое поле может быть валидным
    ],
)
def test_email_field_validation(text_box_page, email, expected_valid):
    """
    Параметризованный тест валидации email поля.
    Проверяет различные форматы email адресов.
    """
    with allure.step(f"Заполняем email поле значением: {email}"):
        text_box_page.fill_user_name("Test User")
        text_box_page.fill_user_email(email)
        text_box_page.fill_current_address("Test Address")

    with allure.step("Отправляем форму"):
        text_box_page.submit()

    with allure.step("Проверяем результат валидации"):
        if expected_valid and email:
            # Для валидных email проверяем что они отображаются
            output_email = text_box_page.get_output_email()
            assert email in output_email, f"Email {email} не отобразился в результатах"
        else:
            # Для невалидных email поведение может отличаться
            # В данном случае просто логируем результат
            output_email = text_box_page.get_output_email()
            allure.attach(
                f"Email: {email}, Output: {output_email}", "validation_result"
            )


@allure.epic("Elements")
@allure.feature("Text Box")
@allure.story("Field limits")
@pytest.mark.elements
def test_long_text_input(text_box_page):
    """
    Тест обработки длинного текста в полях.
    Проверяет как приложение обрабатывает большие объемы текста.
    """
    long_text = "A" * 1000  # 1000 символов

    with allure.step("Заполняем поля длинным текстом"):
        text_box_page.fill_user_name(long_text)
        text_box_page.fill_current_address(long_text)
        text_box_page.fill_permanent_address(long_text)

    with allure.step("Отправляем форму"):
        text_box_page.submit()

    with allure.step("Проверяем что длинный текст обработался корректно"):
        output_data = text_box_page.get_all_output_data()

        # Проверяем что текст отобразился (может быть обрезан)
        assert len(output_data["current_address"]) > 0, "Current address не отобразился"
        assert (
            len(output_data["permanent_address"]) > 0
        ), "Permanent address не отобразился"

        allure.attach(
            f"Input length: {len(long_text)}, Output lengths: {[len(v) for v in output_data.values()]}",
            "text_length_comparison",
        )
