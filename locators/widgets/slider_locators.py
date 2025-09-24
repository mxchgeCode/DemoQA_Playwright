"""
Локаторы для страницы Slider.
Содержит селекторы для элементов управления ползунком диапазона значений.
"""


class SliderLocators:
    """CSS селекторы для элементов страницы Slider."""

    # === ОСНОВНОЙ ПОЛЗУНОК ===
    SLIDER = "input[type='range']"  # Основной слайдер (input range)
    SLIDER_HANDLE = ".range-slider"  # Основной ползунок (input range)
    SLIDER_INPUT = "input[type='range']"  # Input элемент ползунка

    # === ОТОБРАЖЕНИЕ ЗНАЧЕНИЯ ===
    SLIDER_VALUE = "#sliderValue"  # Поле отображения текущего значения
    VALUE_INPUT = "input#sliderValue"  # Input для ввода конкретного значения

    # === КОНТЕЙНЕРЫ И ОБЕРТКИ ===
    SLIDER_CONTAINER = ".range-slider-container"  # Контейнер ползунка
    SLIDER_WRAPPER = ".slider-container"  # Обертка всего компонента

    # === ТРЕК И ДОРОЖКА ПОЛЗУНКА ===
    SLIDER_TRACK = ".range-slider__track"  # Дорожка ползунка
    SLIDER_THUMB = ".range-slider__thumb"  # Ручка ползунка
    SLIDER_RAIL = ".range-slider__rail"  # Рельс ползунка

    # === АТРИБУТЫ И СВОЙСТВА ===
    SLIDER_MIN_VALUE = "[min]"  # Минимальное значение
    SLIDER_MAX_VALUE = "[max]"  # Максимальное значение
    SLIDER_STEP = "[step]"  # Шаг изменения значения
    SLIDER_CURRENT_VALUE = "[value]"  # Текущее значение

    # === АЛЬТЕРНАТИВНЫЕ СЕЛЕКТОРЫ ===
    RANGE_INPUT_ALT = "input.range-slider"  # Альтернативный селектор ползунка
    VALUE_DISPLAY_ALT = "#sliderValue"  # Альтернативный селектор значения
