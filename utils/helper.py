"""
Вспомогательные утилиты для автоматизированных тестов.
Содержит общие функции для работы с данными, файлами и проверками.
"""

import os
import json
import random
import string
import time
from typing import Dict, List, Any
from datetime import datetime, timedelta


class DataGenerator:
    """Генератор тестовых данных для различных сценариев."""

    @staticmethod
    def random_string(
        length: int = 10, include_digits: bool = True, include_symbols: bool = False
    ) -> str:
        """
        Генерирует случайную строку заданной длины.

        Args:
            length: Длина генерируемой строки
            include_digits: Включать ли цифры
            include_symbols: Включать ли специальные символы

        Returns:
            str: Случайная строка
        """
        chars = string.ascii_letters
        if include_digits:
            chars += string.digits
        if include_symbols:
            chars += "!@#$%^&*"

        return "".join(random.choice(chars) for _ in range(length))

    @staticmethod
    def random_email(domain: str = "example.com") -> str:
        """
        Генерирует случайный email адрес.

        Args:
            domain: Домен для email

        Returns:
            str: Случайный email адрес
        """
        username = DataGenerator.random_string(8).lower()
        return f"{username}@{domain}"

    @staticmethod
    def random_phone() -> str:
        """
        Генерирует случайный номер телефона.

        Returns:
            str: Номер телефона в формате 1234567890
        """
        return "".join(random.choice(string.digits) for _ in range(10))

    @staticmethod
    def random_address() -> Dict[str, str]:
        """
        Генерирует случайный адрес.

        Returns:
            dict: Словарь с компонентами адреса
        """
        streets = ["Main St", "Oak Ave", "Pine Rd", "Elm Dr", "Maple Ln"]
        cities = ["Springfield", "Madison", "Franklin", "Georgetown", "Clinton"]
        states = ["NY", "CA", "TX", "FL", "IL"]

        return {
            "street": f"{random.randint(100, 9999)} {random.choice(streets)}",
            "city": random.choice(cities),
            "state": random.choice(states),
            "zip": str(random.randint(10000, 99999)),
            "full": f"{random.randint(100, 9999)} {random.choice(streets)}, {random.choice(cities)}, {random.choice(states)} {random.randint(10000, 99999)}",
        }

    @staticmethod
    def random_date(start_date: datetime = None, end_date: datetime = None) -> datetime:
        """
        Генерирует случайную дату в указанном диапазоне.

        Args:
            start_date: Начальная дата (по умолчанию 1 год назад)
            end_date: Конечная дата (по умолчанию сегодня)

        Returns:
            datetime: Случайная дата
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()

        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)

        return start_date + timedelta(days=random_days)


class FileManager:
    """Менеджер для работы с файлами в тестах."""

    @staticmethod
    def create_test_file(
        filename: str, content: str, directory: str = "test_files"
    ) -> str:
        """
        Создает тестовый файл с указанным содержимым.

        Args:
            filename: Имя файла
            content: Содержимое файла
            directory: Директория для сохранения

        Returns:
            str: Полный путь к созданному файлу
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return file_path

    @staticmethod
    def create_test_image(
        filename: str, size: tuple = (100, 100), directory: str = "test_files"
    ) -> str:
        """
        Создает тестовое изображение.

        Args:
            filename: Имя файла изображения
            size: Размер изображения (ширина, высота)
            directory: Директория для сохранения

        Returns:
            str: Путь к созданному изображению
        """
        try:
            from PIL import Image, ImageDraw

            if not os.path.exists(directory):
                os.makedirs(directory)

            # Создаем простое цветное изображение
            image = Image.new(
                "RGB",
                size,
                color=(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                ),
            )
            draw = ImageDraw.Draw(image)

            # Добавляем простой текст
            draw.text((10, 10), "TEST", fill=(255, 255, 255))

            file_path = os.path.join(directory, filename)
            image.save(file_path)

            return file_path
        except ImportError:
            # Если PIL недоступен, создаем пустой файл
            return FileManager.create_test_file(
                filename, "Fake image content", directory
            )

    @staticmethod
    def cleanup_test_files(directory: str = "test_files") -> None:
        """
        Очищает директорию с тестовыми файлами.

        Args:
            directory: Директория для очистки
        """
        if os.path.exists(directory):
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)


