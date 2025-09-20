"""
Локаторы для страницы Auto Complete.
Содержит селекторы для полей автодополнения с различными конфигурациями:
- Одиночное автодополнение
- Множественное автодополнение
- Выпадающие списки с поиском
- Предложения и фильтрация
"""


class AutoCompleteLocators:
    """CSS селекторы для элементов страницы Auto Complete."""

    # === ПОЛЯ АВТОДОПОЛНЕНИЯ ===
    SINGLE_INPUT = ".auto-complete__control--is-focused .auto-complete__input input"  # Поле одиночного ввода
    SINGLE_CONTAINER = "#autoCompleteSingle"                # Контейнер одиночного автодополнения
    SINGLE_CONTROL = "#autoCompleteSingle .auto-complete__control"  # Контрол одиночного ввода

    MULTIPLE_INPUT = "#autoCompleteMultiple .auto-complete__input input"  # Поле множественного ввода
    MULTIPLE_CONTAINER = "#autoCompleteMultiple"           # Контейнер множественного автодополнения
    MULTIPLE_CONTROL = "#autoCompleteMultiple .auto-complete__control"  # Контрол множественного ввода

    # === ВЫПАДАЮЩИЕ МЕНЮ ===
    DROPDOWN_MENU = ".auto-complete__menu"                 # Выпадающее меню с предложениями
    DROPDOWN_OPTIONS = ".auto-complete__option"            # Опции в выпадающем меню
    DROPDOWN_FOCUSED_OPTION = ".auto-complete__option--is-focused"  # Сфокусированная опция
    DROPDOWN_SELECTED_OPTION = ".auto-complete__option--is-selected"  # Выбранная опция

    # === КОНТРОЛЫ И ИНДИКАТОРЫ ===
    DROPDOWN_INDICATOR = ".auto-complete__dropdown-indicator"  # Индикатор выпадающего списка
    CLEAR_INDICATOR = ".auto-complete__clear-indicator"    # Индикатор очистки
    LOADING_INDICATOR = ".auto-complete__loading-indicator" # Индикатор загрузки

    # === ЗНАЧЕНИЯ И ТЕГИ ===
    SINGLE_VALUE = ".auto-complete__single-value"          # Выбранное значение (одиночное)
    MULTI_VALUE = ".auto-complete__multi-value"            # Тег выбранного значения (множественное)
    MULTI_VALUE_LABEL = ".auto-complete__multi-value__label"  # Текст тега
    MULTI_VALUE_REMOVE = ".auto-complete__multi-value__remove"  # Кнопка удаления тега

    # === ПЛЕЙСХОЛДЕРЫ И СООБЩЕНИЯ ===
    PLACEHOLDER = ".auto-complete__placeholder"            # Плейсхолдер поля ввода
    INPUT_PLACEHOLDER = "input[placeholder]"               # Input с атрибутом placeholder
    NO_OPTIONS_MESSAGE = ".auto-complete__menu-notice"     # Сообщение об отсутствии опций
    LOADING_MESSAGE = ".auto-complete__loading-message"    # Сообщение загрузки

    # === СОСТОЯНИЯ КОНТРОЛОВ ===
    CONTROL_FOCUSED = ".auto-complete__control--is-focused" # Сфокусированный контрол
    CONTROL_DISABLED = ".auto-complete__control--is-disabled" # Отключенный контрол
    MENU_IS_OPEN = ".auto-complete__control--menu-is-open"  # Контрол с открытым меню

    # === ГРУППЫ ОПЦИЙ ===
    OPTION_GROUP = ".auto-complete__group"                 # Группа опций
    GROUP_HEADING = ".auto-complete__group-heading"        # Заголовок группы

    # === ПОИСК И ФИЛЬТРАЦИЯ ===
    SEARCH_INPUT = "input[role='combobox']"                # Поле поиска
    FILTER_RESULTS = ".auto-complete__option"              # Отфильтрованные результаты

    # === АЛЬТЕРНАТИВНЫЕ СЕЛЕКТОРЫ ===
    INPUT_FIELD = "input.auto-complete__input"             # Альтернативный селектор поля ввода
    VALUE_CONTAINER = ".auto-complete__value-container"    # Контейнер значений
    MENU_LIST = ".auto-complete__menu-list"               # Список в меню

    # === АТРИБУТЫ И СВОЙСТВА ===
    INPUT_VALUE_ATTRIBUTE = "value"                        # Атрибут значения input
    ARIA_EXPANDED = "aria-expanded"                        # Атрибут развернутого состояния
    ARIA_SELECTED = "aria-selected"                       # Атрибут выбранного состояния

    # === АНИМАЦИЯ И ПЕРЕХОДЫ ===
    MENU_PORTAL = ".auto-complete__menu-portal"            # Портал меню
    TRANSITION_GROUP = ".auto-complete__multi-value__transition-group"  # Группа переходов
