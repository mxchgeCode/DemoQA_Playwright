"""
Локаторы для страницы Upload and Download.
Содержит селекторы для загрузки и скачивания файлов.
"""


class UploadDownloadLocators:
    """CSS селекторы для элементов страницы Upload and Download."""

    # === ЗАГРУЗКА ФАЙЛОВ ===
    UPLOAD_INPUT = "#uploadFile"                      # Input для выбора файла
    UPLOAD_PATH_TEXT = "#uploadedFilePath"            # Отображение пути загруженного файла

    # === СКАЧИВАНИЕ ФАЙЛОВ ===
    DOWNLOAD_BUTTON = "a#downloadButton"              # Кнопка для скачивания файла

    # === ДОПОЛНИТЕЛЬНЫЕ СЕЛЕКТОРЫ ===
    UPLOAD_CONTAINER = ".upload-download-wrapper"     # Контейнер всей секции
    UPLOAD_LABEL = "label[for='uploadFile']"          # Лейбл для input файла
    DOWNLOAD_SECTION = ".download-section"             # Секция скачивания

    # === СООБЩЕНИЯ И ИНДИКАТОРЫ ===
    SUCCESS_MESSAGE = ".alert-success"                 # Сообщение об успешной загрузке
    ERROR_MESSAGE = ".alert-danger"                    # Сообщение об ошибке
    PROGRESS_BAR = ".progress-bar"                     # Индикатор прогресса загрузки

    # === АТРИБУТЫ ФАЙЛОВ ===
    FILE_SIZE_INFO = ".file-size-info"                # Информация о размере файла
    FILE_TYPE_INFO = ".file-type-info"                # Информация о типе файла
