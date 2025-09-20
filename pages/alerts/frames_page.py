"""
Page Object для страницы Frames.
Содержит методы для работы с iframe элементами.
"""

from playwright.sync_api import Page
from locators.alerts.frames_locators import FramesLocators
from pages.base_page import BasePage


class FramesPage(BasePage):
    """
    Страница тестирования работы с iframe элементами.
    Содержит большой и малый фреймы для демонстрации переключения контекста.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Frames.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def get_big_frame_text(self) -> str:
        """
        Получает текст из большого iframe.

        Returns:
            str: Содержимое текста в большом фрейме
        """
        self.log_step("Получаем текст из большого фрейма")
        frame = self.page.frame_locator(FramesLocators.BIG_FRAME)
        frame_heading = frame.locator(FramesLocators.FRAME_HEADING)
        return frame_heading.inner_text()

    def get_small_frame_text(self) -> str:
        """
        Получает текст из малого iframe.

        Returns:
            str: Содержимое текста в малом фрейме
        """
        self.log_step("Получаем текст из малого фрейма")
        frame = self.page.frame_locator(FramesLocators.SMALL_FRAME)
        frame_heading = frame.locator(FramesLocators.FRAME_HEADING)
        return frame_heading.inner_text()

    def is_big_frame_visible(self) -> bool:
        """
        Проверяет видимость большого iframe.

        Returns:
            bool: True если большой фрейм видим на странице
        """
        return self.page.locator(FramesLocators.BIG_FRAME).is_visible()

    def is_small_frame_visible(self) -> bool:
        """
        Проверяет видимость малого iframe.

        Returns:
            bool: True если малый фрейм видим на странице
        """
        return self.page.locator(FramesLocators.SMALL_FRAME).is_visible()

    def get_frame_count(self) -> int:
        """
        Получает общее количество фреймов на странице.

        Returns:
            int: Количество iframe элементов
        """
        frames = self.page.locator("iframe")
        return frames.count()

    def switch_to_big_frame_context(self):
        """
        Переключается в контекст большого фрейма.

        Returns:
            FrameLocator: Локатор большого фрейма для дальнейшей работы
        """
        self.log_step("Переключаемся в контекст большого фрейма")
        return self.page.frame_locator(FramesLocators.BIG_FRAME)

    def switch_to_small_frame_context(self):
        """
        Переключается в контекст малого фрейма.

        Returns:
            FrameLocator: Локатор малого фрейма для дальнейшей работы
        """
        self.log_step("Переключаемся в контекст малого фрейма")
        return self.page.frame_locator(FramesLocators.SMALL_FRAME)
