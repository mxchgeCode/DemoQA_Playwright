"""
Page Object для страницы Upload and Download.
Содержит методы для загрузки файлов на сервер и скачивания файлов.
"""

import os
from playwright.sync_api import Page
from locators.elements.download_locators import UploadDownloadLocators
from pages.base_page import BasePage


class UploadDownloadPage(BasePage):
    """
    Страница тестирования загрузки и скачивания файлов.
    Поддерживает загрузку файлов через input и скачивание через download link.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы загрузки/скачивания.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def upload_file(self, file_path: str) -> None:
        """
        Загружает файл на сервер через input элемент.

        Args:
            file_path: Полный путь к загружаемому файлу

        Preconditions: файл должен существовать по указанному пути
        Postconditions: файл загружен, отображается путь к загруженному файлу
        """
        self.log_step(f"Загружаем файл: {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        self.page.set_input_files(UploadDownloadLocators.UPLOAD_INPUT, file_path)

    def get_uploaded_file_path_text(self) -> str:
        """
        Получает отображаемый путь к загруженному файлу.

        Returns:
            str: Путь к загруженному файлу как показано на странице
        """
        return self.get_text_safe(UploadDownloadLocators.UPLOAD_PATH_TEXT)

    def download_file(self, download_path: str) -> str:
        """
        Скачивает файл по ссылке и сохраняет в указанную директорию.

        Args:
            download_path: Путь к директории для сохранения файла

        Returns:
            str: Полный путь к сохраненному файлу

        Postconditions: файл скачан и сохранен в указанной директории
        """
        self.log_step(f"Скачиваем файл в директорию: {download_path}")

        if not os.path.exists(download_path):
            os.makedirs(download_path)

        with self.page.expect_download() as download_info:
            self.safe_click(UploadDownloadLocators.DOWNLOAD_BUTTON)

        download = download_info.value
        file_path = os.path.join(download_path, download.suggested_filename)
        download.save_as(file_path)

        return file_path

    def is_upload_successful(self) -> bool:
        """
        Проверяет, успешно ли прошла загрузка файла.

        Returns:
            bool: True если отображается путь к загруженному файлу
        """
        path_text = self.get_uploaded_file_path_text()
        return path_text is not None and len(path_text.strip()) > 0

    def get_download_button_text(self) -> str:
        """
        Получает текст кнопки скачивания.

        Returns:
            str: Текст на кнопке скачивания
        """
        return self.get_text_safe(UploadDownloadLocators.DOWNLOAD_BUTTON)

    # === Методы для совместимости с тестами ===

    def is_file_uploaded(self) -> bool:
        """
        Проверяет, успешно ли прошла загрузка файла.

        Returns:
            bool: True если файл загружен успешно
        """
        return self.is_upload_successful()

    def is_download_button_visible(self) -> bool:
        """
        Проверяет видимость кнопки скачивания.

        Returns:
            bool: True если кнопка скачивания видима
        """
        return self.page.locator(UploadDownloadLocators.DOWNLOAD_BUTTON).is_visible()

    def set_upload_timeout(self, timeout_ms: int) -> None:
        """
        Устанавливает таймаут для загрузки файлов.

        Args:
            timeout_ms: Таймаут в миллисекундах
        """
        self.page.set_default_timeout(timeout_ms)
