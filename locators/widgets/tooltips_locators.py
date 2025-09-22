"""
Локаторы для страницы Tool Tips.
Содержит селекторы для различных типов всплывающих подсказок:
- Подсказки на кнопках
- Подсказки на полях ввода
- Подсказки на тексте и ссылках
- Позиционирование подсказок
"""


class ToolTipsLocators:
    """CSS селекторы для элементов страницы Tool Tips."""

    # === ЭЛЕМЕНТЫ С ПОДСКАЗКАМИ ===
    TOOLTIP_BUTTON = "#toolTipButton"  # Кнопка с подсказкой
    TOOLTIP_TEXT_FIELD = "#toolTipTextField"  # Поле ввода с подсказкой
    TOOLTIP_TEXT_LINK = "a:has-text('Contrary')"  # Ссылка в тексте с подсказкой
    TOOLTIP_SECTION_LINK = "a:has-text('1.10.32')"  # Ссылка на секцию с подсказкой

    # === КОНТЕЙНЕРЫ ПОДСКАЗОК ===
    TOOLTIP_WRAPPER = "[data-tooltip]"  # Обертка элементов с подсказками
    TOOLTIP_TRIGGER = "[data-tip]"  # Триггер подсказки

    # === ВСПЛЫВАЮЩИЕ ПОДСКАЗКИ ===
    TOOLTIP = ".tooltip"  # Основная подсказка
    TOOLTIP_INNER = ".tooltip-inner"  # Внутреннее содержимое подсказки
    TOOLTIP_ARROW = ".tooltip-arrow"  # Стрелка подсказки

    # === БИБЛИОТЕКА REACT-TOOLTIP ===
    REACT_TOOLTIP = ".__react_component_tooltip"  # React tooltip компонент
    TOOLTIP_PLACE_TOP = ".place-top"  # Подсказка сверху
    TOOLTIP_PLACE_BOTTOM = ".place-bottom"  # Подсказка снизу
    TOOLTIP_PLACE_LEFT = ".place-left"  # Подсказка слева
    TOOLTIP_PLACE_RIGHT = ".place-right"  # Подсказка справа

    # === СОСТОЯНИЯ ПОДСКАЗОК ===
    TOOLTIP_SHOW = ".tooltip.show"  # Показанная подсказка
    TOOLTIP_HIDDEN = ".tooltip[style*='display: none']"  # Скрытая подсказка
    TOOLTIP_VISIBLE = ".tooltip[aria-hidden='false']"  # Видимая подсказка
    TOOLTIP_FADE_IN = ".tooltip.fade.in"  # Подсказка с анимацией появления

    # === ТИПЫ ПОДСКАЗОК ===
    TOOLTIP_PRIMARY = ".tooltip-primary"  # Основная подсказка
    TOOLTIP_SECONDARY = ".tooltip-secondary"  # Вторичная подсказка
    TOOLTIP_SUCCESS = ".tooltip-success"  # Подсказка успеха
    TOOLTIP_WARNING = ".tooltip-warning"  # Предупреждающая подсказка
    TOOLTIP_ERROR = ".tooltip-error"  # Подсказка ошибки

    # === КОНТЕНТ ПОДСКАЗОК ===
    TOOLTIP_TEXT = ".tooltip-text"  # Текст подсказки
    TOOLTIP_TITLE = ".tooltip-title"  # Заголовок подсказки
    TOOLTIP_BODY = ".tooltip-body"  # Тело подсказки
    TOOLTIP_CONTENT = ".tooltip-content"  # Содержимое подсказки

    # === ПОЗИЦИОНИРОВАНИЕ ===
    TOOLTIP_TOP = "[data-placement='top']"  # Подсказка сверху
    TOOLTIP_BOTTOM = "[data-placement='bottom']"  # Подсказка снизу
    TOOLTIP_LEFT = "[data-placement='left']"  # Подсказка слева
    TOOLTIP_RIGHT = "[data-placement='right']"  # Подсказка справа

    # === ИНТЕРАКТИВНЫЕ ЭЛЕМЕНТЫ ===
    HOVERABLE_ELEMENT = "[data-hover='tooltip']"  # Элемент с подсказкой при наведении
    CLICKABLE_TOOLTIP = "[data-click='tooltip']"  # Подсказка по клику
    FOCUSABLE_TOOLTIP = "[data-focus='tooltip']"  # Подсказка при фокусе

    # === АНИМАЦИЯ И ПЕРЕХОДЫ ===
    TOOLTIP_TRANSITION = ".tooltip-transition"  # Подсказка с анимацией
    FADE_TOOLTIP = ".fade-tooltip"  # Подсказка с эффектом растворения
    SLIDE_TOOLTIP = ".slide-tooltip"  # Подсказка с эффектом скольжения

    # === ТЕКСТ ДЛЯ ПРОВЕРКИ ===
    BUTTON_TOOLTIP_TEXT = (
        "You hovered over the Button"  # Ожидаемый текст подсказки кнопки
    )
    INPUT_TOOLTIP_TEXT = (
        "You hovered over the text field"  # Ожидаемый текст подсказки поля
    )
    LINK_TOOLTIP_TEXT = (
        "You hovered over the Contrary"  # Ожидаемый текст подсказки ссылки
    )
    SECTION_TOOLTIP_TEXT = (
        "You hovered over the 1.10.32"  # Ожидаемый текст подсказки секции
    )

    # === АТРИБУТЫ ===
    TITLE_ATTRIBUTE = "[title]"  # Элементы с атрибутом title
    DATA_TOOLTIP_ATTRIBUTE = "[data-tooltip]"  # Элементы с data-tooltip
    ARIA_DESCRIBEDBY = "[aria-describedby]"  # Связь с описанием подсказки

    # === КОНТЕКСТНЫЕ МЕНЮ ===
    CONTEXT_TOOLTIP = ".context-tooltip"  # Контекстная подсказка
    POPUP_TOOLTIP = ".popup-tooltip"  # Всплывающая подсказка
    INLINE_TOOLTIP = ".inline-tooltip"  # Встроенная подсказка

    # === ДОСТУПНОСТЬ ===
    TOOLTIP_ROLE = "[role='tooltip']"  # Роль подсказки
    TOOLTIP_ID = "[id*='tooltip']"  # ID подсказки
    LIVE_REGION = "[aria-live]"  # Живой регион для подсказок

    # === РАЗМЕРЫ ПОДСКАЗОК ===
    SMALL_TOOLTIP = ".tooltip-sm"  # Маленькая подсказка
    LARGE_TOOLTIP = ".tooltip-lg"  # Большая подсказка
    EXTRA_LARGE_TOOLTIP = ".tooltip-xl"  # Очень большая подсказка

    # === СПЕЦИАЛЬНЫЕ СЕЛЕКТОРЫ ===
    MULTILINE_TOOLTIP = ".tooltip-multiline"  # Многострочная подсказка
    RICH_TOOLTIP = ".tooltip-rich"  # Подсказка с богатым контентом
    CUSTOM_TOOLTIP = ".custom-tooltip"  # Кастомная подсказка
