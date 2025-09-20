"""
Локаторы для страницы Broken Links - Images.

Содержит все селекторы для взаимодействия с изображениями и ссылками,
включая валидные и поврежденные элементы для тестирования.
"""

from dataclasses import dataclass


@dataclass
class BrokenLinksLocators:
    """
    Класс локаторов для страницы Broken Links - Images.

    Содержит CSS селекторы для всех элементов страницы:
    - Валидные и поврежденные изображения
    - Валидные и поврежденные ссылки
    - Общие селекторы для анализа всех элементов
    """

    # === ИЗОБРАЖЕНИЯ ===

    # Все изображения на странице
    ALL_IMAGES: str = "img"

    # Валидное изображение (рабочее)
    VALID_IMAGE: str = "img[src*='valid']"

    # Поврежденное изображение
    BROKEN_IMAGE: str = "img[src*='broken']"

    # Альтернативные селекторы для изображений
    VALID_IMAGE_ALT: str = "img:first-of-type"
    BROKEN_IMAGE_ALT: str = "img:last-of-type"

    # Изображения по атрибутам
    IMAGES_WITH_ALT: str = "img[alt]"
    IMAGES_WITHOUT_ALT: str = "img:not([alt])"

    # === ССЫЛКИ ===

    # Все ссылки на странице
    ALL_LINKS: str = "a"

    # Валидная ссылка (рабочая)
    VALID_LINK: str = "a[href*='valid']"

    # Поврежденная ссылка
    BROKEN_LINK: str = "a[href*='broken']"

    # Альтернативные селекторы для ссылок
    VALID_LINK_ALT: str = "a:contains('Valid Link')"
    BROKEN_LINK_ALT: str = "a:contains('Broken Link')"

    # Ссылки по типам
    EXTERNAL_LINKS: str = "a[href^='http']"
    INTERNAL_LINKS: str = "a[href^='/'], a[href^='./'], a[href^='../']"
    EMAIL_LINKS: str = "a[href^='mailto:']"
    PHONE_LINKS: str = "a[href^='tel:']"

    # === КОНТЕЙНЕРЫ И РАЗДЕЛЫ ===

    # Основной контейнер страницы
    MAIN_CONTAINER: str = ".main-content"

    # Контейнер с изображениями
    IMAGES_SECTION: str = ".images-section"

    # Контейнер со ссылками
    LINKS_SECTION: str = ".links-section"

    # Демонстрационная область
    DEMO_AREA: str = ".demo-area"

    # === ЗАГОЛОВКИ И ОПИСАНИЯ ===

    # Заголовок страницы
    PAGE_TITLE: str = "h1"

    # Подзаголовки
    SECTION_HEADERS: str = "h2, h3"

    # Описание функциональности
    DESCRIPTION: str = ".description"

    # Инструкции для пользователя
    INSTRUCTIONS: str = ".instructions"

    # === СТАТУСЫ И ИНДИКАТОРЫ ===

    # Индикаторы статуса загрузки
    LOADING_INDICATOR: str = ".loading"

    # Индикаторы ошибок
    ERROR_INDICATOR: str = ".error"

    # Индикаторы успешной загрузки
    SUCCESS_INDICATOR: str = ".success"

    # Предупреждения
    WARNING_INDICATOR: str = ".warning"

    # === РЕЗУЛЬТАТЫ ПРОВЕРОК ===

    # Результаты проверки изображений
    IMAGE_CHECK_RESULTS: str = ".image-check-result"

    # Результаты проверки ссылок
    LINK_CHECK_RESULTS: str = ".link-check-result"

    # Общие результаты
    OVERALL_RESULTS: str = ".overall-results"

    # === ДОПОЛНИТЕЛЬНЫЕ ЭЛЕМЕНТЫ ===

    # Кнопки действий
    ACTION_BUTTONS: str = ".action-btn"

    # Кнопка проверки изображений
    CHECK_IMAGES_BUTTON: str = "#checkImages"

    # Кнопка проверки ссылок
    CHECK_LINKS_BUTTON: str = "#checkLinks"

    # Кнопка полной проверки
    CHECK_ALL_BUTTON: str = "#checkAll"

    # === ТАБЛИЦЫ РЕЗУЛЬТАТОВ ===

    # Таблица с результатами
    RESULTS_TABLE: str = ".results-table"

    # Заголовки таблицы
    TABLE_HEADERS: str = ".results-table th"

    # Строки таблицы
    TABLE_ROWS: str = ".results-table tr"

    # Ячейки таблицы
    TABLE_CELLS: str = ".results-table td"

    # === ФИЛЬТРЫ И СОРТИРОВКА ===

    # Фильтры результатов
    RESULT_FILTERS: str = ".result-filter"

    # Фильтр по статусу
    STATUS_FILTER: str = ".status-filter"

    # Фильтр по типу элемента
    TYPE_FILTER: str = ".type-filter"

    # Сортировка результатов
    SORT_OPTIONS: str = ".sort-option"

    # === ЭКСПОРТ И ОТЧЕТЫ ===

    # Кнопки экспорта
    EXPORT_BUTTONS: str = ".export-btn"

    # Экспорт в CSV
    EXPORT_CSV: str = ".export-csv"

    # Экспорт в JSON
    EXPORT_JSON: str = ".export-json"

    # Печать отчета
    PRINT_REPORT: str = ".print-report"

    # === НАСТРОЙКИ ПРОВЕРКИ ===

    # Панель настроек
    SETTINGS_PANEL: str = ".settings-panel"

    # Таймаут запросов
    TIMEOUT_SETTING: str = "#requestTimeout"

    # Количество попыток
    RETRY_SETTING: str = "#retryCount"

    # Проверка редиректов
    FOLLOW_REDIRECTS: str = "#followRedirects"

    # === ПРОГРЕСС И СТАТИСТИКА ===

    # Индикатор прогресса
    PROGRESS_BAR: str = ".progress-bar"

    # Процент выполнения
    PROGRESS_PERCENTAGE: str = ".progress-percentage"

    # Счетчик проверенных элементов
    CHECKED_COUNTER: str = ".checked-counter"

    # Счетчик ошибок
    ERROR_COUNTER: str = ".error-counter"

    # === ДЕТАЛИ ЭЛЕМЕНТОВ ===

    # Подробная информация об изображении
    IMAGE_DETAILS: str = ".image-details"

    # Размеры изображения
    IMAGE_DIMENSIONS: str = ".image-dimensions"

    # Размер файла изображения
    IMAGE_FILE_SIZE: str = ".image-file-size"

    # HTTP статус изображения
    IMAGE_HTTP_STATUS: str = ".image-http-status"

    # Подробная информация о ссылке
    LINK_DETAILS: str = ".link-details"

    # HTTP статус ссылки
    LINK_HTTP_STATUS: str = ".link-http-status"

    # Время ответа ссылки
    LINK_RESPONSE_TIME: str = ".link-response-time"

    # Редиректы ссылки
    LINK_REDIRECTS: str = ".link-redirects"

    # === УВЕДОМЛЕНИЯ ===

    # Область уведомлений
    NOTIFICATIONS_AREA: str = ".notifications"

    # Уведомления об успехе
    SUCCESS_NOTIFICATIONS: str = ".notification.success"

    # Уведомления об ошибках
    ERROR_NOTIFICATIONS: str = ".notification.error"

    # Предупреждающие уведомления
    WARNING_NOTIFICATIONS: str = ".notification.warning"

    # Информационные уведомления
    INFO_NOTIFICATIONS: str = ".notification.info"
