"""
Локаторы для страницы Droppable (Области сброса).
Содержит селекторы для различных сценариев сброса элементов:
- Простое перетаскивание и сброс
- Принимаемые/непринимаемые элементы
- Предотвращение всплытия событий
- Возврат элементов после сброса
"""


class DroppableLocators:
    """CSS селекторы для элементов страницы Droppable."""

    # === ВКЛАДКИ ФУНКЦИОНАЛЬНОСТИ ===
    SIMPLE_TAB = "#droppableExample-tab-simple"         # Вкладка простого сброса
    ACCEPT_TAB = "#droppableExample-tab-accept"         # Вкладка принятия элементов
    PREVENT_TAB = "#droppableExample-tab-preventPropogation"  # Вкладка предотвращения всплытия
    REVERT_TAB = "#droppableExample-tab-revertable"     # Вкладка возврата элементов

    # === ПРОСТОЕ ПЕРЕТАСКИВАНИЕ ===
    SIMPLE_DRAG = "#draggable"                          # Перетаскиваемый элемент (простой)
    SIMPLE_DROP = "#simpleDropContainer #droppable"     # Область сброса (простая)
    SIMPLE_DROP_CONTAINER = "#simpleDropContainer"      # Контейнер простого сброса

    # === ПРИНЯТИЕ/ОТКЛОНЕНИЕ ЭЛЕМЕНТОВ ===
    ACCEPT_DRAG_ACCEPT = "#acceptable"                  # Принимаемый элемент
    ACCEPT_DRAG_NON_ACCEPT = "#notAcceptable"           # Непринимаемый элемент
    ACCEPT_DROP = "#acceptDropContainer #droppable"     # Область сброса (с принятием)
    ACCEPT_DROP_CONTAINER = "#acceptDropContainer"      # Контейнер принятия

    # === ПРЕДОТВРАЩЕНИЕ ВСПЛЫТИЯ ===
    DRAG_BOX = "#dragBox"                               # Перетаскиваемый блок
    NOT_GREEDY_DROP_BOX = "#notGreedyDropBox"           # Не жадная область сброса
    NOT_GREEDY_INNER_DROP_BOX = "#notGreedyInnerDropBox"  # Внутренняя не жадная область
    GREEDY_DROP_BOX = "#greedyDropBox"                  # Жадная область сброса
    GREEDY_DROP_BOX_INNER = "#greedyDropBoxInner"       # Внутренняя жадная область

    # === ВОЗВРАТ ЭЛЕМЕНТОВ ===
    REVERT_DRAG_REVERT = "#revertable"                  # Элемент с возвратом
    REVERT_DRAG_NOT_REVERT = "#notRevertable"           # Элемент без возврата
    REVERT_DROP_BOX = "#revertableDropContainer #droppable"  # Область сброса возврата
    REVERT_DROP_CONTAINER = "#revertableDropContainer"  # Контейнер возврата

    # === СОСТОЯНИЯ ОБЛАСТЕЙ СБРОСА ===
    DROP_ACTIVE = ".ui-droppable-active"                # Активная область сброса
    DROP_HOVER = ".ui-droppable-hover"                  # Область сброса под курсором
    DROP_ACCEPTED = ".ui-state-highlight"               # Область принявшая элемент
    DROP_DROPPED = ".dropped"                           # Область после успешного сброса

    # === ТЕКСТОВЫЕ СОСТОЯНИЯ ===
    DROP_DEFAULT_TEXT = "Drop here"                     # Текст по умолчанию
    DROP_SUCCESS_TEXT = "Dropped!"                      # Текст успешного сброса
    ACCEPT_TEXT = "Drop here"                           # Текст области принятия
    REJECT_TEXT = "Drop here"                           # Текст области отклонения

    # === КОНТЕЙНЕРЫ ВКЛАДОК ===
    SIMPLE_TAB_PANE = "#droppableExample-tabpane-simple"  # Панель простого сброса
    ACCEPT_TAB_PANE = "#droppableExample-tabpane-accept"  # Панель принятия
    PREVENT_TAB_PANE = "#droppableExample-tabpane-preventPropogation"  # Панель предотвращения
    REVERT_TAB_PANE = "#droppableExample-tabpane-revertable"  # Панель возврата

    # === ВИЗУАЛЬНЫЕ ИНДИКАТОРЫ ===
    HIGHLIGHT_CLASS = ".ui-state-highlight"             # Класс подсветки
    ERROR_CLASS = ".ui-state-error"                     # Класс ошибки
    SUCCESS_CLASS = ".ui-state-success"                 # Класс успеха

    # === АНИМАЦИЯ И ПЕРЕХОДЫ ===
    DRAGGING_CLASS = ".ui-draggable-dragging"           # Элемент в процессе перетаскивания
    REVERTING_CLASS = ".ui-draggable-reverting"         # Элемент в процессе возврата
    HELPER_CLASS = ".ui-draggable-helper"               # Вспомогательный элемент
