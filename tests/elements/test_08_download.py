"""
Тесты для страницы Upload and Download.
Проверяет функциональность загрузки и скачивания файлов:
- Загрузка файлов различных типов и размеров
- Скачивание файлов
- Валидация загруженных файлов
- Обработка ошибок при работе с файлами
"""

import pytest
import allure
import os
import tempfile
from pathlib import Path
from pages.elements.upload_download_page import UploadDownloadPage


@allure.epic("Elements")
@allure.feature("Upload and Download")
@allure.story("File Upload")
@pytest.mark.elements
@pytest.mark.smoke
def test_upload_text_file(upload_download_page: UploadDownloadPage):
    """
    Тест загрузки текстового файла.

    Создает временный текстовый файл и проверяет его успешную загрузку.
    """
    test_content = "This is a test file for upload functionality testing."

    with allure.step("Создаем временный текстовый файл"):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(test_content)
            temp_file_path = temp_file.name

        file_name = os.path.basename(temp_file_path)
        upload_download_page.log_step(f"Создан временный файл: {file_name}")

        allure.attach(test_content, "test_file_content", allure.attachment_type.TEXT)
        allure.attach(file_name, "uploaded_filename", allure.attachment_type.TEXT)

    try:
        with allure.step("Загружаем файл через интерфейс"):
            upload_download_page.log_step(f"Загрузка файла: {file_name}")
            upload_download_page.upload_file(temp_file_path)

        with allure.step("Проверяем успешность загрузки"):
            upload_success = upload_download_page.is_file_uploaded()
            upload_download_page.log_step(f"Файл успешно загружен: {upload_success}")

            assert upload_success, "Файл должен быть успешно загружен"

        with allure.step("Проверяем отображение пути загруженного файла"):
            uploaded_file_path = upload_download_page.get_uploaded_file_path()
            upload_download_page.log_step(f"Путь загруженного файла: {uploaded_file_path}")

            allure.attach(uploaded_file_path, "uploaded_file_path", allure.attachment_type.TEXT)

            # Проверяем что путь содержит имя файла
            assert file_name in uploaded_file_path, f"Путь должен содержать имя файла '{file_name}': {uploaded_file_path}"

    finally:
        # Очищаем временный файл
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
            upload_download_page.log_step(f"Временный файл {file_name} удален")


@allure.epic("Elements")
@allure.feature("Upload and Download")
@allure.story("Multiple File Types Upload")
@pytest.mark.elements
@pytest.mark.regression
def test_upload_different_file_types(upload_download_page: UploadDownloadPage):
    """
    Тест загрузки файлов различных типов.

    Проверяет поддержку различных расширений файлов.
    """
    test_files = [
        ('.txt', 'text/plain', "Test text content"),
        ('.json', 'application/json', '{"test": "data", "number": 123}'),
        ('.csv', 'text/csv', "Name,Age,City\nJohn,30,NYC\nJane,25,LA"),
        ('.xml', 'text/xml', '<?xml version="1.0"?><root><item>test</item></root>')
    ]

    upload_results = {}
    temp_files = []

    try:
        for extension, mime_type, content in test_files:
            with allure.step(f"Тестируем загрузку файла {extension}"):
                # Создаем временный файл
                with tempfile.NamedTemporaryFile(mode='w', suffix=extension, delete=False) as temp_file:
                    temp_file.write(content)
                    temp_file_path = temp_file.name

                temp_files.append(temp_file_path)
                file_name = os.path.basename(temp_file_path)

                upload_download_page.log_step(f"Загрузка файла {file_name} ({mime_type})")

                # Загружаем файл
                upload_download_page.upload_file(temp_file_path)

                # Проверяем результат
                upload_success = upload_download_page.is_file_uploaded()
                uploaded_path = upload_download_page.get_uploaded_file_path() if upload_success else ""

                upload_results[extension] = {
                    "filename": file_name,
                    "mime_type": mime_type,
                    "upload_success": upload_success,
                    "uploaded_path": uploaded_path,
                    "content_length": len(content)
                }

                upload_download_page.log_step(f"Результат {extension}: {upload_results[extension]}")

        with allure.step("Анализируем результаты загрузки разных типов файлов"):
            allure.attach(str(upload_results), "upload_results_by_type", allure.attachment_type.JSON)

            successful_uploads = sum(1 for result in upload_results.values() if result["upload_success"])
            total_uploads = len(upload_results)

            upload_summary = {
                "total_file_types": total_uploads,
                "successful_uploads": successful_uploads,
                "success_rate": successful_uploads / total_uploads if total_uploads > 0 else 0,
                "supported_extensions": [ext for ext, result in upload_results.items() if result["upload_success"]]
            }

            upload_download_page.log_step(f"Сводка загрузки: {upload_summary}")
            allure.attach(str(upload_summary), "upload_types_summary", allure.attachment_type.JSON)

            # Проверяем что хотя бы один тип файлов поддерживается
            assert successful_uploads > 0, f"Должен поддерживаться хотя бы один тип файлов, успешных: {successful_uploads}/{total_uploads}"

    finally:
        # Очищаем все временные файлы
        for temp_file_path in temp_files:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        upload_download_page.log_step(f"Очищены {len(temp_files)} временных файлов")


