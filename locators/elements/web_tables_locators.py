"""
Локаторы для страницы Web Tables.
Содержит селекторы для интерактивной таблицы с CRUD операциями.
"""


class WebTablesLocators:
    """CSS селекторы для элементов страницы Web Tables."""

    # === УПРАВЛЕНИЕ ТАБЛИЦЕЙ ===
    ADD_BUTTON = "#addNewRecordButton"  # Добавить новую запись
    SEARCH_BOX = "#searchBox"  # Поле поиска по таблице

    # === ФОРМА РЕГИСТРАЦИИ/РЕДАКТИРОВАНИЯ ===
    REGISTRATION_FORM = ".modal-content"  # Модальная форма
    FIRST_NAME_INPUT = "#firstName"  # Поле ввода имени
    LAST_NAME_INPUT = "#lastName"  # Поле ввода фамилии
    EMAIL_INPUT = "#userEmail"  # Поле ввода email
    AGE_INPUT = "#age"  # Поле ввода возраста
    SALARY_INPUT = "#salary"  # Поле ввода зарплаты
    DEPARTMENT_INPUT = "#department"  # Поле ввода отдела
    SUBMIT_BUTTON = "#submit"  # Кнопка отправки формы

    # === СТРУКТУРА ТАБЛИЦЫ ===
    TABLE_CONTAINER = ".rt-table"  # Контейнер таблицы
    TABLE_HEADER = ".rt-thead"  # Заголовок таблицы
    TABLE_BODY = ".rt-tbody"  # Тело таблицы
    TABLE_ROWS = ".rt-tr-group"  # Строки таблицы
    TABLE_CELLS = ".rt-td"  # Ячейки таблицы

    # === ДЕЙСТВИЯ СО СТРОКАМИ ===
    EDIT_BUTTON = "span[title='Edit']"  # Кнопка редактирования записи
    DELETE_BUTTON = "span[title='Delete']"  # Кнопка удаления записи

    # Шаблоны селекторов для конкретных строк
    DELETE_BUTTON_TEMPLATE = "span[title='Delete'][data-row-id='{}']"  # Удаление по ID
    EDIT_BUTTON_TEMPLATE = (
        "span[title='Edit'][data-row-id='{}']"  # Редактирование по ID
    )
    ROW_BY_INDEX_TEMPLATE = ".rt-tr-group:nth-child({})"  # Строка по индексу

    # === СОДЕРЖИМОЕ ЯЧЕЕК (по колонкам) ===
    FIRST_NAME_COLUMN = ".rt-td:nth-child(1)"  # Колонка имени
    LAST_NAME_COLUMN = ".rt-td:nth-child(2)"  # Колонка фамилии
    AGE_COLUMN = ".rt-td:nth-child(3)"  # Колонка возраста
    EMAIL_COLUMN = ".rt-td:nth-child(4)"  # Колонка email
    SALARY_COLUMN = ".rt-td:nth-child(5)"  # Колонка зарплаты
    DEPARTMENT_COLUMN = ".rt-td:nth-child(6)"  # Колонка отдела
    ACTION_COLUMN = ".rt-td:nth-child(7)"  # Колонка действий

    # === ПАГИНАЦИЯ (если есть) ===
    PAGINATION_CONTAINER = ".pagination"  # Контейнер пагинации
    NEXT_PAGE_BUTTON = ".-next button"  # Следующая страница
    PREV_PAGE_BUTTON = ".-previous button"  # Предыдущая страница
    PAGE_INFO = ".-pageInfo"  # Информация о странице

    # === ДОПОЛНИТЕЛЬНЫЕ ЭЛЕМЕНТЫ ===
    NO_DATA_MESSAGE = ".rt-noData"  # Сообщение "No rows found"
    LOADING_INDICATOR = ".-loading"  # Индикатор загрузки

    # === ЗАКРЫТИЕ ФОРМЫ ===
    MODAL_CLOSE_X = ".modal-header .close"  # Кнопка X закрытия модали
    MODAL_CLOSE_BUTTON = ".modal-footer .btn-secondary"  # Кнопка Close
