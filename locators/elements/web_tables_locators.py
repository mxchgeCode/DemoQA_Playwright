"""
Локаторы для страницы Web Tables.

Содержит все селекторы для взаимодействия с веб-таблицами,
включая поиск, добавление, редактирование, удаление записей и пагинацию.
"""

from dataclasses import dataclass


@dataclass
class WebTablesLocators:
    """
    Класс локаторов для страницы Web Tables.

    Содержит CSS селекторы для всех элементов веб-таблицы:
    - Поиск и фильтрация записей
    - Добавление новых записей
    - Редактирование существующих записей
    - Удаление записей
    - Пагинация и навигация
    - Сортировка столбцов
    """

    # === ОСНОВНЫЕ ЭЛЕМЕНТЫ ТАБЛИЦЫ ===

    # Контейнер всей таблицы
    TABLE_CONTAINER: str = ".rt-table"

    # Заголовки столбцов таблицы
    TABLE_HEADERS: str = ".rt-thead .rt-th"

    # Все строки таблицы (включая заголовки)
    TABLE_ROWS: str = ".rt-tr-group"

    # Строки с данными (исключая заголовки)
    TABLE_DATA_ROWS: str = ".rt-tr-group .rt-tr"

    # Ячейки таблицы
    TABLE_CELLS: str = ".rt-td"

    # Тело таблицы
    TABLE_BODY: str = ".rt-tbody"

    # === ПОИСК И ФИЛЬТРАЦИЯ ===

    # Поле поиска
    SEARCH_INPUT: str = "#searchBox"
    SEARCH_BOX: str = "#searchBox"  # Добавляем отсутствующий локатор

    # Кнопка очистки поиска
    SEARCH_CLEAR: str = ".search-clear"

    # Результаты поиска
    SEARCH_RESULTS: str = ".rt-tr-group:not([style*='display: none'])"

    # Пустые результаты поиска
    NO_RESULTS: str = ".rt-noData"

    # === ДОБАВЛЕНИЕ ЗАПИСЕЙ ===

    # Кнопка добавления новой записи
    ADD_BUTTON: str = "#addNewRecordButton"

    # Форма регистрации/добавления
    REGISTRATION_FORM: str = ".modal-content"

    # Заголовок формы
    FORM_TITLE: str = "#registration-form-modal"

    # === ПОЛЯ ФОРМЫ ===

    # Поле имени
    FIRST_NAME_INPUT: str = "#firstName"

    # Поле фамилии
    LAST_NAME_INPUT: str = "#lastName"

    # Поле email
    EMAIL_INPUT: str = "#userEmail"

    # Поле возраста
    AGE_INPUT: str = "#age"

    # Поле зарплаты
    SALARY_INPUT: str = "#salary"

    # Поле отдела
    DEPARTMENT_INPUT: str = "#department"

    # === КНОПКИ ФОРМЫ ===

    # Кнопка отправки формы
    SUBMIT_BUTTON: str = "#submit"

    # Кнопка закрытия формы
    CLOSE_BUTTON: str = ".close"

    # Кнопка отмены
    CANCEL_BUTTON: str = ".btn-light"

    # === ДЕЙСТВИЯ СО ЗАПИСЯМИ ===

    # Кнопки редактирования (иконки карандаша)
    EDIT_BUTTONS: str = "[title='Edit']"

    # Кнопки удаления (иконки корзины)
    DELETE_BUTTONS: str = "[title='Delete']"

    # Конкретная кнопка редактирования
    EDIT_BUTTON: str = "span[title='Edit']"

    # Конкретная кнопка удаления
    DELETE_BUTTON: str = "span[title='Delete']"

    # Строка с конкретной записью для удаления
    DELETE_ROW: str = ".rt-tr-group"

    # === СТОЛБЦЫ ТАБЛИЦЫ ===

    # Столбец имени (1-й столбец)
    FIRST_NAME_COLUMN: str = ".rt-td:nth-child(1)"

    # Столбец фамилии (2-й столбец)
    LAST_NAME_COLUMN: str = ".rt-td:nth-child(2)"

    # Столбец возраста (3-й столбец)
    AGE_COLUMN: str = ".rt-td:nth-child(3)"

    # Столбец email (4-й столбец)
    EMAIL_COLUMN: str = ".rt-td:nth-child(4)"

    # Столбец зарплаты (5-й столбец)
    SALARY_COLUMN: str = ".rt-td:nth-child(5)"

    # Столбец отдела (6-й столбец)
    DEPARTMENT_COLUMN: str = ".rt-td:nth-child(6)"

    # Столбец действий (7-й столбец)
    ACTION_COLUMN: str = ".rt-td:nth-child(7)"

    # === СОРТИРОВКА ===

    # Сортируемые заголовки столбцов
    SORTABLE_HEADERS: str = ".rt-th[role='columnheader']"

    # Индикатор сортировки по возрастанию
    SORT_ASC: str = ".sort-asc"

    # Индикатор сортировки по убыванию
    SORT_DESC: str = ".sort-desc"

    # === ПАГИНАЦИЯ ===

    # Контейнер пагинации
    PAGINATION_CONTAINER: str = ".pagination"

    # Кнопки номеров страниц
    PAGE_BUTTONS: str = ".page-link"

    # Активная страница
    ACTIVE_PAGE: str = ".page-item.active .page-link"

    # Кнопка "Предыдущая страница"
    PREVIOUS_PAGE: str = ".page-item .page-link[aria-label='Previous']"

    # Кнопка "Следующая страница"
    NEXT_PAGE: str = ".page-item .page-link[aria-label='Next']"

    # Первая страница
    FIRST_PAGE: str = ".page-item:first-child .page-link"

    # Последняя страница
    LAST_PAGE: str = ".page-item:last-child .page-link"

    # === ИНФОРМАЦИЯ О ТАБЛИЦЕ ===

    # Показано записей на странице
    RECORDS_INFO: str = ".records-info"

    # Общее количество записей
    TOTAL_RECORDS: str = ".total-records"

    # Размер страницы (записей на странице)
    PAGE_SIZE_SELECT: str = ".page-size-select"

    # === СОСТОЯНИЯ ЭЛЕМЕНТОВ ===

    # Загрузка таблицы
    LOADING_INDICATOR: str = ".loading"

    # Пустая таблица
    EMPTY_TABLE: str = ".empty-table"

    # Ошибка загрузки
    ERROR_MESSAGE: str = ".error-message"

    # === ВАЛИДАЦИЯ ФОРМЫ ===

    # Сообщения об ошибках валидации
    VALIDATION_ERRORS: str = ".validation-error"

    # Обязательные поля
    REQUIRED_FIELDS: str = ".required"

    # Поля с ошибками
    INVALID_FIELDS: str = ".is-invalid"

    # === МОДАЛЬНЫЕ ОКНА ===

    # Модальное окно формы
    FORM_MODAL: str = ".modal"

    # Overlay модального окна
    MODAL_BACKDROP: str = ".modal-backdrop"

    # Содержимое модального окна
    MODAL_CONTENT: str = ".modal-content"

    # Заголовок модального окна
    MODAL_HEADER: str = ".modal-header"

    # Тело модального окна
    MODAL_BODY: str = ".modal-body"

    # Футер модального окна
    MODAL_FOOTER: str = ".modal-footer"

    # === ДОПОЛНИТЕЛЬНЫЕ ЭЛЕМЕНТЫ ===

    # Чекбоксы выбора записей
    ROW_CHECKBOXES: str = ".row-checkbox"

    # Чекбокс выбора всех записей
    SELECT_ALL_CHECKBOX: str = ".select-all"

    # Кнопки массовых действий
    BULK_ACTIONS: str = ".bulk-actions"

    # Экспорт данных
    EXPORT_BUTTON: str = ".export-btn"

    # Импорт данных
    IMPORT_BUTTON: str = ".import-btn"

    # === ФИЛЬТРЫ ===

    # Контейнер фильтров
    FILTERS_CONTAINER: str = ".filters"

    # Фильтр по отделу
    DEPARTMENT_FILTER: str = ".department-filter"

    # Фильтр по возрасту
    AGE_FILTER: str = ".age-filter"

    # Фильтр по зарплате
    SALARY_FILTER: str = ".salary-filter"

    # Кнопка сброса фильтров
    RESET_FILTERS: str = ".reset-filters"

    # Применить фильтры
    APPLY_FILTERS: str = ".apply-filters"
