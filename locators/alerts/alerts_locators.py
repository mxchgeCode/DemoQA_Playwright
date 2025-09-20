"""
Локаторы для страницы Alerts.
Содержит селекторы для различных типов JavaScript alert диалогов.
"""


class AlertsLocators:
    """CSS селекторы для элементов страницы Alerts."""

    # Кнопки для вызова различных типов alert диалогов
    SIMPLE_ALERT_BUTTON = "button#alertButton"
    TIMER_ALERT_BUTTON = "button#timerAlertButton"  # Alert с задержкой 5 секунд
    CONFIRM_BUTTON = "button#confirmButton"  # Confirm диалог с OK/Cancel
    PROMPT_BUTTON = "button#promtButton"  # Prompt диалог с полем ввода

    # Элементы отображения результатов
    CONFIRM_RESULT_TEXT = "#confirmResult"  # Результат confirm диалога
    PROMPT_RESULT_TEXT = "#promptResult"  # Результат prompt диалога

    # Дополнительные селекторы для надежности
    ALL_ALERT_BUTTONS = "button[id$='Button']"  # Все кнопки alert на странице
    RESULT_CONTAINER = "#output"  # Контейнер результатов


class AlertsLocators:
    """CSS селекторы для элементов страницы Alerts."""

    # Исправленные селекторы (исходная версия имеет опечатки)
    ALERT_BUTTON = "button#alertButton"
    TIMER_ALERT_BUTTON = "button#timerAlertButton"
    CONFIRM_BUTTON = "button#confirmButton"
    PROMPT_BUTTON = "button#promtButton"  # Оставляем как в исходном коде (с опечаткой)

    # Результаты
    CONFIRM_RESULT = "#confirmResult"
    PROMPT_RESULT = "#promptResult"
