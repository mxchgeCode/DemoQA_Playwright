"""
Локаторы для страницы Dynamic Properties.
Содержит селекторы для элементов с динамически изменяющимися свойствами.
"""


class DynamicPropertiesLocators:
    """CSS селекторы для элементов страницы Dynamic Properties."""

    # === ДИНАМИЧЕСКИЕ КНОПКИ ===
    ENABLE_AFTER_BUTTON = "#enableAfter"              # Кнопка, активируемая через 5 секунд
    COLOR_CHANGE_BUTTON = "#colorChange"              # Кнопка с изменяющимся цветом
    VISIBLE_AFTER_BUTTON = "#visibleAfter"            # Кнопка, появляющаяся через 5 секунд

    # === СТАТИЧЕСКИЕ ЭЛЕМЕНТЫ ===
    STATIC_TEXT = ".static-text"                      # Статический текст для сравнения
    DYNAMIC_TEXT = ".dynamic-text"                    # Динамически изменяющийся текст

    # === СОСТОЯНИЯ ЭЛЕМЕНТОВ ===
    DISABLED_STATE = "[disabled]"                     # Селектор для отключенных элементов
    ENABLED_STATE = ":not([disabled])"                # Селектор для активных элементов
    VISIBLE_STATE = ":visible"                        # Селектор для видимых элементов
    HIDDEN_STATE = ":hidden"                          # Селектор для скрытых элементов

    # === ЦВЕТОВЫЕ КЛАССЫ ===
    DEFAULT_COLOR_CLASS = ".btn-primary"              # Класс цвета по умолчанию
    CHANGED_COLOR_CLASS = ".btn-danger"               # Класс измененного цвета

    # === КОНТЕЙНЕРЫ ===
    PROPERTIES_CONTAINER = ".dynamic-properties"      # Основной контейнер страницы
    BUTTONS_ROW = ".row"                              # Строка с кнопками

    # === TIMING SELECTORS (для ожидания изменений) ===
    TIMER_5_SEC = "[data-timer='5000']"               # Элементы с 5-секундной задержкой
    TIMER_3_SEC = "[data-timer='3000']"               # Элементы с 3-секундной задержкой
