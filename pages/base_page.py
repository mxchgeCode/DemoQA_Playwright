"""
Базовый класс для всех Page Object с общими утилитами.
Содержит методы ожидания, безопасных кликов и логирования.
"""

import logging
from typing import Optional, Union
from playwright.sync_api import Page, Locator

logger = logging.getLogger(__name__)


class BasePage:
    """
    Базовый класс для всех Page Object моделей.
    Предоставляет общие методы для взаимодействия с элементами страницы.
    """

    def __init__(self, page: Page):
        """
        Инициализация базовой страницы.

        Args:
            page: Экземпляр страницы Playwright
        """
        self.page = page

    def wait_for_visible(self, selector: Union[str, Locator], timeout: int = 10000) -> None:
        """
        Ожидает появления видимого элемента на странице.
    
        Args:
            selector: CSS селектор элемента или Locator
            timeout: Максимальное время ожидания в миллисекундах
    
        Raises:
            TimeoutError: Если элемент не появился за указанное время
        """
        if isinstance(selector, str):
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        else:
            selector.wait_for(state="visible", timeout=timeout)

    def safe_click(self, selector: Union[str, Locator], timeout: int = 10000) -> None:
        """
        Безопасный клик по элементу с предварительным ожиданием.
    
        Args:
            selector: CSS селектор элемента или Locator
            timeout: Максимальное время ожидания элемента
        """
        self.wait_for_visible(selector, timeout)
        if isinstance(selector, str):
            self.page.click(selector)
        else:
            selector.first.click()

    def safe_fill(self, selector: Union[str, Locator], text: str, timeout: int = 10000) -> None:
        """
        Безопасное заполнение поля с предварительным ожиданием.
    
        Args:
            selector: CSS селектор поля ввода или Locator
            text: Текст для ввода
            timeout: Максимальное время ожидания элемента
        """
        self.wait_for_visible(selector, timeout)
        if isinstance(selector, str):
            self.page.fill(selector, text)
        else:
            selector.first.fill(text)

    def get_text_safe(self, selector: Union[str, Locator], timeout: int = 5000) -> Optional[str]:
        """
        Безопасное получение текста элемента.
    
        Args:
            selector: CSS селектор элемента или Locator
            timeout: Максимальное время ожидания элемента
    
        Returns:
            str или None: Текст элемента или None если элемент не найден
        """
        try:
            locator = self.page.locator(selector) if isinstance(selector, str) else selector
            locator = locator.first
            locator.wait_for(state="visible", timeout=timeout)
            return (locator.inner_text() or "").strip()
        except Exception as e:
            logger.warning(f"Не удалось получить текст для {selector}: {e}")
            return None

    def wait_for_url_contains(self, url_part: str, timeout: int = 10000) -> bool:
        """
        Ожидает, пока URL не будет содержать указанную строку.

        Args:
            url_part: Часть URL для поиска
            timeout: Максимальное время ожидания

        Returns:
            bool: True если URL содержит нужную строку
        """
        try:
            self.page.wait_for_url(f"**/*{url_part}*", timeout=timeout)
            return True
        except:
            return False

    def log_step(self, step_description: str) -> None:
        """
        Логирует шаг теста для отладки.

        Args:
            step_description: Описание выполняемого шага
        """
        logger.info(f"Шаг: {step_description}")
