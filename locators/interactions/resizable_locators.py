"""
Локаторы для страницы Resizable (Изменение размера).
Содержит селекторы для элементов с возможностью изменения размера:
- Блок с ограничениями размера
- Элемент без ограничений
- Ручки изменения размера
"""


class ResizableLocators:
    """CSS селекторы для элементов страницы Resizable."""

    # === ОСНОВНЫЕ ИЗМЕНЯЕМЫЕ ЭЛЕМЕНТЫ ===
    BOX_WITH_LIMIT = "#resizableBoxWithRestriction"     # Блок с ограничениями размера
    BOX_HANDLE = "#resizableBoxWithRestriction > span.react-resizable-handle-se"  # Ручка блока с ограничениями

    BUTTON_RESIZABLE = "#resizable"                      # Кнопка без ограничений размера
    BUTTON_HANDLE = "#resizable > span.react-resizable-handle-se"  # Ручка кнопки без ограничений

    # === РУЧКИ ИЗМЕНЕНИЯ РАЗМЕРА ===
    HANDLE_SE = ".react-resizable-handle-se"            # Ручка юго-восток (правый нижний угол)
    HANDLE_S = ".react-resizable-handle-s"              # Ручка юг (нижняя сторона)
    HANDLE_E = ".react-resizable-handle-e"              # Ручка восток (правая сторона)
    HANDLE_NE = ".react-resizable-handle-ne"            # Ручка северо-восток
    HANDLE_N = ".react-resizable-handle-n"              # Ручка север
    HANDLE_NW = ".react-resizable-handle-nw"            # Ручка северо-запад
    HANDLE_W = ".react-resizable-handle-w"              # Ручка запад
    HANDLE_SW = ".react-resizable-handle-sw"            # Ручка юго-запад

    # === КОНТЕЙНЕРЫ ===
    RESIZABLE_CONTAINER = ".resizable-container"         # Контейнер изменяемых элементов
    RESTRICTION_CONTAINER = ".restriction-container"    # Контейнер с ограничениями

    # === КЛАССЫ СОСТОЯНИЙ ===
    RESIZABLE_CLASS = ".react-resizable"                # Класс изменяемого элемента
    RESIZING_CLASS = ".react-resizable-resizing"        # Элемент в процессе изменения размера
    HANDLE_ACTIVE = ".react-resizable-handle-active"    # Активная ручка

    # === ВСПОМОГАТЕЛЬНЫЕ СЕЛЕКТОРЫ ===
    ALL_RESIZABLE = ".react-resizable"                  # Все изменяемые элементы
    ALL_HANDLES = ".react-resizable-handle"             # Все ручки изменения размера

    # === ОГРАНИЧЕНИЯ РАЗМЕРА ===
    MIN_SIZE_INDICATOR = "[data-min-size]"              # Индикатор минимального размера
    MAX_SIZE_INDICATOR = "[data-max-size]"              # Индикатор максимального размера

    # === РАЗМЕРЫ ПО УМОЛЧАНИЮ ===
    DEFAULT_BOX_SIZE = "200x200"                        # Размер блока по умолчанию
    DEFAULT_BUTTON_SIZE = "auto"                        # Размер кнопки по умолчанию

    # === АТРИБУТЫ РАЗМЕРОВ ===
    WIDTH_ATTRIBUTE = "width"                           # Атрибут ширины
    HEIGHT_ATTRIBUTE = "height"                         # Атрибут высоты
    STYLE_ATTRIBUTE = "style"                           # Атрибут стиля

    # === КУРСОРЫ ИЗМЕНЕНИЯ РАЗМЕРА ===
    CURSOR_SE_RESIZE = "cursor: se-resize"              # Курсор изменения размера SE
    CURSOR_S_RESIZE = "cursor: s-resize"                # Курсор изменения размера S
    CURSOR_E_RESIZE = "cursor: e-resize"                # Курсор изменения размера E