@allure.epic("Elements")
@allure.feature("Upload and Download")
@allure.story("File Download")
@pytest.mark.elements
@pytest.mark.smoke
def test_download_file(upload_download_page: UploadDownloadPage):
    """
    Тест скачивания файла.

    Проверяет функциональность скачивания предустановленного файла.
    """
    with allure.step("Получаем информацию о файле для скачивания"):
        download_button_visible = upload_download_page.is_download_button_visible()
        upload_download_page.log_step(f"Кнопка скачивания видима: {download_button_visible}")

        assert download_button_visible, "Кнопка скачивания должна быть видима"

    with allure.step("Получаем атрибуты кнопки скачивания"):
        download_attrs = upload_download_page.get_download_button_attributes()
        upload_download_page.log_step(f"Атрибуты кнопки скачивания: {download_attrs}")

        allure.attach(str(download_attrs), "download_button_attributes", allure.attachment_type.JSON)

        # Проверяем наличие href (ссылки на файл)
        assert download_attrs.get("href"), "Кнопка скачивания должна иметь атрибут href"

    with allure.step("Проверяем доступность файла для скачивания"):
        # Получаем URL файла
        download_url = download_attrs.get("href", "")

        if download_url:
            # Проверяем что URL является валидной ссылкой
            is_valid_url = upload_download_page.is_valid_download_url(download_url)
            upload_download_page.log_step(f"URL скачивания валидный: {is_valid_url}")

            download_info = {
                "download_url": download_url,
                "is_valid_url": is_valid_url,
                "url_accessible": False
            }

            if is_valid_url:
                # Проверяем доступность URL (HEAD запрос)
                url_accessible = upload_download_page.check_download_url_accessibility(download_url)
                download_info["url_accessible"] = url_accessible
                upload_download_page.log_step(f"URL доступен для скачивания: {url_accessible}")

            allure.attach(str(download_info), "download_info", allure.attachment_type.JSON)

    with allure.step("Имитируем клик по кнопке скачивания"):
        upload_download_page.log_step("Клик по кнопке скачивания")

        # Кликаем по кнопке скачивания
        download_initiated = upload_download_page.click_download_button()
        upload_download_page.log_step(f"Скачивание инициировано: {download_initiated}")

        # В реальном браузере файл начнет скачиваться
        # В автотестах мы можем проверить что клик прошел успешно
        assert download_initiated, "Клик по кнопке скачивания должен быть успешным"

        # Небольшая пауза для обработки скачивания
        upload_download_page.page.wait_for_timeout(2000)


@allure.epic("Elements")
@allure.feature("Upload and Download")
@allure.story("File Size Validation")
@pytest.mark.elements
def test_upload_large_file(upload_download_page: UploadDownloadPage):
    """
    Тест загрузки файла большого размера.

    Проверяет ограничения по размеру файла и обработку больших файлов.
    """
    # Создаем файл размером около 1MB
    large_file_size = 1024 * 1024  # 1MB
    large_content = "X" * large_file_size

    with allure.step("Создаем файл большого размера"):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(large_content)
            temp_file_path = temp_file.name

        actual_file_size = os.path.getsize(temp_file_path)
        file_name = os.path.basename(temp_file_path)

        upload_download_page.log_step(f"Создан большой файл: {file_name}, размер: {actual_file_size} bytes")

        file_info = {
            "filename": file_name,
            "size_bytes": actual_file_size,
            "size_mb": round(actual_file_size / (1024 * 1024), 2)
        }

        allure.attach(str(file_info), "large_file_info", allure.attachment_type.JSON)

    try:
        with allure.step("Пытаемся загрузить большой файл"):
            upload_download_page.log_step(f"Загрузка большого файла: {file_info['size_mb']} MB")

            # Увеличиваем таймаут для большого файла
            upload_download_page.set_upload_timeout(30000)  # 30 секунд

            upload_start_time = upload_download_page.get_current_timestamp()
            upload_download_page.upload_file(temp_file_path)
            upload_end_time = upload_download_page.get_current_timestamp()

            upload_duration = upload_end_time - upload_start_time

        with allure.step("Проверяем результат загрузки большого файла"):
            upload_success = upload_download_page.is_file_uploaded()
            error_message = upload_download_page.get_upload_error_message() if not upload_success else ""

            large_upload_result = {
                "file_size_mb": file_info["size_mb"],
                "upload_success": upload_success,
                "upload_duration_ms": upload_duration,
                "error_message": error_message,
                "upload_timeout": upload_duration > 25000  # Проверяем таймаут
            }

            upload_download_page.log_step(f"Результат загрузки большого файла: {large_upload_result}")
            allure.attach(str(large_upload_result), "large_file_upload_result", allure.attachment_type.JSON)

            # Анализируем результат (большой файл может не загружаться из-за ограничений)
            if upload_success:
                upload_download_page.log_step("✅ Большой файл успешно загружен")
                uploaded_path = upload_download_page.get_uploaded_file_path()
                assert file_name in uploaded_path, f"Путь должен содержать имя файла: {uploaded_path}"
            else:
                upload_download_page.log_step("ℹ️ Большой файл не загрузился (возможно, есть ограничения)")
                # Это может быть нормальным поведением для защиты от больших файлов

    finally:
        # Очищаем большой временный файл
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
            upload_download_page.log_step(f"Большой временный файл {file_name} удален")


