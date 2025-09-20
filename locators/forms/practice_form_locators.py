"""
Локаторы для страницы Practice Form.
Содержит селекторы для полной формы регистрации с различными типами полей.
"""


class AutomationPracticeFormLocators:
    """CSS селекторы для элементов страницы Practice Form."""

    # === ОСНОВНАЯ СТРУКТУРА ФОРМЫ ===
    FORM_CONTAINER = "#userForm"                      # Основной контейнер формы

    # === ОСНОВНЫЕ ПОЛЯ ВВОДА ===
    FIRST_NAME_INPUT = "#firstName"                   # Поле ввода имени
    LAST_NAME_INPUT = "#lastName"                     # Поле ввода фамилии
    EMAIL_INPUT = "#userEmail"                        # Поле ввода email
    MOBILE_INPUT = "#userNumber"                      # Поле ввода номера телефона

    # === ПОЛ (РАДИО КНОПКИ) ===
    GENDER_RADIOS = "input[name='gender']"            # Все радио кнопки пола
    MALE_GENDER = "label[for='gender-radio-1']"       # Мужской пол
    FEMALE_GENDER = "label[for='gender-radio-2']"     # Женский пол
    OTHER_GENDER = "label[for='gender-radio-3']"      # Другой пол

    # === ДАТА РОЖДЕНИЯ ===
    DATE_OF_BIRTH_INPUT = "#dateOfBirthInput"         # Поле выбора даты рождения
    DATE_PICKER = ".react-datepicker"                 # Календарь для выбора даты
    DATE_MONTH_SELECT = ".react-datepicker__month-select" # Dropdown выбора месяца
    DATE_YEAR_SELECT = ".react-datepicker__year-select"   # Dropdown выбора года
    DATE_DAY = ".react-datepicker__day"               # Дни в календаре

    # === ПРЕДМЕТЫ (АВТОКОМПЛИТ) ===
    SUBJECTS_INPUT = "#subjectsInput"                 # Поле ввода предметов
    SUBJECTS_DROPDOWN = ".subjects-auto-complete__menu" # Dropdown предметов
    SUBJECTS_OPTION = ".subjects-auto-complete__option" # Опции предметов
    SUBJECTS_MULTI_VALUE = ".subjects-auto-complete__multi-value" # Выбранные предметы

    # === ХОББИ (ЧЕКБОКСЫ) ===
    HOBBIES_CHECKBOXES = "input[type='checkbox']"     # Все чекбоксы хобби
    SPORTS_HOBBY = "label[for='hobbies-checkbox-1']"  # Спорт
    READING_HOBBY = "label[for='hobbies-checkbox-2']" # Чтение
    MUSIC_HOBBY = "label[for='hobbies-checkbox-3']"   # Музыка

    # === ЗАГРУЗКА ИЗОБРАЖЕНИЯ ===
    PICTURE_UPLOAD_INPUT = "#uploadPicture"           # Input для загрузки файла
    UPLOAD_LABEL = "label[for='uploadPicture']"       # Лейбл для загрузки

    # === АДРЕС ===
    CURRENT_ADDRESS_TEXTAREA = "#currentAddress"     # Текстовое поле адреса

    # === ШТАТ И ГОРОД (DROPDOWN) ===
    STATE_DROPDOWN = "#state"                         # Dropdown выбора штата
    STATE_CONTAINER = "#state .css-1hwfws3"          # Контейнер штата
    CITY_DROPDOWN = "#city"                          # Dropdown выбора города
    CITY_CONTAINER = "#city .css-1hwfws3"            # Контейнер города

    # === КНОПКА ОТПРАВКИ ===
    SUBMIT_BUTTON = "#submit"                         # Кнопка отправки формы

    # === МОДАЛЬНОЕ ОКНО РЕЗУЛЬТАТА ===
    MODAL_DIALOG = ".modal-content"                   # Модальное окно с результатами
    MODAL_TITLE = ".modal-title"                      # Заголовок модального окна
    MODAL_BODY = ".modal-body"                        # Тело модального окна
    MODAL_TABLE = ".table"                            # Таблица с результатами
    MODAL_CLOSE_BUTTON = "#closeLargeModal"           # Кнопка закрытия модального окна

    # === ВАЛИДАЦИЯ И ОШИБКИ ===
    REQUIRED_FIELD = ".was-validated .form-control:invalid" # Невалидные обязательные поля
    VALID_FIELD = ".was-validated .form-control:valid"      # Валидные поля
    ERROR_MESSAGE = ".invalid-feedback"               # Сообщения об ошибках

    # === ДОПОЛНИТЕЛЬНЫЕ СЕЛЕКТОРЫ ===
    FORM_LABEL = ".form-label"                        # Лейблы полей формы
    FORM_GROUP = ".form-group"                        # Группы полей
    REQUIRED_ASTERISK = ".text-danger"                # Звездочки обязательных полей
