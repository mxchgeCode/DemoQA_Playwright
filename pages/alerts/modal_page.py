"""
Page Object для страницы Modal Dialogs.
Содержит методы для работы с модальными диалоговыми окнами.
"""

from playwright.sync_api import Page
from locators.alerts.modal_locators import ModalDialogsLocators
from pages.base_page import BasePage


class ModalPage(BasePage):
    """
    Страница тестирования модальных диалоговых окон.
    Содержит малый и большой модальные диалоги.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Modal Dialogs.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def open_small_modal(self) -> None:
        """
        Открывает малый модальный диалог.
        Postconditions: появляется малый модальный диалог с коротким текстом.
        """
        self.log_step("Открываем малый модальный диалог")
        self.safe_click(ModalDialogsLocators.SMALL_MODAL_BUTTON)
        self.wait_for_visible(ModalDialogsLocators.MODAL_DIALOG, timeout=5000)

    def open_large_modal(self) -> None:
        """
        Открывает большой модальный диалог.
        Postconditions: появляется большой модальный диалог с длинным текстом.
        """
        self.log_step("Открываем большой модальный диалог")
        self.safe_click(ModalDialogsLocators.LARGE_MODAL_BUTTON)
        self.wait_for_visible(ModalDialogsLocators.MODAL_DIALOG, timeout=5000)

    def close_modal_by_x(self) -> None:
        """
        Закрывает модальный диалог нажатием на кнопку X.
        Postconditions: модальный диалог скрыт.
        """
        self.log_step("Закрываем модальный диалог кнопкой X")
        self.safe_click(ModalDialogsLocators.MODAL_CLOSE_BUTTON)

    def close_modal_by_close_button(self) -> None:
        """
        Закрывает модальный диалог нажатием на кнопку Close.
        Postconditions: модальный диалог скрыт.
        """
        self.log_step("Закрываем модальный диалог кнопкой Close")
        self.safe_click(ModalDialogsLocators.MODAL_CLOSE_BUTTON_ALT)

    def close_modal_by_overlay(self) -> None:
        """
        Закрывает модальный диалог кликом по затемненной области (overlay).
        Postconditions: модальный диалог скрыт.
        """
        self.log_step("Закрываем модальный диалог кликом по overlay")
        # Кликаем по затемненной области рядом с диалогом
        modal_backdrop = self.page.locator(ModalDialogsLocators.MODAL_BACKDROP)
        modal_backdrop.click(
            position={"x": 10, "y": 10}
        )  # Клик в левый верхний угол overlay

    def is_modal_visible(self) -> bool:
        """
        Проверяет видимость модального диалога.

        Returns:
            bool: True если модальный диалог видим
        """
        return self.page.locator(ModalDialogsLocators.MODAL_DIALOG).is_visible()

    def get_modal_title(self) -> str:
        """
        Получает заголовок модального диалога.

        Returns:
            str: Текст заголовка модального диалога
        """
        return self.get_text_safe(ModalDialogsLocators.MODAL_TITLE) or ""

    def get_modal_body_text(self) -> str:
        """
        Получает текст содержимого модального диалога.

        Returns:
            str: Текст тела модального диалога
        """
        return self.get_text_safe(ModalDialogsLocators.MODAL_BODY) or ""

    def wait_for_modal_to_close(self, timeout: int = 5000) -> bool:
        """
        Ожидает закрытия модального диалога.

        Args:
            timeout: Максимальное время ожидания в миллисекундах

        Returns:
            bool: True если диалог закрылся в указанное время
        """
        self.log_step("Ожидаем закрытия модального диалога")
        try:
            self.page.wait_for_selector(
                ModalDialogsLocators.MODAL_DIALOG, state="hidden", timeout=timeout
            )
            return True
        except:
            return False

    def get_modal_size_class(self) -> str:
        """
        Получает CSS класс размера модального диалога.

        Returns:
            str: CSS класс определяющий размер модального диалога
        """
        modal = self.page.locator(ModalDialogsLocators.MODAL_DIALOG)
        class_attr = modal.get_attribute("class") or ""

        if "modal-sm" in class_attr:
            return "small"
        elif "modal-lg" in class_attr:
            return "large"
        else:
            return "default"
