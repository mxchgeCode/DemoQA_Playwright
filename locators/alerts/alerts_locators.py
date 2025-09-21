"""
Локаторы для страницы Alerts.
Содержит селекторы для различных типов JavaScript alert диалогов.
"""


class AlertsLocators:
    """CSS селекторы для элементов страницы Alerts."""

    # Кнопки для вызова различных типов alert диалогов
    ALERT_BUTTON = "button#alertButton"  # Простой alert
    TIMER_ALERT_BUTTON = "button#timerAlertButton"  # Alert с задержкой 5 секунд
    CONFIRM_BUTTON = "button#confirmButton"  # Confirm диалог с OK/Cancel
    PROMPT_BUTTON = "button#promtButton"  # Prompt диалог (сохраняем опечатку в ID на реальном сайте)

    # Элементы отображения результатов
    CONFIRM_RESULT = "#confirmResult"  # Результат confirm диалога
    PROMPT_RESULT = "#promptResult"   # Результат prompt диалога

    # Альтернативные селекторы для проверки
    ALERT_SECTION = ".card-body"  # Секция с кнопками
    ALL_BUTTONS = "button[id*='Button']"  # Все кнопки с 'Button' в ID
