"""
Локаторы для страницы Selectable (Выбираемые элементы).
Содержит селекторы для интерактивного выбора элементов:
- Список элементов
- Сетка элементов
- Состояния выбора
"""


class SelectableLocators:
    """CSS селекторы для элементов страницы Selectable."""

    # === ВКЛАДКИ ИНТЕРФЕЙСА ===
    LIST_TAB_BUTTON = "#demo-tab-list"                  # Кнопка вкладки списка
    GRID_TAB_BUTTON = "#demo-tab-grid"                  # Кнопка вкладки сетки

    # === КОНТЕНТ ВКЛАДОК ===
    LIST_TAB_CONTENT = "#demo-tabpane-list .list-group-item"  # Элементы списка
    GRID_TAB_CONTENT = "#demo-tabpane-grid .list-group-item"  # Элементы сетки

    # === КОНТЕЙНЕРЫ ВКЛАДОК ===
    LIST_TAB_PANE = "#demo-tabpane-list"                # Панель вкладки списка
    GRID_TAB_PANE = "#demo-tabpane-grid"                # Панель вкладки сетки

    # === ЭЛЕМЕНТЫ СПИСКА ===
    LIST_ITEMS = "#demo-tabpane-list .list-group-item"  # Все элементы списка
    LIST_ITEM_TEMPLATE = "#demo-tabpane-list .list-group-item:nth-child({})"  # Шаблон N-го элемента
    LIST_CONTAINER = "#demo-tabpane-list ol"            # Контейнер списка

    # === ЭЛЕМЕНТЫ СЕТКИ ===
    GRID_ITEMS = "#demo-tabpane-grid .list-group-item"  # Все элементы сетки
    GRID_ITEM_TEMPLATE = "#demo-tabpane-grid .list-group-item:nth-child({})"  # Шаблон N-го элемента сетки
    GRID_CONTAINER = "#demo-tabpane-grid .row"          # Контейнер сетки

    # === СОСТОЯНИЯ ВЫБОРА ===
    SELECTED_ITEM = ".active"                           # Выбранный элемент
    UNSELECTED_ITEM = ".list-group-item:not(.active)"   # Невыбранный элемент
    SELECTABLE_ITEM = ".list-group-item"                # Выбираемый элемент

    # === КЛАССЫ СОСТОЯНИЙ ===
    ACTIVE_CLASS = "active"                             # Класс активного элемента
    SELECTED_CLASS = "ui-selected"                      # Класс выбранного элемента
    SELECTING_CLASS = "ui-selecting"                    # Элемент в процессе выбора

    # === МНОЖЕСТВЕННЫЙ ВЫБОР ===
    MULTI_SELECTED = ".list-group-item.active"         # Множественно выбранные элементы
    SELECTION_AREA = ".ui-selectable"                   # Область выбора
    LASSO_SELECTION = ".ui-selectable-lasso"            # Лассо выбора

    # === НАВИГАЦИЯ ПО ВКЛАДКАМ ===
    TAB_NAVIGATION = ".nav-tabs"                        # Навигация по вкладкам
    ACTIVE_TAB = ".nav-tabs .nav-link.active"           # Активная вкладка
    TAB_CONTENT_CONTAINER = ".tab-content"              # Контейнер содержимого вкладок

    # === ВСПОМОГАТЕЛЬНЫЕ СЕЛЕКТОРЫ ===
    ALL_ITEMS = ".list-group-item"                      # Все выбираемые элементы
    FIRST_ITEM = ".list-group-item:first-child"         # Первый элемент
    LAST_ITEM = ".list-group-item:last-child"           # Последний элемент

    # === ИНДЕКСЫ ЭЛЕМЕНТОВ (для удобства) ===
    FIRST_LIST_ITEM = 0                                 # Индекс первого элемента списка
    SECOND_LIST_ITEM = 1                                # Индекс второго элемента списка
    THIRD_LIST_ITEM = 2                                 # Индекс третьего элемента списка
    FOURTH_LIST_ITEM = 3                                # Индекс четвертого элемента списка

    # === АТРИБУТЫ И СВОЙСТВА ===
    ITEM_TEXT_ATTRIBUTE = "textContent"                 # Атрибут текста элемента
    SELECTION_STATE_ATTRIBUTE = "aria-selected"        # Атрибут состояния выбора

    # === АНИМАЦИЯ И ВИЗУАЛЬНЫЕ ЭФФЕКТЫ ===
    HOVER_EFFECT = ":hover"                             # Эффект наведения
    FOCUS_EFFECT = ":focus"                             # Эффект фокуса
    TRANSITION_CLASS = ".transition"                    # Класс анимации перехода
