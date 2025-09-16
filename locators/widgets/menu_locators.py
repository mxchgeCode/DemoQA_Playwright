class MenuLocators:
    # Основной контейнер
    MAIN_CONTAINER = "#app"

    # Menu tree structure
    MENU_TREE = ".menu-list"  # Более надежный селектор
    TREE_ITEMS = ".menu-item"  # Более надежный селектор

    # Конкретные элементы по тексту (используем :has-text для гибкости)
    MAIN_ITEM_1 = ":has-text('Main Item 1')"
    MAIN_ITEM_2 = ":has-text('Main Item 2')"
    MAIN_ITEM_3 = ":has-text('Main Item 3')"
    SUB_ITEM = ":has-text('Sub Item')"
    SUB_SUB_LIST = ":has-text('SUB SUB LIST')"
    SUB_SUB_ITEM_1 = ":has-text('Sub Sub Item 1')"
    SUB_SUB_ITEM_2 = ":has-text('Sub Sub Item 2')"

    # Все кликабельные элементы
    CLICKABLE_ITEMS = ".menu-item > a"  # Кликабельные элементы меню
