"""
Page Object для страницы Slider.
Содержит методы для работы с ползунком (slider) и получения его значений.
"""

from playwright.sync_api import Page
from locators.widgets.slider_locators import SliderLocators
from pages.base_page import BasePage


class SliderPage(BasePage):
    """
    Страница тестирования slider элемента.
    Позволяет перемещать ползунок и получать его текущее значение.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Slider.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def set_slider_value(self, target_value: int) -> None:
        """
        Устанавливает значение слайдера путем перемещения ползунка.

        Args:
            target_value: Целевое значение слайдера (0-100)

        Postconditions: слайдер установлен на указанное значение
        """
        self.log_step(f"Устанавливаем значение слайдера: {target_value}")

        # Получаем элементы
        slider = self.page.locator(SliderLocators.SLIDER)
        thumb = self.page.locator(SliderLocators.SLIDER_THUMB)

        # Получаем размеры слайдера
        slider_box = slider.bounding_box()
        slider_width = slider_box["width"]

        # Вычисляем позицию для целевого значения (0-100)
        target_percentage = target_value / 100
        target_x = slider_box["x"] + (slider_width * target_percentage)
        target_y = slider_box["y"] + slider_box["height"] / 2

        # Перемещаем ползунок
        thumb_box = thumb.bounding_box()
        current_x = thumb_box["x"] + thumb_box["width"] / 2
        current_y = thumb_box["y"] + thumb_box["height"] / 2

        self.page.mouse.move(current_x, current_y)
        self.page.mouse.down()
        self.page.mouse.move(target_x, target_y, steps=10)
        self.page.mouse.up()

    def drag_slider_by_offset(self, x_offset: int) -> None:
        """
        Перемещает ползунок на указанное смещение.

        Args:
            x_offset: Смещение в пикселях (положительное - вправо, отрицательное - влево)

        Postconditions: ползунок смещен на указанное количество пикселей
        """
        self.log_step(f"Перемещаем слайдер на смещение: {x_offset}px")
        thumb = self.page.locator(SliderLocators.SLIDER_THUMB)

        thumb_box = thumb.bounding_box()
        start_x = thumb_box["x"] + thumb_box["width"] / 2
        start_y = thumb_box["y"] + thumb_box["height"] / 2

        self.page.mouse.move(start_x, start_y)
        self.page.mouse.down()
        self.page.mouse.move(start_x + x_offset, start_y, steps=5)
        self.page.mouse.up()

    def get_slider_value(self) -> int:
        """
        Получает текущее значение слайдера из поля отображения.

        Returns:
            int: Текущее значение слайдера (0-100)
        """
        value_text = self.get_text_safe(SliderLocators.SLIDER_VALUE)
        try:
            return int(value_text.strip())
        except (ValueError, AttributeError):
            return 0

    def get_slider_attribute_value(self) -> int:
        """
        Получает значение слайдера из атрибута aria-valuenow.

        Returns:
            int: Значение из атрибута или 0 при ошибке
        """
        slider = self.page.locator(SliderLocators.SLIDER)
        value = slider.get_attribute("aria-valuenow")
        try:
            return int(value) if value else 0
        except ValueError:
            return 0

    def is_slider_enabled(self) -> bool:
        """
        Проверяет, активен ли слайдер для взаимодействия.

        Returns:
            bool: True если слайдер активен
        """
        slider = self.page.locator(SliderLocators.SLIDER)
        return slider.is_enabled()

    def get_slider_range(self) -> tuple[int, int]:
        """
        Получает диапазон значений слайдера из атрибутов.

        Returns:
            tuple: (минимальное_значение, максимальное_значение)
        """
        slider = self.page.locator(SliderLocators.SLIDER)
        min_val = slider.get_attribute("aria-valuemin")
        max_val = slider.get_attribute("aria-valuemax")

        try:
            return int(min_val or "0"), int(max_val or "100")
        except ValueError:
            return 0, 100
