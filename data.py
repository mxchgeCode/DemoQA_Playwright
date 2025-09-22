"""
Централизованные данные проекта: URL'ы, константы, тестовые данные.
"""

# Гибридные структуры для одновременной поддержки доступа по ключам и по атрибутам
class _Hybrid:
    def __init__(self, data: dict):
        # Преобразуем вложенные словари в _Hybrid рекурсивно
        for k, v in data.items():
            if isinstance(v, dict):
                v = _Hybrid(v)
            setattr(self, k, v)
        # Сохраняем оригинальный словарь для []-доступа
        self._data = {k: getattr(self, k) for k in data.keys()}

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def items(self):
        return self._data.items()

    def get(self, key, default=None):
        return self._data.get(key, default)


class URLs:
    """Константы URL'ов для всех страниц приложения."""

    # Базовый URL
    BASE_URL = "https://demoqa.com"

    # Elements
    TEXT_BOX = f"{BASE_URL}/text-box"
    CHECK_BOX = f"{BASE_URL}/checkbox"
    RADIO_BUTTON = f"{BASE_URL}/radio-button"
    WEB_TABLES = f"{BASE_URL}/webtables"
    BUTTONS = f"{BASE_URL}/buttons"
    LINKS_PAGE = f"{BASE_URL}/links"
    BROKEN_LINKS = f"{BASE_URL}/broken"
    DOWNLOAD = f"{BASE_URL}/upload-download"
    DYNAMIC = f"{BASE_URL}/dynamic-properties"

    # Forms
    PRACTICE_FORM = f"{BASE_URL}/automation-practice-form"

    # Alerts, Frame & Windows
    BROWSER_WINDOWS = f"{BASE_URL}/browser-windows"
    ALERTS_PAGE = f"{BASE_URL}/alerts"
    FRAMES_PAGE = f"{BASE_URL}/frames"
    NESTED_FRAMES_PAGE = f"{BASE_URL}/nestedframes"
    MODAL_DIALOGS = f"{BASE_URL}/modal-dialogs"

    # Widgets
    ACCORDION = f"{BASE_URL}/accordian"
    AUTO_COMPLETE = f"{BASE_URL}/auto-complete"
    DATE_PICKER = f"{BASE_URL}/date-picker"
    SLIDER = f"{BASE_URL}/slider"
    PROGRESS_BAR = f"{BASE_URL}/progress-bar"
    TABS = f"{BASE_URL}/tabs"
    TOOL_TIPS = f"{BASE_URL}/tool-tips"
    MENU = f"{BASE_URL}/menu"
    SELECT_MENU = f"{BASE_URL}/select-menu"

    # Interactions
    SORTABLE = f"{BASE_URL}/sortable"
    SELECTABLE = f"{BASE_URL}/selectable"
    RESIZABLE = f"{BASE_URL}/resizable"
    DROPPABLE = f"{BASE_URL}/droppable"
    DRAGABBLE = f"{BASE_URL}/dragabble"

    # Book Store Application
    LOGIN_PAGE = f"{BASE_URL}/login"
    BOOKS = f"{BASE_URL}/books"
    PROFILE = f"{BASE_URL}/profile"
    BOOK_STORE_API = f"{BASE_URL}/BookStore/v1"


class TestData:
    """Тестовые данные для различных форм и полей."""

    # Данные пользователя: гибрид поддерживает и USERS["valid_user"]["first_name"],
    # и USERS.valid_user.first_name, и USERS.test_user.username
    USERS = _Hybrid(
        {
            "valid_user": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "age": "30",
                "salary": "75000",
                "department": "Engineering",
            },
            "test_user": {
                "username": "testuser",
                "password": "TestPassword123!",
                "first_name": "Test",
                "last_name": "User",
            },
        }
    )

    # Данные для форм
    FORM_DATA = {
        "practice_form": {
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice.johnson@test.com",
            "gender": "Female",
            "mobile": "1234567890",
            "subjects": ["Math", "Physics"],
            "hobbies": ["Sports", "Reading"],
            "current_address": "123 Main Street, Test City",
            "state": "NCR",
            "city": "Delhi",
        }
    }

    # Файлы для тестирования
    FILES = {
        "sample_image": "test_files/sample.jpg",
        "sample_document": "test_files/sample.pdf",
        "large_file": "test_files/large_file.txt",
    }

    # API ответы
    API_RESPONSES = {
        "created": "Link has responded with staus 201 and status text Created",
        "no_content": "Link has responded with staus 204 and status text No Content",
        "moved": "Link has responded with staus 301 and status text Moved Permanently",
        "bad_request": "Link has responded with staus 400 and status text Bad Request",
        "unauthorized": "Link has responded with staus 401 and status text Unauthorized",
        "forbidden": "Link has responded with staus 403 and status text Forbidden",
        "not_found": "Link has responded with staus 404 and status text Not Found",
    }


class Colors:
    """Цветовые константы для проверок."""

    # Hex цвета
    RED = "#dc3545"
    GREEN = "#28a745"
    BLUE = "#007bff"
    YELLOW = "#ffc107"
    WHITE = "#ffffff"
    BLACK = "#000000"

    # RGB цвета
    RED_RGB = "rgb(220, 53, 69)"
    GREEN_RGB = "rgb(40, 167, 69)"
    BLUE_RGB = "rgb(0, 123, 255)"


class Timeouts:
    """Константы таймаутов для различных операций."""

    SHORT = 3000  # 3 секунды
    MEDIUM = 10000  # 10 секунд
    LONG = 30000  # 30 секунд
    UPLOAD = 60000  # 60 секунд для загрузки файлов

    # Специальные таймауты
    ANIMATION = 1000  # Ожидание анимации
    TOOLTIP = 2000  # Ожидание tooltip
    MODAL = 5000  # Ожидание модального окна
