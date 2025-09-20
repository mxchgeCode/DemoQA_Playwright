"""
Локаторы для страницы авторизации BookStore.
Содержит селекторы для форм входа, регистрации и элементов управления аккаунтом.
"""


class LoginLocators:
    """CSS селекторы для элементов страницы авторизации BookStore."""

    # === ФОРМА ВХОДА В СИСТЕМУ ===
    USERNAME_INPUT = "#userName"  # Поле ввода имени пользователя
    PASSWORD_INPUT = "#password"  # Поле ввода пароля
    LOGIN_BUTTON = "#login"  # Кнопка входа в систему

    # Навигационные элементы
    NEW_USER_BUTTON = "#newUser"  # Переход к регистрации
    FORGOT_PASSWORD_LINK = "text=Forgot Password"  # Ссылка восстановления пароля

    # === ФОРМА РЕГИСТРАЦИИ ===
    # Поля регистрации нового пользователя
    FIRST_NAME = "#firstname"  # Имя
    LAST_NAME = "#lastname"  # Фамилия
    USER_NAME_REG = "#userName"  # Имя пользователя (регистрация)
    PASSWORD_REG = "#password"  # Пароль (регистрация)
    REGISTER_BUTTON = "#register"  # Кнопка регистрации

    # Навигация в регистрации
    BACK_TO_LOGIN_BUTTON = "#gotologin"  # Возврат к форме входа

    # === ВАЛИДАЦИЯ И ОШИБКИ ===
    # Поля с ошибками валидации (класс is-invalid)
    FIRST_NAME_INPUT = "#firstname.is-invalid"  # Невалидное имя
    LAST_NAME_INPUT = "#lastname.is-invalid"  # Невалидная фамилия
    USER_NAME_INPUT_REG = "#userName.is-invalid"  # Невалидное имя пользователя
    PASSWORD_INPUT_REG = "#password.is-invalid"  # Невалидный пароль

    # Сообщения об ошибках
    ERROR_MESSAGE = "#name"  # Общее сообщение об ошибке
    PASSWORD_ERROR = "#password ~ .invalid-feedback"  # Ошибка требований к паролю
    CAPTCHA_ERROR = "#name"  # Ошибка проверки reCAPTCHA

    # === ЭЛЕМЕНТЫ ИНТЕРФЕЙСА ===
    PAGE_HEADER = "h1.text-center"  # Заголовок страницы
    CAPTCHA_CHECKBOX = ".recaptcha-checkbox-border"  # Чекбокс reCAPTCHA

    # === СОСТОЯНИЕ ПОСЛЕ АВТОРИЗАЦИИ ===
    USER_DISPLAY = "#userName-value"  # Отображение имени авторизованного пользователя
    LOGOUT_BUTTON = "#logout"  # Кнопка выхода из системы (если есть)

    # === ДУБЛИРУЮЩИЕ СЕЛЕКТОРЫ ДЛЯ ЯСНОСТИ ===
    # Форма входа (явное указание контекста)
    USER_NAME_LOGIN = "#userName"  # Имя пользователя для входа
    PASSWORD_LOGIN = "#password"  # Пароль для входа
