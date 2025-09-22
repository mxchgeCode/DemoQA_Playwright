"""
Page Object для страницы Nested Frames.
Содержит методы для работы с вложенными iframe элементами.
"""

from playwright.sync_api import Page
from locators.alerts.nested_frames_locators import NestedFramesLocators
from pages.base_page import BasePage


class NestedFramesPage(BasePage):
    """
    Страница тестирования работы с вложенными iframe элементами.
    Содержит родительский фрейм с дочерним фреймом внутри.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Nested Frames.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def get_parent_frame_text(self) -> str:
        """
        Получает текст из родительского фрейма.

        Returns:
            str: Содержимое текста в родительском фрейме
        """
        self.log_step("Получаем текст из родительского фрейма")
        parent_frame = self.page.frame_locator(NestedFramesLocators.PARENT_FRAME)
        return parent_frame.locator(NestedFramesLocators.PARENT_BODY).inner_text()

    def get_child_frame_text(self) -> str:
        """
        Получает текст из дочернего фрейма (вложенного в родительский).

        Returns:
            str: Содержимое текста в дочернем фрейме
        """
        self.log_step("Получаем текст из дочернего фрейма")
        parent_frame = self.page.frame_locator(NestedFramesLocators.PARENT_FRAME)
        child_frame = parent_frame.frame_locator(NestedFramesLocators.CHILD_FRAME)
        return child_frame.locator(NestedFramesLocators.CHILD_TEXT).inner_text()

    def is_parent_frame_visible(self) -> bool:
        """
        Проверяет видимость родительского фрейма.

        Returns:
            bool: True если родительский фрейм видим
        """
        return self.page.locator(NestedFramesLocators.PARENT_FRAME).is_visible()

    def get_nested_frames_count(self) -> int:
        """
        Получает количество всех фреймов на странице (включая вложенные).

        Returns:
            int: Общее количество фреймов
        """
        # Подсчитываем фреймы на основной странице
        main_frames = self.page.locator(NestedFramesLocators.CHILD_FRAME_ALT).count()

        # Подсчитываем вложенные фреймы в родительском фрейме
        try:
            parent_frame = self.page.frame_locator(NestedFramesLocators.PARENT_FRAME)
            nested_frames = parent_frame.locator(
                NestedFramesLocators.CHILD_FRAME_ALT
            ).count()
            return main_frames + nested_frames
        except:
            return main_frames

    def switch_to_parent_frame_context(self):
        """
        Переключается в контекст родительского фрейма.

        Returns:
            FrameLocator: Локатор родительского фрейма
        """
        self.log_step("Переключаемся в контекст родительского фрейма")
        return self.page.frame_locator(NestedFramesLocators.PARENT_FRAME)

    def switch_to_child_frame_context(self):
        """
        Переключается в контекст дочернего фрейма через родительский.

        Returns:
            FrameLocator: Локатор дочернего фрейма
        """
        self.log_step("Переключаемся в контекст дочернего фрейма")
        parent_frame = self.page.frame_locator(NestedFramesLocators.PARENT_FRAME)
        return parent_frame.frame_locator(NestedFramesLocators.CHILD_FRAME)