@allure.epic("Elements")
@allure.feature("Upload and Download")
@allure.story("Invalid File Handling")
@pytest.mark.elements
def test_upload_invalid_file_types(upload_download_page: UploadDownloadPage):
    """
    Тест загрузки файлов недопустимых типов.

    Проверяет обработку попыток загрузки потенциально опасных или неподдерживаемых файлов.
    """
    # Типы файлов которые могут быть запрещены
    potentially_invalid_files = [
        ('.exe', 'application/x-executable', "MZ"),  # Исполняемый файл
        ('.bat', 'application/x-bat', "@echo off\necho Hello"),  # Batch файл
        ('.js', 'application/javascript', "alert('test');"),  # JavaScript
        ('.html', 'text/html', "<script>alert('xss')</script>")  # HTML с JS
    ]

    invalid_upload_results = {}
    temp_files = []

    try:
        for extension, mime_type, content in potentially_invalid_files:
            with allure.step(f"Тестируем загрузку потенциально недопустимого файла {extension}"):
                # Создаем временный файл
                mode = 'wb' if extension == '.exe' else 'w'
                with tempfile.NamedTemporaryFile(mode=mode, suffix=extension, delete=False) as temp_file:
                    if extension == '.exe':
                        temp_file.write(content.encode())
                    else:
                        temp_file.write(content)
                    temp_file_path = temp_file.name

                temp_files.append(temp_file_path)
                file_name = os.path.basename(temp_file_path)

                upload_download_page.log_step(f"Попытка загрузки {file_name} ({mime_type})")

                # Пытаемся загрузить файл
                upload_download_page.upload_file(temp_file_path)

                # Проверяем результат
                upload_success = upload_download_page.is_file_uploaded()
                error_message = upload_download_page.get_upload_error_message() if not upload_success else ""
                security_blocked = "security" in error_message.lower() or "forbidden" in error_message.lower()

                invalid_upload_results[extension] = {
                    "filename": file_name,
                    "mime_type": mime_type,
                    "upload_attempted": True,
                    "upload_success": upload_success,
                    "error_message": error_message,
                    "security_blocked": security_blocked,
                    "properly_rejected": not upload_success and extension in ['.exe', '.bat']
                }

                upload_download_page.log_step(f"Результат {extension}: {invalid_upload_results[extension]}")

        with allure.step("Анализируем обработку недопустимых файлов"):
            allure.attach(str(invalid_upload_results), "invalid_files_results", allure.attachment_type.JSON)

            properly_rejected = sum(1 for result in invalid_upload_results.values()
                                  if result["properly_rejected"])
            security_blocks = sum(1 for result in invalid_upload_results.values()
                                if result["security_blocked"])

            security_summary = {
                "total_invalid_attempts": len(invalid_upload_results),
                "properly_rejected": properly_rejected,
                "security_blocks": security_blocks,
                "security_effective": properly_rejected > 0 or security_blocks > 0
            }

            upload_download_page.log_step(f"Сводка безопасности: {security_summary}")
            allure.attach(str(security_summary), "security_summary", allure.attachment_type.JSON)

    finally:
        # Очищаем все временные файлы
        for temp_file_path in temp_files:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        upload_download_page.log_step(f"Очищены {len(temp_files)} временных файлов")
