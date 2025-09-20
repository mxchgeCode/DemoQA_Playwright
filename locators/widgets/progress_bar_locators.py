"""
Локаторы для страницы Progress Bar.
Содержит селекторы для элементов управления и отображения прогресс-бара.
"""


class ProgressBarLocators:
    """CSS селекторы для элементов страницы Progress Bar."""

    # === ОСНОВНЫЕ ЭЛЕМЕНТЫ ПРОГРЕСС-БАРА ===
    PROGRESS_BAR = "#progressBar"  # Основной прогресс-бар элемент
    PROGRESS_BAR_VALUE = "#progressBar .progress-bar"  # Полоса прогресса со значением

    # === КНОПКИ УПРАВЛЕНИЯ ===
    START_STOP_BUTTON = "#startStopButton"  # Кнопка Start/Stop
    RESET_BUTTON = "#resetButton"  # Кнопка Reset (появляется после остановки)

    # === ЗНАЧЕНИЯ И СОСТОЯНИЯ ===
    PROGRESS_LABEL = ".progress-bar"  # Метка с процентами
    PROGRESS_WRAPPER = ".progress"  # Обертка прогресс-бара

    # === ДИНАМИЧЕСКИЕ СОСТОЯНИЯ КНОПКИ ===
    START_BUTTON_STATE = "button:has-text('Start')"  # Кнопка в состоянии Start
    STOP_BUTTON_STATE = "button:has-text('Stop')"  # Кнопка в состоянии Stop
    RESET_BUTTON_STATE = "button:has-text('Reset')"  # Кнопка в состоянии Reset

    # === АТРИБУТЫ ПРОГРЕССА ===
    PROGRESS_VALUE_ATTRIBUTE = "[aria-valuenow]"  # Атрибут текущего значения
    PROGRESS_MIN_ATTRIBUTE = "[aria-valuemin]"  # Минимальное значение
    PROGRESS_MAX_ATTRIBUTE = "[aria-valuemax]"  # Максимальное значение

    # === КОНТЕЙНЕР КОМПОНЕНТА ===
    PROGRESS_CONTAINER = ".progress-bar-container"  # Общий контейнер
    BUTTON_CONTAINER = ".mt-3"  # Контейнер кнопок
