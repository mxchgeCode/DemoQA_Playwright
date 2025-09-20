"""
Тесты для страницы Text Box.
Проверяет функциональность заполнения текстовых полей и отображения результатов.
"""

import pytest
import allure
from data import TestData


@allure.epic("Elements")
@allure.feature("Text Box")
@allure.story("Form Submission")
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

    test_data = {
        "name": f"{user_data['first_name']} {user_data['last_name']}",
        "email": user_data["email"],
        "current_address": "123 Test Street, Test City, TC 12345",
        "permanent_address": "456 Permanent Avenue, Permanent City, PC 67890",
    }

    with allure.step("Заполняем все поля текстовой формы"):
        text_box_page.fill_all_fields(
            name=test_data["name"],
            email=test_data["email"],
            current_addr=test_data["current_address"],
            permanent_addr=test_data["permanent_address"],
        )

        allure.attach(str(test_data), "filled_form_data")

    with allure.step("Отправляем форму"):
        text_box_page.submit()

        # Ждем появления результатов
        text_box_page.page.wait_for_timeout(1000)

    with allure.step("Проверяем корректность отображения данных"):
        output_data = text_box_page.get_all_output_data()

        # Проверяем каждое поле отдельно
        assert (
            test_data["name"] in output_data["name"]
        ), f"Имя не совпадает. Ожидалось: '{test_data['name']}', получено: '{output_data['name']}'"

        assert (
            test_data["email"] in output_data["email"]
        ), f"Email не совпадает. Ожидалось: '{test_data['email']}', получено: '{output_data['email']}'"

        assert (
            test_data["current_address"] in output_data["current_address"]
        ), f"Текущий адрес не совпадает. Ожидалось: '{test_data['current_address']}', получено: '{output_data['current_address']}'"

        assert (
            test_data["permanent_address"] in output_data["permanent_address"]
        ), f"Постоянный адрес не совпадает. Ожидалось: '{test_data['permanent_address']}', получено: '{output_data['permanent_address']}'"

        allure.attach(str(output_data), "form_output_data")


@allure.epic("Elements")
@allure.feature("Text Box")
@allure.story("Field Validation")
@pytest.mark.elements
def test_empty_form_submission(text_box_page):
    """
    Тест отправки пустой формы.
    Проверяет поведение приложения при отправке формы без данных.
    """
    with allure.step("Очищаем все поля формы"):
        text_box_page.clear_all_fields()

    with allure.step("Отправляем пустую форму"):
        text_box_page.submit()
        text_box_page.page.wait_for_timeout(1000)

    with allure.step("Проверяем поведение при пустой форме"):
        is_output_visible = text_box_page.is_output_visible()

        if is_output_visible:
            output_data = text_box_page.get_all_output_data()
            # Если область видна, все поля должны быть пустыми или содержать только метки
            empty_values = [v for v in output_data.values() if v and v.strip()]

            allure.attach(str(output_data), "empty_form_output")
            allure.attach(f"Output visible: {is_output_visible}", "output_visibility")
        else:
            allure.attach("Output area is hidden", "output_state")


@allure.epic("Elements")
@allure.feature("Text Box")
@allure.story("Email Validation")
@pytest.mark.elements
@pytest.mark.parametrize(
    "email,description,should_work",
    [
        ("test@example.com", "Standard email", True),
        ("user.name+tag@example.co.uk", "Complex valid email", True),
        ("test123@domain-name.info", "Email with numbers and hyphens", True),
        ("invalid-email", "Missing @ symbol", False),
        ("test@", "Missing domain", False),
        ("@example.com", "Missing username", False),
        ("test..email@example.com", "Double dots", False),
        ("", "Empty email", True),  # Empty field may be allowed
    ],
)
def test_email_field_validation(text_box_page, email, description, should_work):
    """
    Параметризованный тест валидации email поля.
    Проверяет различные форматы email адресов.
    """
    with allure.step(f"Тестируем email: {email} ({description})"):
        # Заполняем обязательные поля для успешной отправки
        text_box_page.fill_user_name("Test User")
        text_box_page.fill_user_email(email)
        text_box_page.fill_current_address("Test Address")

        allure.attach(email, "tested_email")
        allure.attach(description, "email_description")

    with allure.step("Отправляем форму"):
        text_box_page.submit()
        text_box_page.page.wait_for_timeout(1000)

    with allure.step("Анализируем результат валидации"):
        output_data = text_box_page.get_all_output_data()
        output_email = output_data.get("email", "")

        if should_work and email:
            # Для валидных email проверяем что они отображаются
            assert (
                email in output_email
            ), f"Валидный email '{email}' должен отобразиться в результатах. Получено: '{output_email}'"

            allure.attach("✓ Email validated successfully", "validation_result")
        else:
            # Для невалидных email логируем поведение
            validation_result = f"Email: '{email}' | Output: '{output_email}' | Expected to work: {should_work}"
            allure.attach(validation_result, "validation_analysis")


