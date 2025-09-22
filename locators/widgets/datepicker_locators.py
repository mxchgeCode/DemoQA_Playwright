"""
Локаторы для страницы Date Picker.
Содержит селекторы для различных компонентов выбора даты:
- Простой выбор даты
- Выбор даты и времени
- Календарный интерфейс
- Навигация по месяцам/годам
"""


class DatePickerLocators:
    """CSS селекторы для элементов страницы Date Picker."""

    # === ОСНОВНЫЕ ПОЛЯ ВВОДА ===
    DATE_INPUT = "#datePickerMonthYearInput"  # Поле выбора даты (месяц/год)
    DATE_TIME_INPUT = "#dateAndTimePickerInput"  # Поле выбора даты и времени

    # === КАЛЕНДАРНЫЙ ВИДЖЕТ ===
    DATE_PICKER = ".react-datepicker"  # Основной календарный виджет
    DATE_PICKER_WRAPPER = ".react-datepicker-wrapper"  # Обертка календаря
    DATE_PICKER_POPPER = ".react-datepicker-popper"  # Поппер календаря

    # === ЗАГОЛОВОК КАЛЕНДАРЯ ===
    MONTH_YEAR_HEADER = (
        ".react-datepicker__current-month"  # Заголовок текущего месяца/года
    )
    MONTH_SELECT = ".react-datepicker__month-select"  # Dropdown выбора месяца
    YEAR_SELECT = ".react-datepicker__year-select"  # Dropdown выбора года

    # === НАВИГАЦИЯ ===
    PREV_MONTH_BUTTON = (
        ".react-datepicker__navigation--previous"  # Кнопка предыдущего месяца
    )
    NEXT_MONTH_BUTTON = (
        ".react-datepicker__navigation--next"  # Кнопка следующего месяца
    )
    PREV_YEAR_BUTTON = ".react-datepicker__navigation--years-previous"  # Предыдущий год
    NEXT_YEAR_BUTTON = ".react-datepicker__navigation--years-next"  # Следующий год

    # === ДНИ И ДАТЫ ===
    DAY_NAMES = ".react-datepicker__day-names"  # Названия дней недели
    DAY_NAME = ".react-datepicker__day-name"  # Отдельное название дня
    WEEK = ".react-datepicker__week"  # Неделя в календаре
    DAY = ".react-datepicker__day"  # День в календаре
    TODAY = ".react-datepicker__day--today"  # Сегодняшняя дата
    SELECTED_DAY = ".react-datepicker__day--selected"  # Выбранный день

    # === СОСТОЯНИЯ ДНЕЙ ===
    DAY_DISABLED = ".react-datepicker__day--disabled"  # Отключенный день
    DAY_OUTSIDE_MONTH = (
        ".react-datepicker__day--outside-month"  # День вне текущего месяца
    )
    DAY_WEEKEND = ".react-datepicker__day--weekend"  # Выходной день
    DAY_KEYBOARD_SELECTED = (
        ".react-datepicker__day--keyboard-selected"  # Выбранный с клавиатуры
    )

    # === ВРЕМЯ ===
    TIME_CONTAINER = ".react-datepicker__time-container"  # Контейнер времени
    TIME_BOX = ".react-datepicker__time-box"  # Блок выбора времени
    TIME_LIST = ".react-datepicker__time-list"  # Список времени
    TIME_LIST_ITEM = ".react-datepicker__time-list-item"  # Элемент списка времени
    TIME_LIST_ITEM_SELECTED = (
        ".react-datepicker__time-list-item--selected"  # Выбранное время
    )

    # === ВВОД ВРЕМЕНИ ===
    TIME_INPUT = ".react-datepicker-time__input"  # Поле ввода времени
    HOUR_INPUT = ".react-datepicker-time__input:nth-child(1)"  # Ввод часов
    MINUTE_INPUT = ".react-datepicker-time__input:nth-child(3)"  # Ввод минут

    # === МЕСЯЦЫ И ГОДЫ (режим выбора) ===
    MONTH_CONTAINER = ".react-datepicker__month-container"  # Контейнер месяцев
    YEAR_DROPDOWN = ".react-datepicker__year-dropdown"  # Dropdown годов
    YEAR_OPTION = ".react-datepicker__year-option"  # Опция года
    MONTH_OPTION = ".react-datepicker__month-option"  # Опция месяца

    # === КНОПКИ УПРАВЛЕНИЯ ===
    TODAY_BUTTON = ".react-datepicker__today-button"  # Кнопка "Сегодня"
    CLEAR_BUTTON = ".react-datepicker__close-icon"  # Кнопка очистки
    CALENDAR_ICON = ".react-datepicker__calendar-icon"  # Иконка календаря

    # === ПОРТАЛ И ПОЗИЦИОНИРОВАНИЕ ===
    PORTAL = ".react-datepicker__portal"  # Портал календаря
    TRIANGLE = ".react-datepicker__triangle"  # Треугольник указателя

    # === КАСТОМИЗАЦИЯ ===
    CUSTOM_HEADER = ".react-datepicker__header--custom"  # Кастомный заголовок
    CUSTOM_DAY = ".react-datepicker__day--custom"  # Кастомный день

    # === RANGE PICKER (если есть) ===
    START_DATE = ".react-datepicker__day--range-start"  # Начало диапазона
    END_DATE = ".react-datepicker__day--range-end"  # Конец диапазона
    IN_RANGE = ".react-datepicker__day--in-range"  # День в диапазоне

    # === ВВОД ЗНАЧЕНИЙ ===
    INPUT_CONTAINER = ".react-datepicker__input-container"  # Контейнер input
    TAB_LOOP = ".react-datepicker__tab-loop"  # Цикл табуляции

    # === ДОСТУПНОСТЬ ===
    ARIA_LABEL = "[aria-label]"  # Элементы с aria-label
    ARIA_SELECTED = "[aria-selected='true']"  # Выбранные элементы
    ROLE_BUTTON = "[role='button']"  # Кнопки для скринридеров
