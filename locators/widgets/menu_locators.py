"""
Локаторы для страницы Menu.
Содержит селекторы для навигационного меню с подпунктами:
- Основные пункты меню
- Подменю и вложенные элементы
- Состояния наведения и активации
"""


class MenuLocators:
    """CSS селекторы для элементов страницы Menu."""

    # === ОСНОВНОЕ МЕНЮ ===
    MENU_CONTAINER = "#nav"                                # Основной контейнер меню
    MENU_LIST = "#nav ul"                                  # Список пунктов меню

    # === ОСНОВНЫЕ ПУНКТЫ МЕНЮ (первый уровень) ===
    MAIN_ITEM_1 = "#nav li:nth-child(1) a"                # Первый пункт меню
    MAIN_ITEM_2 = "#nav li:nth-child(2) a"                # Второй пункт меню
    MAIN_ITEM_3 = "#nav li:nth-child(3) a"                # Третий пункт меню

    # === КОНКРЕТНЫЕ ПУНКТЫ МЕНЮ ===
    MAIN_ITEM_LINK_1 = "a:has-text('Main Item 1')"        # Пункт "Main Item 1"
    MAIN_ITEM_LINK_2 = "a:has-text('Main Item 2')"        # Пункт "Main Item 2"
    MAIN_ITEM_LINK_3 = "a:has-text('Main Item 3')"        # Пункт "Main Item 3"

    # === ПОДМЕНЮ (второй уровень) ===
    SUB_MENU = "#nav ul ul"                               # Подменю
    SUB_ITEM_LIST = "#nav li:nth-child(2) ul li a"        # Элементы подменю

    # === КОНКРЕТНЫЕ ПОДПУНКТЫ ===
    SUB_SUB_LIST = "a:has-text('SUB SUB LIST »')"         # Подпункт с вложенным меню
    SUB_ITEM_1 = "a:has-text('Sub Item 1')"               # Подпункт 1
    SUB_ITEM_2 = "a:has-text('Sub Item 2')"               # Подпункт 2

    # === ПОДПОДМЕНЮ (третий уровень) ===
    SUB_SUB_MENU = "#nav ul ul ul"                        # Подподменю (третий уровень)
    SUB_SUB_ITEM_1 = "a:has-text('Sub Sub Item 1')"       # Элемент третьего уровня 1
    SUB_SUB_ITEM_2 = "a:has-text('Sub Sub Item 2')"       # Элемент третьего уровня 2

    # === ОБЩИЕ СЕЛЕКТОРЫ ===
    ALL_MENU_ITEMS = "#nav a"                             # Все пункты меню
    ALL_MENU_LINKS = "#nav li a"                          # Все ссылки меню
    TOP_LEVEL_ITEMS = "#nav > ul > li > a"                # Пункты первого уровня

    # === СОСТОЯНИЯ ЭЛЕМЕНТОВ ===
    HOVERED_ITEM = "#nav li:hover"                        # Элемент под курсором
    ACTIVE_ITEM = "#nav li.active"                        # Активный элемент
    FOCUSED_ITEM = "#nav a:focus"                         # Сфокусированный элемент

    # === ИНДИКАТОРЫ ПОДМЕНЮ ===
    DROPDOWN_INDICATOR = ".dropdown-indicator"            # Индикатор наличия подменю
    ARROW_INDICATOR = ".arrow"                            # Стрелка подменю
    EXPAND_ICON = ".expand-icon"                          # Иконка раскрытия

    # === КОНТЕЙНЕРЫ И ОБЕРТКИ ===
    MENU_WRAPPER = ".menu-wrapper"                        # Обертка меню
    NAVIGATION_BAR = ".navigation"                        # Навигационная панель
    MENU_OVERLAY = ".menu-overlay"                        # Оверлей меню

    # === МОБИЛЬНОЕ МЕНЮ ===
    MOBILE_MENU_TOGGLE = ".mobile-menu-toggle"            # Кнопка мобильного меню
    MOBILE_MENU = ".mobile-menu"                          # Мобильное меню
    HAMBURGER_BUTTON = ".hamburger"                       # Кнопка "гамбургер"

    # === СОСТОЯНИЯ ВИДИМОСТИ ===
    VISIBLE_SUBMENU = "ul[style*='display: block']"       # Видимое подменю
    HIDDEN_SUBMENU = "ul[style*='display: none']"         # Скрытое подменю

    # === АНИМАЦИЯ И ПЕРЕХОДЫ ===
    TRANSITION_CLASS = ".menu-transition"                 # Класс анимации
    SLIDE_DOWN = ".slide-down"                            # Анимация выпадения
    FADE_IN = ".fade-in"                                  # Анимация появления

    # === ДОСТУПНОСТЬ ===
    ARIA_EXPANDED = "[aria-expanded]"                     # Атрибут развернутого состояния
    ARIA_HASPOPUP = "[aria-haspopup]"                     # Атрибут наличия всплывающего меню
    ROLE_MENU = "[role='menu']"                           # Роль меню
    ROLE_MENUITEM = "[role='menuitem']"                   # Роль элемента меню

    # === СТРУКТУРНЫЕ СЕЛЕКТОРЫ ===
    MENU_LEVEL_1 = "#nav > ul > li"                      # Элементы первого уровня
    MENU_LEVEL_2 = "#nav ul ul li"                       # Элементы второго уровня
    MENU_LEVEL_3 = "#nav ul ul ul li"                    # Элементы третьего уровня

    # === ТЕКСТОВЫЕ СЕЛЕКТОРЫ ===
    MENU_TEXT = ".menu-text"                              # Текст пункта меню
    MENU_LABEL = ".menu-label"                            # Лейбл пункта меню
    MENU_DESCRIPTION = ".menu-description"                # Описание пункта меню
