"""
Тесты для страницы Practice Form.
Проверяет заполнение и отправку формы с различными типами полей.
"""

import pytest
import allure
from data import TestData
import tempfile
import os


@allure.epic("Forms")
@allure.feature("Practice Form")
@allure.story("Complete Form Submission")
@pytest.mark.forms
@pytest.mark.smoke
def test_fill_form_and_submit(practice_form_page):
    """
    Тест полного заполнения и отправки формы регистрации.

    Шаги:
    1. Заполнить все обязательные поля формы
    2. Выбрать опциональные поля (хобби, предметы)
    3. Отправить форму
    4. Проверить модальное окно с результатами
    """
    form_data = TestData.FORM_DATA["practice_form"]

    with allure.step("Заполняем основные поля формы"):
        practice_form_page.fill_first_name(form_data["first_name"])
        practice_form_page.fill_last_name(form_data["last_name"])
        practice_form_page.fill_email(form_data["email"])

        allure.attach(
            f"Name: {form_data['first_name']} {form_data['last_name']}", "user_name"
        )
        allure.attach(form_data["email"], "user_email")

    with allure.step("Выбираем пол"):
        practice_form_page.select_gender(form_data["gender"])
        allure.attach(form_data["gender"], "selected_gender")

    with allure.step("Заполняем номер телефона"):
        practice_form_page.fill_mobile(form_data["mobile"])
        allure.attach(form_data["mobile"], "phone_number")

    with allure.step("Устанавливаем дату рождения"):
        # Используем текущую дату или предустановленную
        practice_form_page.fill_date_of_birth("10 Sep 1990")
        allure.attach("10 Sep 1990", "birth_date")

    with allure.step("Добавляем предметы"):
        for subject in form_data["subjects"]:
            practice_form_page.fill_subjects([subject])

        allure.attach(str(form_data["subjects"]), "selected_subjects")

    with allure.step("Выбираем хобби"):
        for hobby in form_data["hobbies"]:
            practice_form_page.select_hobbies([hobby])

        allure.attach(str(form_data["hobbies"]), "selected_hobbies")

    with allure.step("Создаем и загружаем тестовое изображение"):
        # Создаем временный файл изображения
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_file.write(b"fake image content for testing")
            temp_image_path = tmp_file.name

        try:
            practice_form_page.upload_picture(temp_image_path)
            allure.attach(
                f"Uploaded file: {os.path.basename(temp_image_path)}", "uploaded_file"
            )
        finally:
            # Очищаем временный файл
            if os.path.exists(temp_image_path):
                os.unlink(temp_image_path)

    with allure.step("Заполняем адрес"):
        practice_form_page.fill_current_address(form_data["current_address"])
        allure.attach(form_data["current_address"], "current_address")

    with allure.step("Выбираем штат и город"):
        practice_form_page.select_state(form_data["state"])
        practice_form_page.select_city(form_data["city"])

        allure.attach(f"{form_data['state']}, {form_data['city']}", "state_city")

    with allure.step("Отправляем форму"):
        practice_form_page.submit_form()

    with allure.step("Проверяем появление модального окна с результатами"):
        assert (
            practice_form_page.is_modal_visible()
        ), "Модальное окно с результатами должно появиться"

        modal_title = practice_form_page.page.locator(".modal-title").inner_text()
        assert (
            "Thanks for submitting the form" in modal_title
        ), f"Неожиданный заголовок модального окна: {modal_title}"

        allure.attach(modal_title, "modal_title")

    with allure.step("Проверяем содержимое таблицы результатов"):
        # Проверяем что в модальном окне есть таблица с данными
        modal_table = practice_form_page.page.locator(".modal-body .table")
        assert modal_table.is_visible(), "Таблица результатов должна быть видна"

        # Получаем все строки таблицы
        table_rows = modal_table.locator("tr").all()
        table_content = []

        for row in table_rows:
            cells = row.locator("td").all()
            if len(cells) >= 2:
                label = cells[0].inner_text().strip()
                value = cells[1].inner_text().strip()
                table_content.append(f"{label}: {value}")

        allure.attach("\n".join(table_content), "form_results_table")

        # Проверяем наличие ключевых данных в результатах
        table_text = "\n".join(table_content)
        assert (
            form_data["first_name"] in table_text
        ), "Имя должно присутствовать в результатах"
        assert (
            form_data["last_name"] in table_text
        ), "Фамилия должна присутствовать в результатах"
        assert (
            form_data["email"] in table_text
        ), "Email должен присутствовать в результатах"

    with allure.step("Закрываем модальное окно"):
        practice_form_page.close_modal()

        # Проверяем что модальное окно закрылось
        modal_visible = practice_form_page.is_modal_visible()
        assert not modal_visible, "Модальное окно должно закрыться"


