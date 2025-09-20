"""
Локаторы для страницы Tabs.
Содержит селекторы для элементов интерфейса вкладок и их содержимого.
"""


class TabsLocators:
    """CSS селекторы для элементов страницы Tabs."""

    # === ЗАГОЛОВКИ ВКЛАДОК (НАВИГАЦИЯ) ===
    WHAT_TAB = "#demo-tab-what"  # Вкладка What
    ORIGIN_TAB = "#demo-tab-origin"  # Вкладка Origin
    USE_TAB = "#demo-tab-use"  # Вкладка Use
    MORE_TAB = "#demo-tab-more"  # Вкладка More (отключена по умолчанию)

    # === ПАНЕЛИ СОДЕРЖИМОГО ВКЛАДОК ===
    WHAT_CONTENT = "#demo-tabpane-what"  # Панель содержимого What
    ORIGIN_CONTENT = "#demo-tabpane-origin"  # Панель содержимого Origin
    USE_CONTENT = "#demo-tabpane-use"  # Панель содержимого Use
    MORE_CONTENT = "#demo-tabpane-more"  # Панель содержимого More

    # === ТЕКСТОВОЕ СОДЕРЖИМОЕ В ПАНЕЛЯХ ===
    WHAT_TEXT = "#demo-tabpane-what p"  # Текст в панели What
    ORIGIN_TEXT = "#demo-tabpane-origin p"  # Текст в панели Origin
    USE_TEXT = "#demo-tabpane-use p"  # Текст в панели Use
    MORE_TEXT = "#demo-tabpane-more p"  # Текст в панели More

    # === СОСТОЯНИЯ ВКЛАДОК ===
    ACTIVE_TAB = ".nav-link.active"  # Активная вкладка
    DISABLED_TAB = ".nav-link.disabled"  # Отключенная вкладка
    INACTIVE_TAB = ".nav-link:not(.active)"  # Неактивная вкладка

    # === КОНТЕЙНЕРЫ ===
    TAB_NAVIGATION = ".nav.nav-tabs"  # Навигация по вкладкам
    TAB_CONTENT_CONTAINER = ".tab-content"  # Контейнер содержимого вкладок
    ACTIVE_PANEL = ".tab-pane.active"  # Активная панель содержимого

    # === ОБЩИЕ СЕЛЕКТОРЫ ===
    ALL_TAB_HEADERS = ".nav-link"  # Все заголовки вкладок
    ALL_TAB_PANELS = ".tab-pane"  # Все панели содержимого
    TAB_WRAPPER = ".tabs-wrapper"  # Общая обертка компонента
