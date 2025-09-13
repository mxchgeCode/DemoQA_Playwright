import time
from pages.base_page import BasePage
from locators.progress_bar_locators import ProgressBarLocators


class ProgressBarPage(BasePage):

    def _wait_for_enabled(self, locator, timeout=5000):
        """Ждёт, пока элемент станет enabled"""
        start_time = time.time()
        while True:
            if locator.is_enabled():
                return
            if time.time() - start_time > timeout / 1000:
                raise TimeoutError(f"Элемент не стал enabled за {timeout} мс")
            self.page.wait_for_timeout(100)

    def start_progress(self, retries=3):
        for attempt in range(retries):
            try:
                button = self.page.locator(ProgressBarLocators.START_STOP_BUTTON)
                button.wait_for(state="visible", timeout=10000)
                self._wait_for_enabled(button, timeout=5000)
                button.click()
                return
            except Exception as e:
                if attempt == retries - 1:
                    raise Exception(
                        f"Не удалось нажать Start после {retries} попыток"
                    ) from e
                self.page.wait_for_timeout(1000)

    def stop_progress(self, retries=3):
        for attempt in range(retries):
            try:
                button = self.page.locator(ProgressBarLocators.START_STOP_BUTTON)
                button.wait_for(state="visible", timeout=10000)
                self._wait_for_enabled(button, timeout=5000)
                button.click()
                return
            except Exception as e:
                if attempt == retries - 1:
                    raise Exception(
                        f"Не удалось нажать Stop после {retries} попыток"
                    ) from e
                self.page.wait_for_timeout(1000)

    def reset_progress(self, retries=3):
        """Сбрасывает прогресс."""
        # --- ВАЖНО: Убедитесь, что ProgressBarLocators.RESET_BUTTON определен и указывает на правильную кнопку ---
        # Если такой локатор отсутствует, нужно его добавить в locators/progress_bar_locators.py
        # Например: RESET_BUTTON = "#resetButton" (если у кнопки есть уникальный ID)
        # ИЛИ, если это та же кнопка, что и Start/Stop, но с другим текстом, логика должна быть сложнее.

        # Предположим, у нас есть отдельная кнопка Reset:
        from locators.progress_bar_locators import ProgressBarLocators

        # Проверим, определен ли локатор
        if not hasattr(ProgressBarLocators, "RESET_BUTTON"):
            print(
                "? Локатор RESET_BUTTON не найден в locators/progress_bar_locators.py. Используется Start/Stop."
            )
            # В этом случае логика сброса может быть другой, например, просто клик по Start/Stop, если он в режиме "Stop"
            # Или тест должен проверять текст кнопки.
            # Для простоты, предположим, что RESET_BUTTON должен существовать.
            raise NotImplementedError(
                "Локатор RESET_BUTTON должен быть определен в ProgressBarLocators"
            )

        for attempt in range(retries):
            try:
                button = self.page.locator(ProgressBarLocators.RESET_BUTTON)
                button.wait_for(state="visible", timeout=10000)
                self._wait_for_enabled(button, timeout=5000)
                button.click()
                print("✓ Кнопка Reset нажата")
                return
            except Exception as e:
                if attempt == retries - 1:
                    raise Exception(
                        f"Не удалось нажать Reset после {retries} попыток: {e}"
                    ) from e
                self.page.wait_for_timeout(1000)
        print("? Не удалось нажать Reset")

    def get_progress_value(self) -> str:
        progress_bar = self.page.locator(ProgressBarLocators.PROGRESS_BAR)
        progress_bar.wait_for(state="visible", timeout=10000)
        return progress_bar.inner_text().strip()

    def get_button_text(self) -> str:
        button = self.page.locator(ProgressBarLocators.START_STOP_BUTTON)
        button.wait_for(state="visible", timeout=10000)
        return button.inner_text().strip()
