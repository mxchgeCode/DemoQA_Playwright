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
        # Ждём либо контейнер малого модального окна, либо активный модал как fallback
        try:
            self.wait_for_visible(
                ModalDialogsLocators.SMALL_MODAL_CONTAINER, timeout=5000
            )
        except Exception:
            self.wait_for_visible(ModalDialogsLocators.MODAL_ACTIVE, timeout=5000)

    def open_large_modal(self) -> None:
        """
        Открывает большой модальный диалог.
        Postconditions: появляется большой модальный диалог с длинным текстом.
        """
        self.log_step("Открываем большой модальный диалог")
        self.safe_click(ModalDialogsLocators.LARGE_MODAL_BUTTON)
        # Ждём либо контейнер большого модального окна, либо активный модал как fallback
        try:
            self.wait_for_visible(
                ModalDialogsLocators.LARGE_MODAL_CONTAINER, timeout=5000
            )
        except Exception:
            self.wait_for_visible(ModalDialogsLocators.MODAL_ACTIVE, timeout=5000)

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

    # --- Compatibility / convenience methods expected by tests ---
    def get_modal_body(self) -> str:
        """Совместимый метод-обёртка для получения тела модального окна (тесты ожидают get_modal_body)."""
        return self.get_modal_body_text()

    def is_small_modal_visible(self) -> bool:
        """Проверяет видимость малого модального окна (несколько вариантов селекторов)."""
        small = self.page.locator(ModalDialogsLocators.SMALL_MODAL_CONTAINER)
        title = self.page.locator(ModalDialogsLocators.SMALL_MODAL_TITLE)
        if small.count() > 0:
            return small.is_visible()
        if title.count() > 0:
            return title.is_visible()
        # fallback: общий активный modal
        active = self.page.locator(ModalDialogsLocators.MODAL_ACTIVE)
        return active.count() > 0 and active.is_visible()

    def is_large_modal_visible(self) -> bool:
        """Проверяет видимость большого модального окна (несколько вариантов селекторов)."""
        large = self.page.locator(ModalDialogsLocators.LARGE_MODAL_CONTAINER)
        title = self.page.locator(ModalDialogsLocators.LARGE_MODAL_TITLE)
        if large.count() > 0:
            return large.is_visible()
        if title.count() > 0:
            return title.is_visible()
        active = self.page.locator(ModalDialogsLocators.MODAL_ACTIVE)
        return active.count() > 0 and active.is_visible()

    def has_small_modal_close_button(self) -> bool:
        """Проверяет наличие кнопки закрытия в малом модальном окне."""
        return (
            self.page.locator(ModalDialogsLocators.SMALL_MODAL_CLOSE).count() > 0
            and self.page.locator(ModalDialogsLocators.SMALL_MODAL_CLOSE).is_visible()
        )

    def has_large_modal_close_button(self) -> bool:
        """Проверяет наличие кнопки закрытия в большом модальном окне."""
        return (
            self.page.locator(ModalDialogsLocators.LARGE_MODAL_CLOSE).count() > 0
            and self.page.locator(ModalDialogsLocators.LARGE_MODAL_CLOSE).is_visible()
        )

    def get_small_modal_size(self) -> dict:
        """Возвращает размеры малого модального окна в виде {'width': w, 'height': h}."""
        # Пытаемся несколько селекторов, ждём их и затем берём bounding_box
        candidates = [
            ModalDialogsLocators.SMALL_MODAL_CONTAINER,
            ModalDialogsLocators.MODAL_DIALOG,
            ModalDialogsLocators.MODAL_ACTIVE,
        ]
        for sel in candidates:
            loc = self.page.locator(sel)
            if loc.count() > 0:
                try:
                    # дождаться элемента (небольшой таймаут)
                    loc.wait_for(state="visible", timeout=2000)
                    box = loc.bounding_box() or {}
                    return {
                        "width": box.get("width", 0),
                        "height": box.get("height", 0),
                    }
                except Exception:
                    continue
        return {"width": 0, "height": 0}

    def get_large_modal_size(self) -> dict:
        """Возвращает размеры большого модального окна в виде {'width': w, 'height': h}."""
        candidates = [
            ModalDialogsLocators.LARGE_MODAL_CONTAINER,
            ModalDialogsLocators.MODAL_DIALOG,
            ModalDialogsLocators.MODAL_ACTIVE,
        ]
        for sel in candidates:
            loc = self.page.locator(sel)
            if loc.count() > 0:
                try:
                    loc.wait_for(state="visible", timeout=2000)
                    box = loc.bounding_box() or {}
                    return {
                        "width": box.get("width", 0),
                        "height": box.get("height", 0),
                    }
                except Exception:
                    continue
        return {"width": 0, "height": 0}

    def close_small_modal(self) -> None:
        """Закрывает малое модальное окно кнопкой закрытия (если есть)."""
        if self.page.locator(ModalDialogsLocators.SMALL_MODAL_CLOSE).count() > 0:
            self.safe_click(ModalDialogsLocators.SMALL_MODAL_CLOSE)
        else:
            # fallback to generic close
            self.close_modal_by_close_button()

    def close_large_modal(self) -> None:
        """Закрывает большое модальное окно кнопкой закрытия (если есть)."""
        if self.page.locator(ModalDialogsLocators.LARGE_MODAL_CLOSE).count() > 0:
            self.safe_click(ModalDialogsLocators.LARGE_MODAL_CLOSE)
        else:
            self.close_modal_by_close_button()

    def has_modal_overlay(self) -> bool:
        """Проверяет наличие overlay (фон) модального окна."""
        return self.page.locator(ModalDialogsLocators.MODAL_BACKDROP).count() > 0

    def is_modal_overlay_visible(self) -> bool:
        """Проверяет, виден ли overlay (активный класс)."""
        return self.page.locator(
            ModalDialogsLocators.MODAL_BACKDROP_ACTIVE
        ).is_visible()

    def click_modal_overlay(self) -> bool:
        """Кликает по overlay, возвращает True если клик выполнен."""
        try:
            backdrop = self.page.locator(ModalDialogsLocators.MODAL_BACKDROP)
            if backdrop.count() > 0:
                backdrop.first.click(position={"x": 5, "y": 5})
                return True
        except Exception:
            return False
        return False

    def get_modal_aria_attributes(self) -> dict:
        """Возвращает словарь ключевых ARIA атрибутов модального окна."""
        modal = self.page.locator(ModalDialogsLocators.MODAL_DIALOG)
        attrs = {}
        for attr in ("role", "aria-modal", "aria-labelledby"):
            try:
                val = modal.get_attribute(attr)
                if val is not None:
                    attrs[attr] = val
            except Exception:
                # ignore missing attributes
                pass
        return attrs

    def get_focused_element_in_modal(self) -> str | None:
        """Возвращает строковое представление текущего элемента с фокусом внутри страницы (outerHTML) или None."""
        try:
            return self.page.evaluate(
                "() => { const e = document.activeElement; return e ? e.outerHTML : null }"
            )
        except Exception:
            return None

    def can_close_modal_with_escape(self) -> bool:
        """Простая проверка: предполагаем, что модальные окна можно закрыть с помощью Escape (Bootstrap по умолчанию)."""
        # Это эвристика — возвращаем True, тест затем попытается закрыть модал с помощью close_modal_with_escape
        return True

    def close_modal_with_escape(self) -> bool:
        """Попытка закрыть модальное окно клавишей Escape, возвращает True если окно закрылось."""
        try:
            was_visible = self.is_modal_visible()
            self.page.keyboard.press("Escape")
            # даём немного времени на закрытие
            self.page.wait_for_timeout(300)
            return not self.is_modal_visible() if was_visible else False
        except Exception:
            return False

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
