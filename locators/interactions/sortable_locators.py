"""
Локаторы для страницы Sortable.
Содержит селекторы для перетаскиваемых элементов в списках и сетках.
"""


class SortableLocators:
    """CSS селекторы для элементов страницы Sortable."""

    # === ВКЛАДКИ ИНТЕРФЕЙСА ===
    LIST_TAB = "#demo-tab-list"  # Вкладка списка
    GRID_TAB = "#demo-tab-grid"  # Вкладка сетки

    # === ЭЛЕМЕНТЫ СПИСКА ===
    ITEM_LIST = "div.list-group-item.list-group-item-action"  # Элементы в списке
    LIST_CONTAINER = "#demo-tabpane-list"  # Контейнер списка
    LIST_ITEM_TEMPLATE = ".list-group-item:nth-child({})"  # Шаблон для N-го элемента

    # === ЭЛЕМЕНТЫ СЕТКИ ===
    GRID_ITEM_LIST = ".create-grid > li"  # Элементы в сетке
    GRID_CONTAINER = "#demo-tabpane-grid"  # Контейнер сетки
    GRID_ITEM_TEMPLATE = (
        ".create-grid > li:nth-child({})"  # Шаблон для N-го элемента сетки
    )

    # === СОСТОЯНИЯ ЭЛЕМЕНТОВ ===
    DRAGGING_ELEMENT = ".ui-sortable-helper"  # Перетаскиваемый элемент
    DROP_PLACEHOLDER = ".ui-sortable-placeholder"  # Плейсхолдер для вставки
    SORTABLE_ACTIVE = ".ui-sortable"  # Активный сортируемый контейнер

    # === ИНТЕРАКТИВНЫЕ ЗОНЫ ===
    DRAG_HANDLE = ".drag-handle"  # Ручка для перетаскивания
    SORTABLE_AREA = ".sortable-area"  # Область сортировки

    # === ВСПОМОГАТЕЛЬНЫЕ СЕЛЕКТОРЫ ===
    ALL_SORTABLE_ITEMS = ".list-group-item, .create-grid li"  # Все сортируемые элементы
    FIRST_LIST_ITEM = ".list-group-item:first-child"  # Первый элемент списка
    LAST_LIST_ITEM = ".list-group-item:last-child"  # Последний элемент списка
    FIRST_GRID_ITEM = ".create-grid li:first-child"  # Первый элемент сетки
    LAST_GRID_ITEM = ".create-grid li:last-child"  # Последний элемент сетки

    # === КОНТЕЙНЕРЫ ВКЛАДОК ===
    TAB_NAVIGATION = ".nav-tabs"  # Навигация по вкладкам
    TAB_CONTENT = ".tab-content"  # Контент вкладок
    ACTIVE_TAB_PANEL = ".tab-pane.active"  # Активная панель вкладки