class ValidationHelper:
    """Помощник для валидации данных в тестах."""

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Проверяет валидность email адреса.

        Args:
            email: Email для проверки

        Returns:
            bool: True если email валиден
        """
        import re

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """
        Проверяет валидность номера телефона.

        Args:
            phone: Номер телефона для проверки

        Returns:
            bool: True если номер валиден
        """
        import re

        # Простая проверка на 10 цифр
        pattern = r"^\d{10}$"
        return bool(
            re.match(
                pattern,
                phone.replace("-", "")
                .replace(" ", "")
                .replace("(", "")
                .replace(")", ""),
            )
        )

    @staticmethod
    def compare_strings_ignore_case(str1: str, str2: str) -> bool:
        """
        Сравнивает строки без учета регистра.

        Args:
            str1: Первая строка
            str2: Вторая строка

        Returns:
            bool: True если строки одинаковы
        """
        return str1.lower().strip() == str2.lower().strip()

    @staticmethod
    def contains_all_words(text: str, words: List[str]) -> bool:
        """
        Проверяет, содержит ли текст все указанные слова.

        Args:
            text: Текст для проверки
            words: Список слов для поиска

        Returns:
            bool: True если все слова найдены
        """
        text_lower = text.lower()
        return all(word.lower() in text_lower for word in words)


class WaitHelper:
    """Помощник для ожиданий в тестах."""

    @staticmethod
    def wait_for_condition(
        condition_func, timeout: int = 10, interval: float = 0.5
    ) -> bool:
        """
        Ждет выполнения условия с заданным интервалом.

        Args:
            condition_func: Функция условия (должна возвращать bool)
            timeout: Максимальное время ожидания в секундах
            interval: Интервал проверки в секундах

        Returns:
            bool: True если условие выполнилось в указанное время
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)

        return False

    @staticmethod
    def wait_and_retry(action_func, retry_count: int = 3, delay: float = 1.0):
        """
        Выполняет действие с повторными попытками.

        Args:
            action_func: Функция для выполнения
            retry_count: Количество попыток
            delay: Задержка между попытками

        Returns:
            Результат выполнения функции

        Raises:
            Exception: Последнее исключение если все попытки неуспешны
        """
        last_exception = None

        for attempt in range(retry_count):
            try:
                return action_func()
            except Exception as e:
                last_exception = e
                if attempt < retry_count - 1:
                    time.sleep(delay)

        if last_exception:
            raise last_exception


class TestDataManager:
    """Менеджер тестовых данных с сохранением в JSON."""

    def __init__(self, data_file: str = "test_data.json"):
        """
        Инициализация менеджера.

        Args:
            data_file: Путь к файлу с данными
        """
        self.data_file = data_file
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """Загружает данные из файла."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {}

    def save_data(self) -> None:
        """Сохраняет данные в файл."""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get_test_data(self, test_name: str, default: Any = None) -> Any:
        """
        Получает данные для теста.

        Args:
            test_name: Имя теста
            default: Значение по умолчанию

        Returns:
            Сохраненные данные или значение по умолчанию
        """
        return self.data.get(test_name, default)

    def set_test_data(self, test_name: str, data: Any) -> None:
        """
        Сохраняет данные для теста.

        Args:
            test_name: Имя теста
            data: Данные для сохранения
        """
        self.data[test_name] = data
        self.save_data()

    def generate_unique_user(self, prefix: str = "user") -> Dict[str, str]:
        """
        Генерирует уникальные данные пользователя.

        Args:
            prefix: Префикс для имени пользователя

        Returns:
            dict: Данные пользователя
        """
        timestamp = str(int(time.time()))

        user_data = {
            "first_name": f"{prefix.capitalize()}",
            "last_name": f"Test{timestamp[-4:]}",
            "username": f"{prefix}_{timestamp}",
            "email": f"{prefix}_{timestamp}@example.com",
            "phone": DataGenerator.random_phone(),
            "address": DataGenerator.random_address()["full"],
        }

        # Сохраняем для возможного повторного использования
        self.set_test_data(f"generated_user_{timestamp}", user_data)

        return user_data


# Экземпляры утилит для использования в тестах
data_generator = DataGenerator()
file_manager = FileManager()
validation_helper = ValidationHelper()
wait_helper = WaitHelper()
test_data_manager = TestDataManager()
