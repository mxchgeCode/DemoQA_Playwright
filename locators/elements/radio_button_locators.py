"""
Локаторы для страницы Radio Button.
Содержит селекторы для радио кнопок с различными состояниями.
"""


class RadioButtonLocators:
    """CSS селекторы для элементов страницы Radio Button."""

    # === РАДИО КНОПКИ (labels для клика) ===
    YES_RADIO = "label[for='yesRadio']"               # Радио кнопка Yes (активна)
    IMPRESSIVE_RADIO = "label[for='impressiveRadio']" # Радио кнопка Impressive (активна)
    NO_RADIO = "label[for='noRadio']"                 # Радио кнопка No (отключена)

    # === РАДИО КНОПКИ (input элементы) ===
    YES_RADIO_INPUT = "#yesRadio"                     # Input элемент Yes
    IMPRESSIVE_RADIO_INPUT = "#impressiveRadio"       # Input элемент Impressive
    NO_RADIO_INPUT = "#noRadio"                       # Input элемент No

    # === РЕЗУЛЬТАТ ВЫБОРА ===
    RESULT_TEXT = "span.text-success"                 # Отображение выбранного значения

    # === СОСТОЯНИЯ КНОПОК ===
    CHECKED_RADIO = "input[type='radio']:checked"     # Выбранная радио кнопка
    DISABLED_RADIO = "input[type='radio']:disabled"   # Отключенная радио кнопка
    ENABLED_RADIO = "input[type='radio']:not(:disabled)" # Активная радио кнопка

    # === ГРУППЫ РАДИО КНОПОК ===
    RADIO_GROUP = ".custom-radio"                     # Группа радио кнопок
    ALL_RADIO_BUTTONS = "input[type='radio']"         # Все радио кнопки
    ALL_RADIO_LABELS = "label.custom-control-label"   # Все лейблы радио кнопок

    # === КОНТЕЙНЕРЫ ===
    RADIO_CONTAINER = ".radio-button-wrapper"         # Основной контейнер
    RESULT_CONTAINER = ".radio-result"                # Контейнер результата

    # === ДОПОЛНИТЕЛЬНЫЕ СЕЛЕКТОРЫ ===
    RADIO_TEXT = ".custom-control-label"              # Текст рядом с радио кнопкой
    RADIO_INDICATOR = ".custom-control-indicator"     # Визуальный индикатор

    # === СЕЛЕКТОРЫ ПО ЗНАЧЕНИЮ ===
    YES_VALUE_RADIO = "input[value='Yes']"            # Радио кнопка со значением Yes
    IMPRESSIVE_VALUE_RADIO = "input[value='Impressive']" # Радио кнопка со значением Impressive
    NO_VALUE_RADIO = "input[value='No']"              # Радио кнопка со значением No