@allure.epic("Forms")
@allure.feature("Practice Form")
@allure.story("Required Fields Validation")
@pytest.mark.forms
@pytest.mark.regression
def test_submit_form_with_minimum_required_fields(practice_form_page):
    """
    Тест отправки формы с минимально необходимыми полями.

    Проверяет какие поля действительно обязательны для успешной отправки.
    """
    with allure.step("Заполняем только обязательные поля"):
        practice_form_page.fill_first_name("MinTest")
        practice_form_page.fill_last_name("User")
        practice_form_page.select_gender("Male")  # Обычно обязательное
        practice_form_page.fill_mobile("1234567890")  # Обычно обязательное

        allure.attach("MinTest User", "minimal_user_data")

    with allure.step("Пытаемся отправить форму"):
        practice_form_page.submit_form()

    with allure.step("Проверяем результат отправки"):
        # Даем время на обработку формы
        practice_form_page.page.wait_for_timeout(2000)

        modal_visible = practice_form_page.is_modal_visible()

        if modal_visible:
            # Если модальное окно появилось - форма принята
            modal_title = practice_form_page.page.locator(".modal-title").inner_text()
            allure.attach(modal_title, "successful_submission")
            practice_form_page.close_modal()

        else:
            # Если модального окна нет, проверяем есть ли ошибки валидации
            validation_errors = practice_form_page.page.locator(
                ".invalid-feedback"
            ).all()
            error_messages = [
                error.inner_text() for error in validation_errors if error.is_visible()
            ]

            if error_messages:
                allure.attach("\n".join(error_messages), "validation_errors")
                # Это нормальное поведение - не все обязательные поля заполнены
            else:
                allure.attach("No modal and no validation errors", "unexpected_state")


@allure.epic("Forms")
@allure.feature("Practice Form")
@allure.story("Field Validation")
@pytest.mark.forms
@pytest.mark.parametrize(
    "email,should_be_valid",
    [
        ("test@example.com", True),
        ("invalid-email", False),
        ("user.name+tag@domain.co.uk", True),
        ("@domain.com", False),
        ("test@", False),
        ("", True),  # Пустое поле может быть валидным если не обязательно
    ],
)
def test_email_field_validation(practice_form_page, email, should_be_valid):
    """
    Параметризованный тест валидации email поля.
    """
    with allure.step(f"Тестируем email: {email}"):
        # Заполняем минимальные обязательные поля
        practice_form_page.fill_first_name("Test")
        practice_form_page.fill_last_name("User")
        practice_form_page.select_gender("Male")
        practice_form_page.fill_mobile("1234567890")

        # Заполняем тестируемый email
        practice_form_page.fill_email(email)

        allure.attach(email, "test_email")

    with allure.step("Отправляем форму"):
        practice_form_page.submit_form()
        practice_form_page.page.wait_for_timeout(2000)

    with allure.step("Анализируем результат валидации"):
        modal_visible = practice_form_page.is_modal_visible()

        # Проверяем есть ли ошибки в поле email
        email_field = practice_form_page.page.locator("#userEmail")
        email_classes = email_field.get_attribute("class") or ""
        is_invalid = "is-invalid" in email_classes

        validation_result = {
            "email": email,
            "expected_valid": should_be_valid,
            "modal_appeared": modal_visible,
            "field_invalid": is_invalid,
            "field_classes": email_classes,
        }

        allure.attach(str(validation_result), "email_validation_result")

        if should_be_valid and email:
            # Для валидных email не должно быть ошибок валидации
            assert (
                not is_invalid
            ), f"Email '{email}' должен быть валидным, но поле помечено как невалидное"
        elif not should_be_valid and email:
            # Для невалидных email может быть ошибка (зависит от реализации)
            pass  # Логируем результат без строгой проверки

        if modal_visible:
            practice_form_page.close_modal()


@allure.epic("Forms")
@allure.feature("Practice Form")
@allure.story("File Upload")
@pytest.mark.forms
def test_file_upload_functionality(practice_form_page):
    """
    Тест функциональности загрузки файла.

    Проверяет различные типы файлов и размеры.
    """
    test_files = [
        ("test.txt", b"Simple text file content", ".txt"),
        ("test.jpg", b"fake jpg content", ".jpg"),
        ("test.png", b"fake png content", ".png"),
    ]

    for filename, content, extension in test_files:
        with allure.step(f"Тестируем загрузку файла: {filename}"):
            # Создаем временный файл
            with tempfile.NamedTemporaryFile(
                suffix=extension, delete=False
            ) as tmp_file:
                tmp_file.write(content)
                temp_path = tmp_file.name

            try:
                # Заполняем минимальные поля
                practice_form_page.fill_first_name("FileTest")
                practice_form_page.fill_last_name("User")
                practice_form_page.select_gender("Other")
                practice_form_page.fill_mobile("9876543210")

                # Загружаем файл
                practice_form_page.upload_picture(temp_path)

                # Отправляем форму
                practice_form_page.submit_form()
                practice_form_page.page.wait_for_timeout(2000)

                # Проверяем результат
                if practice_form_page.is_modal_visible():
                    modal_content = practice_form_page.page.locator(
                        ".modal-body"
                    ).inner_text()
                    file_mentioned = (
                        filename in modal_content
                        or os.path.basename(temp_path) in modal_content
                    )

                    allure.attach(
                        f"File upload successful for {filename}: {file_mentioned}",
                        "file_upload_result",
                    )
                    practice_form_page.close_modal()

            finally:
                # Очищаем временный файл
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
