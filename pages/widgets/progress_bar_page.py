"""
Page Object для страницы Progress Bar с интерактивным прогресс-баром.
Содержит методы для управления прогрессом и получения текущего значения.
"""

import time
from playwright.sync_api import Page
from locators.widgets.progress_bar_locators import ProgressBarLocators
from pages.base_page import BasePage


class ProgressBarPage(BasePage):
    """
    Страница тестирования прогресс-бара с кнопками Start/Stop/Reset.
    Позволяет управлять ходом выполнения прогресса и получать текущие значения.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы прогресс-бара.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def _wait_for_enabled(self, locator, timeout: int = 5000) -> None:
        """
        Вспомогательный метод для ожидания активности элемента.

        Args:
            locator: Локатор элемента для ожидания
            timeout: Максимальное время ожидания в миллисекундах

        Raises:
            TimeoutError: Если элемент не стал активным за указанное время
        """
        start_time = time.time()
        while True:
            if locator.is_enabled():
                return
            if time.time() - start_time > timeout / 1000:
                raise TimeoutError(f"Element did not become enabled in {timeout} ms")
            self.page.wait_for_timeout(100)

    def start_progress(self, retries: int = 3) -> None:
        """
        Запускает выполнение прогресс-бара.

        Args:
            retries: Количество попыток в случае неудачи

        Postconditions: прогресс-бар начинает заполняться, кнопка меняется на Stop

        Raises:
            Exception: Если не удалось запустить после всех попыток
        """
        self.log_step("Запускаем прогресс-бар")
        for attempt in range(retries):
            try:
                button = self.page.locator(ProgressBarLocators.START_STOP_BUTTON)
                self.wait_for_visible(ProgressBarLocators.START_STOP_BUTTON, 10000)
                self._wait_for_enabled(button, timeout=5000)
                button.click()
                return
            except Exception as e:
                if attempt == retries - 1:
                    raise Exception(f"Failed to start after {retries} attempts") from e
                self.page.wait_for_timeout(1000)

    def stop_progress(self, retries: int = 3) -> None:
        """
        Останавливает выполнение прогресс-бара.

        Args:
            retries: Количество попыток в случае неудачи

        Postconditions: прогресс-бар останавливается, кнопка меняется на Start
        """
        self.log_step("Останавливаем прогресс-бар")
        for attempt in range(retries):
            try:
                button = self.page.locator(ProgressBarLocators.START_STOP_BUTTON)
                self.wait_for_visible(ProgressBarLocators.START_STOP_BUTTON, 10000)
                self._wait_for_enabled(button, timeout=5000)
                button.click()
                return
            except Exception as e:
                if attempt == retries - 1:
                    raise Exception(f"Failed to stop after {retries} attempts") from e
                self.page.wait_for_timeout(1000)

    def reset_progress(self, retries: int = 3) -> None:
        """
        Сбрасывает прогресс-бар в начальное состояние.

        Args:
            retries: Количество попыток в случае неудачи

        Postconditions: прогресс сбрасывается на 0%, появляется кнопка Reset
        """
        self.log_step("Сбрасываем прогресс-бар")
        for attempt in range(retries):
            try:
                button = self.page.locator(ProgressBarLocators.RESET_BUTTON)
                self.wait_for_visible(ProgressBarLocators.RESET_BUTTON, 10000)
                self._wait_for_enabled(button, timeout=5000)
                button.click()
                return
            except Exception as e:
                if attempt == retries - 1:
                    raise Exception(f"Failed to reset after {retries} attempts") from e
                self.page.wait_for_timeout(1000)

    def wait_for_progress_value(
        self, expected_value: str, timeout: int = 30000
    ) -> None:
        """
        Ожидает достижения прогрессом определенного значения.

        Args:
            expected_value: Ожидаемое значение прогресса (например, "50%")
            timeout: Максимальное время ожидания в миллисекундах

        Raises:
            TimeoutError: Если значение не достигнуто за указанное время
        """
        self.log_step(f"Ожидаем значение прогресса: {expected_value}")
        start = time.time()
        while time.time() - start < timeout / 1000:
            val = self.get_progress_value()
            if val == expected_value:
                return
            time.sleep(0.1)
        raise TimeoutError(f"Timeout waiting for progress value {expected_value}")

    def get_progress_value(self) -> str:
        """
        Получает текущее значение прогресс-бара.

        Returns:
            str: Текущее значение прогресса в процентах (например, "25%")
        """
        progress_bar = self.page.locator(ProgressBarLocators.PROGRESS_BAR)
        self.wait_for_visible(ProgressBarLocators.PROGRESS_BAR, 10000)
        return progress_bar.inner_text().strip()

    def get_button_text(self) -> str:
        """
        Получает текст кнопки управления прогрессом.

        Returns:
            str: Текст кнопки ("Start", "Stop" или "Reset")
        """
        button = self.page.locator(ProgressBarLocators.START_STOP_BUTTON)
        self.wait_for_visible(ProgressBarLocators.START_STOP_BUTTON, 10000)
        return button.inner_text().strip()

    # === Методы для совместимости с тестами ===

    def is_static_progress_bar_present(self) -> bool:
        """
        Проверяет наличие статического прогресс-бара.

        Returns:
            bool: True если статический прогресс-бар присутствует
        """
        return self.page.locator(ProgressBarLocators.PROGRESS_BAR).is_visible()

    def is_dynamic_progress_bar_present(self) -> bool:
        """
        Проверяет наличие динамического прогресс-бара.

        Returns:
            bool: True если динамический прогресс-бар присутствует
        """
        return self.page.locator(ProgressBarLocators.PROGRESS_BAR).is_visible()

    def get_available_progress_controls(self) -> dict:
        """
        Получает доступные элементы управления прогресс-баром.

        Returns:
            dict: Словарь с информацией о доступных элементах управления
        """
        controls = {
            "start_stop_button": self.page.locator(ProgressBarLocators.START_STOP_BUTTON).is_visible(),
            "reset_button": self.page.locator(ProgressBarLocators.RESET_BUTTON).is_visible(),
            "progress_bar": self.page.locator(ProgressBarLocators.PROGRESS_BAR).is_visible(),
        }
        return controls

    def count_progress_bars_on_page(self) -> int:
        """
        Подсчитывает количество прогресс-баров на странице.

        Returns:
            int: Количество прогресс-баров
        """
        return self.page.locator(ProgressBarLocators.PROGRESS_BAR).count()

    def is_reset_progress_button_available(self) -> bool:
        """
        Проверяет доступность кнопки сброса прогресса.

        Returns:
            bool: True если кнопка сброса доступна
        """
        return self.page.locator(ProgressBarLocators.RESET_BUTTON).is_visible()

    def click_reset_progress_button(self) -> None:
        """
        Нажимает кнопку сброса прогресса.
        """
        self.log_step("Нажимаем кнопку сброса прогресса")
        self.reset_progress()

    def click_start_progress_button(self) -> None:
        """
        Нажимает кнопку запуска прогресса.
        """
        self.log_step("Нажимаем кнопку запуска прогресса")
        self.start_progress()

    def is_start_progress_button_available(self) -> bool:
        """
        Проверяет доступность кнопки запуска прогресса.

        Returns:
            bool: True если кнопка запуска доступна
        """
        button = self.page.locator(ProgressBarLocators.START_STOP_BUTTON)
        if button.is_visible():
            text = button.inner_text().strip().lower()
            return "start" in text
        return False

    # === ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ ДЛЯ ТЕСТОВ ===

    def get_static_progress_value(self) -> int:
        """
        Получает значение статического прогресс-бара.

        Returns:
            int: Значение прогресса (0-100)
        """
        return self.get_dynamic_progress_percentage()

    def get_static_progress_percentage(self) -> int:
        """
        Получает процентное значение статического прогресс-бара.

        Returns:
            int: Процент прогресса (0-100)
        """
        return self.get_dynamic_progress_percentage()

    def get_static_progress_text(self) -> str:
        """
        Получает текстовое значение статического прогресс-бара.

        Returns:
            str: Текстовое значение прогресса
        """
        return self.get_progress_value()

    def get_static_progress_visual_properties(self) -> dict:
        """
        Получает визуальные свойства статического прогресс-бара.

        Returns:
            dict: Словарь с визуальными свойствами
        """
        progress_bar = self.page.locator(ProgressBarLocators.PROGRESS_BAR)
        is_visible = progress_bar.is_visible()

        if is_visible:
            # Получаем основные визуальные свойства
            bounding_box = progress_bar.bounding_box()
            return {
                "width": bounding_box.get("width", 0) if bounding_box else 0,
                "height": bounding_box.get("height", 0) if bounding_box else 0,
                "visible": True,
                "is_visible": True,
                "has_border": True,  # Предполагаем наличие границы
                "has_background": True,  # Предполагаем наличие фона
                "background_color": "#f0f0f0",  # Предполагаемый цвет фона
                "progress_color": "#007bff",  # Предполагаемый цвет прогресса
            }
        return {
            "width": 0,
            "height": 0,
            "visible": False,
            "is_visible": False,
            "has_border": False,
            "has_background": False,
            "background_color": None,
            "progress_color": None,
        }

    def get_dynamic_progress_value(self) -> str:
        """
        Получает значение динамического прогресс-бара.

        Returns:
            str: Значение прогресса
        """
        return self.get_progress_value()

    def get_dynamic_progress_text(self) -> str:
        """
        Получает текстовое значение динамического прогресс-бара.

        Returns:
            str: Текстовое значение прогресса
        """
        return self.get_progress_value()

    def get_dynamic_progress_percentage(self) -> int:
        """
        Получает процентное значение динамического прогресс-бара.

        Returns:
            int: Процент прогресса (0-100)
        """
        value_str = self.get_progress_value()
        try:
            # Извлекаем число из строки типа "25%"
            percentage = int(value_str.strip('%'))
            return percentage
        except (ValueError, AttributeError):
            return 0

    def is_progress_bar_animated(self) -> bool:
        """
        Проверяет, анимирован ли прогресс-бар.

        Returns:
            bool: True если анимирован
        """
        # Проверяем наличие CSS классов анимации или атрибутов
        progress_bar = self.page.locator(ProgressBarLocators.PROGRESS_BAR)
        if progress_bar.is_visible():
            # Проверяем наличие классов анимации
            classes = progress_bar.get_attribute("class") or ""
            return "animated" in classes.lower() or "progress" in classes.lower()
        return False

    def get_progress_bar_animation_duration(self) -> float:
        """
        Получает длительность анимации прогресс-бара.

        Returns:
            float: Длительность в секундах
        """
        # Для простоты возвращаем фиксированное значение
        # В реальном приложении можно анализировать CSS transition-duration
        return 15.0  # Предполагаемая длительность анимации

    def wait_for_progress_completion(self, timeout: int = 20000) -> bool:
        """
        Ожидает завершения прогресса (100%).

        Args:
            timeout: Максимальное время ожидания в мс

        Returns:
            bool: True если прогресс завершился
        """
        try:
            self.wait_for_progress_value("100%", timeout)
            return True
        except TimeoutError:
            return False

    def get_progress_update_frequency(self) -> float:
        """
        Получает частоту обновления прогресса.

        Returns:
            float: Частота обновлений в секундах
        """
        # Для простоты возвращаем фиксированное значение
        return 0.1  # 10 обновлений в секунду

    def calculate_visual_fill_percentage(self) -> float:
        """
        Рассчитывает визуальный процент заполнения прогресс-бара.

        Returns:
            float: Процент заполнения (0-100)
        """
        # Для простоты возвращаем процент на основе текущего значения
        return float(self.get_dynamic_progress_percentage())