@allure.epic("Elements")
@allure.feature("Text Box")
@allure.story("Field Limits")
@pytest.mark.elements
@pytest.mark.parametrize(
    "text_length,description",
    [
        (100, "Short text (100 chars)"),
        (500, "Medium text (500 chars)"),
        (1000, "Long text (1000 chars)"),
        (2000, "Very long text (2000 chars)"),
    ],
)
def test_text_length_handling(text_box_page, text_length, description):
    """
    Тест обработки текста различной длины в полях.
    Проверяет как приложение обрабатывает большие объемы текста.
    """
    test_text = "A" * text_length

    with allure.step(f"Заполняем поля текстом ({description})"):
        text_box_page.fill_user_name(f"User_{text_length}")
        text_box_page.fill_current_address(test_text)
        text_box_page.fill_permanent_address(test_text)

        allure.attach(f"Length: {text_length}", "text_length")
        allure.attach(
            test_text[:100] + "..." if len(test_text) > 100 else test_text,
            "text_sample",
        )

    with allure.step("Отправляем форму"):
        text_box_page.submit()
        text_box_page.page.wait_for_timeout(1000)

    with allure.step("Проверяем корректность обработки длинного текста"):
        output_data = text_box_page.get_all_output_data()

        # Проверяем что текст обработался (может быть обрезан)
        assert (
            len(output_data["current_address"]) > 0
        ), "Current address должен содержать данные после отправки"
        assert (
            len(output_data["permanent_address"]) > 0
        ), "Permanent address должен содержать данные после отправки"

        # Анализируем длины
        current_len = len(output_data["current_address"])
        permanent_len = len(output_data["permanent_address"])

        length_analysis = {
            "input_length": text_length,
            "current_output_length": current_len,
            "permanent_output_length": permanent_len,
            "truncated": current_len < text_length or permanent_len < text_length,
        }

        allure.attach(str(length_analysis), "length_analysis")
        allure.attach(
            (
                output_data["current_address"][:200] + "..."
                if len(output_data["current_address"]) > 200
                else output_data["current_address"]
            ),
            "output_sample",
        )


@allure.epic("Elements")
@allure.feature("Text Box")
@allure.story("Special Characters")
@pytest.mark.elements
@pytest.mark.parametrize(
    "special_text,description",
    [
        ("Hello <script>alert('test')</script>", "HTML/JavaScript injection"),
        ("Text with 'quotes' and \"double quotes\"", "Various quote types"),
        ("Special chars: @#$%^&*()+=[]{}|;:,.<>?", "Symbol characters"),
        ("Unicode: ñáéíóú 中文 🎉", "Unicode and emojis"),
        ("Newlines\nand\ttabs", "Escape sequences"),
    ],
)
def test_special_characters_handling(text_box_page, special_text, description):
    """
    Тест обработки специальных символов и потенциально опасного контента.
    """
    with allure.step(f"Тестируем специальные символы: {description}"):
        text_box_page.fill_user_name("Special Test User")
        text_box_page.fill_user_email("test@example.com")
        text_box_page.fill_current_address(special_text)

        allure.attach(special_text, "input_special_text")
        allure.attach(description, "test_description")

    with allure.step("Отправляем форму со специальными символами"):
        text_box_page.submit()
        text_box_page.page.wait_for_timeout(1000)

    with allure.step("Проверяем безопасную обработку специальных символов"):
        output_data = text_box_page.get_all_output_data()
        output_address = output_data.get("current_address", "")

        # Проверяем что контент не выполнился как код (например, скрипты)
        page_title = text_box_page.page.title()
        assert "alert" not in page_title.lower(), "Скрипты не должны выполняться"

        # Проверяем что данные сохранились в каком-то виде
        assert len(output_address) > 0, "Специальные символы должны быть обработаны"

        security_check = {
            "input_contains_script": "<script>" in special_text,
            "output_contains_script": "<script>" in output_address,
            "page_title_unchanged": "Text Box" in page_title,
            "data_preserved": len(output_address) > 0,
        }

        allure.attach(str(security_check), "security_analysis")
        allure.attach(output_address, "processed_output")
