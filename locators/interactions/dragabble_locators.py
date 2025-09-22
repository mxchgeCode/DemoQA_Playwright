"""
Локаторы для страницы Dragabble (Перетаскивание).
Содержит селекторы для различных типов перетаскиваемых элементов:
- Простое перетаскивание
- Ограничения по осям
- Ограничения контейнером
- Стили курсора
"""


class DragabbleLocators:
    """CSS селекторы для элементов страницы Dragabble."""

    # === ОСНОВНОЙ ПЕРЕТАСКИВАЕМЫЙ ЭЛЕМЕНТ ===
    DRAG_BOX = "#dragBox"  # Основной перетаскиваемый блок

    # === ВКЛАДКИ ФУНКЦИОНАЛЬНОСТИ ===
    TAB_SIMPLE = "#draggableExample-tab-simple"  # Вкладка простого перетаскивания
    TAB_AXIS_RESTRICTED = (
        "#draggableExample-tab-axisRestriction"  # Вкладка ограничения по осям
    )
    TAB_CONTAINER_RESTRICTED = (
        "#draggableExample-tab-containerRestriction"  # Вкладка ограничения контейнером
    )
    TAB_CURSOR_STYLE = "#draggableExample-tab-cursorStyle"  # Вкладка стилей курсора

    # === ЭЛЕМЕНТЫ С ОГРАНИЧЕНИЯМИ ПО ОСЯМ ===
    DRAG_BOX_AXIS_X = "#restrictedX"  # Элемент с ограничением по оси X
    DRAG_BOX_AXIS_Y = "#restrictedY"  # Элемент с ограничением по оси Y

    # === ЭЛЕМЕНТЫ С ОГРАНИЧЕНИЯМИ КОНТЕЙНЕРА ===
    DRAG_BOX_CONTAINER = (
        "#containmentWrapper #dragBox"  # Элемент в ограниченном контейнере
    )
    DRAGGABLE_DIV_CONTAINER = ".draggable.ui-widget-content.ui-draggable.ui-draggable-handle"  # Div в контейнере
    DRAGGABLE_SPAN_CONTAINER = (
        ".ui-widget-header.ui-draggable.ui-draggable-handle"  # Span в контейнере
    )
    CONTAINMENT_WRAPPER = "#containmentWrapper"  # Контейнер ограничения

    # === ЭЛЕМЕНТЫ СО СТИЛЯМИ КУРСОРА ===
    DRAG_BOX_CURSOR = "#cursorCentered"  # Элемент с центрированным курсором (устарел)
    CURSOR_CENTER = "#cursorCenter"  # Курсор по центру
    CURSOR_TOP_LEFT = "#cursorTopLeft"  # Курсор в левом верхнем углу
    CURSOR_BOTTOM = "#cursorBottom"  # Курсор внизу элемента

    # === КОНТЕЙНЕРЫ ВКЛАДОК ===
    SIMPLE_TAB_PANE = (
        "#draggableExample-tabpane-simple"  # Панель простого перетаскивания
    )
    AXIS_TAB_PANE = (
        "#draggableExample-tabpane-axisRestriction"  # Панель ограничения по осям
    )
    CONTAINER_TAB_PANE = "#draggableExample-tabpane-containerRestriction"  # Панель ограничения контейнером
    CURSOR_TAB_PANE = "#draggableExample-tabpane-cursorStyle"  # Панель стилей курсора

    # === ВСПОМОГАТЕЛЬНЫЕ СЕЛЕКТОРЫ ===
    ALL_DRAGGABLE = ".ui-draggable"  # Все перетаскиваемые элементы
    DRAGGABLE_HANDLE = ".ui-draggable-handle"  # Ручки для перетаскивания
    DRAG_ACTIVE = ".ui-draggable-dragging"  # Элемент в процессе перетаскивания

    # === ТЕКСТОВЫЕ МЕТКИ ===
    AXIS_X_LABEL = "text=Only X"  # Метка ограничения по X
    AXIS_Y_LABEL = "text=Only Y"  # Метка ограничения по Y
    CONTAINER_LABEL = "text=I'm contained within"  # Метка контейнера

    # === ОБЛАСТИ ОГРАНИЧЕНИЙ ===
    RESTRICTED_AREA = ".drag-restricted-area"  # Зона ограниченного перетаскивания
    BOUNDARY_CONTAINER = ".boundary-container"  # Контейнер границ
