"""
Локаторы для страницы Select Menu.
Содержит селекторы для различных типов выпадающих меню и мультиселектов.
"""


class SelectMenuLocators:
    """CSS селекторы для элементов страницы Select Menu."""

    # === ОСНОВНЫЕ КОНТЕЙНЕРЫ ===
    MAIN_CONTAINER = "#app"                           # Основной контейнер приложения
    CONTAINER = "#withOptGroup"                       # Контейнер с группированными опциями

    # === SELECT VALUE (Первый dropdown) ===
    SELECT_VALUE_CONTAINER = "#selectOne"             # Контейнер Select Value
    SELECT_VALUE_CONTROL = "#selectOne .css-yk16xz-control" # Контрол Select Value
    SELECT_VALUE_PLACEHOLDER = "#selectOne .css-1wa3eu0-placeholder" # Плейсхолдер
    SELECT_VALUE_SINGLE_VALUE = "#selectOne .css-1uccc91-singleValue" # Выбранное значение

    # === SELECT ONE (Второй dropdown) ===
    SELECT_ONE_CONTAINER = "#selectOne"               # Контейнер Select One
    SELECT_ONE_CONTROL = ".css-yk16xz-control"        # Контрол выпадающего меню
    SELECT_ONE_DISPLAY_TEXT = ".css-1hwfws3"          # Отображаемый текст выбора

    # === OLD STYLE SELECT (Стандартный HTML select) ===
    OLD_STYLE_SELECT = "#oldSelectMenu"               # Стандартный HTML select
    SELECT_VALUE = "#oldSelectMenu"                   # Алиас для старого селекта

    # === MULTISELECT (Множественный выбор) ===
    MULTISELECT = "#cars"                             # Стандартный HTML multiselect
    MULTISELECT_CONTROL = "div.css-yk16xz-control"    # Контрол мультиселекта

    # === DROPDOWN МЕНЮ ===
    DROPDOWN_MENU = ".css-26l3qy-menu"                # Выпадающее меню
    DROPDOWN_OPTIONS = ".css-yt9ioa-option"           # Опции в dropdown
    DROPDOWN_CONTROL = ".css-yk16xz-control"          # Контрол dropdown
    DROPDOWN_VALUE = "div.css-1hwfws3"                # Значение в dropdown
    DROPDOWN_INDICATOR = ".css-1wy0on6"               # Индикатор dropdown

    # === ВЫБРАННЫЕ ЗНАЧЕНИЯ ===
    SELECTED_TAG = ".css-1rhbuit-multiValue"          # Тег выбранного значения
    SELECTED_TAG_TEXT = ".css-12jo7m5"                # Текст выбранного тега
    SELECTED_TAG_REMOVE = ".css-1wy0on6"              # Кнопка удаления тега

    # === ЭЛЕМЕНТЫ УПРАВЛЕНИЯ ===
    CLOSE_BUTTON = "div.css-xb97g8"                   # Кнопка закрытия/очистки
    PLACEHOLDER = "div.css-1wa3eu0-placeholder"       # Плейсхолдер
    CLEAR_INDICATOR = ".css-1wy0on6"                  # Индикатор очистки
    DROPDOWN_INDICATOR_ARROW = ".css-1xc3v61-indicatorSeparator" # Стрелка dropdown

    # === ГРУППИРОВАННЫЕ ОПЦИИ ===
    OPTION_GROUP_HEADER = ".css-1n7v3ny-group"       # Заголовок группы опций
    OPTION_GROUP_OPTIONS = ".css-1n7v3ny-option"     # Опции в группе

    # === СОСТОЯНИЯ ===
    FOCUSED_CONTROL = ".css-1pahdxg-control"          # Сфокусированный контрол
    DISABLED_CONTROL = ".css-1s2u09g-control"         # Отключенный контрол
    ERROR_CONTROL = ".css-1hwfws3.error"              # Контрол с ошибкой

    # === ПОИСК И ФИЛЬТРАЦИЯ ===
    SEARCH_INPUT = "input[role='combobox']"           # Поле поиска в dropdown
    NO_OPTIONS_MESSAGE = ".css-1gl4k7y"               # Сообщение об отсутствии опций
    LOADING_MESSAGE = ".css-1nmdiq5-loadingMessage"   # Сообщение загрузки
