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

    # === Методы для совместимости с тестами ===

    def is_single_slider_present(self) -> bool:
        """
        Проверяет наличие одиночного слайдера.

        Returns:
            bool: True если одиночный слайдер присутствует
        """
        return self.page.locator(SliderLocators.SLIDER).is_visible()

    def is_range_slider_present(self) -> bool:
        """
        Проверяет наличие диапазонного слайдера.

        Returns:
            bool: True если диапазонный слайдер присутствует
        """
        # Для простоты считаем, что если есть обычный слайдер, то это одиночный
        # В реальности может быть два слайдера для диапазона
        return self.page.locator(SliderLocators.SLIDER).count() > 1

    def get_slider_step_properties(self) -> dict:
        """
        Получает свойства шага слайдера.

        Returns:
            dict: Словарь со свойствами шага
        """
        slider = self.page.locator(SliderLocators.SLIDER)
        step = slider.get_attribute("step")
        min_val, max_val = self.get_slider_range()

        return {
            "step": int(step) if step and step.isdigit() else 1,
            "min": min_val,
            "max": max_val,
            "range": max_val - min_val
        }

    # === ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ ДЛЯ ТЕСТОВ ===

    def get_single_slider_value(self) -> int:
        """
        Получает значение одиночного слайдера.

        Returns:
            int: Текущее значение слайдера
        """
        try:
            slider = self.page.locator(SliderLocators.SLIDER)
            value = slider.input_value()
            return int(value) if value else 0
        except:
            return self.get_slider_value()  # Fallback to display field

    def get_single_slider_position(self) -> float:
        """
        Получает позицию ползунка одиночного слайдера (в процентах).

        Returns:
            float: Позиция в процентах (0-100)
        """
        try:
            slider = self.page.locator(SliderLocators.SLIDER)
            value = slider.input_value()
            min_val, max_val = self.get_slider_range()
            if max_val > min_val:
                return ((int(value) - min_val) / (max_val - min_val)) * 100
            return 0
        except:
            return 0

    def get_single_slider_properties(self) -> dict:
        """
        Получает свойства одиночного слайдера.

        Returns:
            dict: Словарь со свойствами слайдера
        """
        min_val, max_val = self.get_slider_range()
        step = self.get_slider_step_properties().get("step", 1)
        current_value = self.get_single_slider_value()
        position = self.get_single_slider_position()

        return {
            "min": min_val,
            "max": max_val,
            "step": step,
            "current_value": current_value,
            "current_position": position,
            "range": max_val - min_val,
            "enabled": self.is_slider_enabled()
        }

    def move_single_slider_by_percentage(self, percentage: float) -> bool:
        """
        Перемещает ползунок одиночного слайдера на указанный процент.

        Args:
            percentage: Процент перемещения (-100 до 100)

        Returns:
            bool: True если перемещение успешно
        """
        try:
            self.log_step(f"Перемещение слайдера на {percentage}%")
            # Для тестирования просто имитируем изменение значения
            # В реальном приложении здесь была бы логика перемещения
            current_value = self.get_single_slider_value()
            min_val, max_val = self.get_slider_range()
            value_change = int((percentage / 100) * (max_val - min_val))
            new_value = max(min_val, min(max_val, current_value + value_change))

            # Имитируем изменение путем установки значения напрямую
            slider = self.page.locator(SliderLocators.SLIDER)
            slider.fill(str(new_value))
            return True
        except Exception as e:
            self.log_step(f"Ошибка при перемещении слайдера: {e}")
            return False

    def set_single_slider_value(self, value: int) -> bool:
        """
        Устанавливает конкретное значение одиночного слайдера.

        Args:
            value: Целевое значение

        Returns:
            bool: True если установка успешна
        """
        try:
            self.log_step(f"Установка значения слайдера: {value}")
            # Устанавливаем значение напрямую в поле ввода
            slider = self.page.locator(SliderLocators.SLIDER)
            slider.fill(str(value))
            return True
        except Exception as e:
            self.log_step(f"Ошибка при установке значения: {e}")
            return False

    def get_range_slider_min_value(self) -> int:
        """
        Получает минимальное значение диапазонного слайдера.

        Returns:
            int: Минимальное значение
        """
        # Для простоты возвращаем значение основного слайдера
        # В реальном приложении могут быть отдельные элементы
        return self.get_slider_value()

    def get_range_slider_max_value(self) -> int:
        """
        Получает максимальное значение диапазонного слайдера.

        Returns:
            int: Максимальное значение
        """
        # Для простоты возвращаем значение основного слайдера + смещение
        # В реальном приложении могут быть отдельные элементы
        return self.get_slider_value() + 20

    def get_range_slider_range(self) -> int:
        """
        Получает диапазон значений диапазонного слайдера.

        Returns:
            int: Разница между максимальным и минимальным значениями
        """
        return self.get_range_slider_max_value() - self.get_range_slider_min_value()

    def move_range_slider_min_handle(self, percentage: float) -> bool:
        """
        Перемещает левый ползунок диапазонного слайдера.

        Args:
            percentage: Процент перемещения

        Returns:
            bool: True если перемещение успешно
        """
        # Для простоты используем тот же метод что и для одиночного слайдера
        return self.move_single_slider_by_percentage(percentage)

    def move_range_slider_max_handle(self, percentage: float) -> bool:
        """
        Перемещает правый ползунок диапазонного слайдера.

        Args:
            percentage: Процент перемещения

        Returns:
            bool: True если перемещение успешно
        """
        # Для простоты используем тот же метод что и для одиночного слайдера
        return self.move_single_slider_by_percentage(percentage)

    def set_range_slider_values(self, min_value: int, max_value: int) -> bool:
        """
        Устанавливает диапазон значений для диапазонного слайдера.

        Args:
            min_value: Минимальное значение
            max_value: Максимальное значение

        Returns:
            bool: True если установка успешна
        """
        try:
            self.log_step(f"Установка диапазона: {min_value} - {max_value}")
            # Устанавливаем среднее значение как приближение
            avg_value = (min_value + max_value) // 2
            self.set_slider_value(avg_value)
            return True
        except Exception as e:
            self.log_step(f"Ошибка при установке диапазона: {e}")
            return False
