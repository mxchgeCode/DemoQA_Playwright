class LoginLocators:
    USERNAME_INPUT = "#userName"
    PASSWORD_INPUT = "#password"


    ERROR_MESSAGE = "#name"  # ошибка при неуспешном входе

    FORGOT_PASSWORD_LINK = "text=Forgot Password"



    NEW_USER_BUTTON = "#newUser"
    PAGE_HEADER = "h1.text-center"
    REGISTER_BUTTON = "#register"

    # Поля регистрации
    FIRST_NAME = "#firstname"
    LAST_NAME = "#lastname"
    USER_NAME_REG = "#userName"
    PASSWORD_REG = "#password"

    # Предупреждения (класс is-invalid на input)
    FIRST_NAME_INPUT = "#firstname.is-invalid"
    LAST_NAME_INPUT = "#lastname.is-invalid"
    USER_NAME_INPUT_REG = "#userName.is-invalid"
    PASSWORD_INPUT_REG = "#password.is-invalid"

    # Сообщение ошибки пароля
    PASSWORD_ERROR = "#password ~ .invalid-feedback"

    # Сообщение капчи
    CAPTCHA_ERROR = "#name"

    CAPTCHA_CHECKBOX = ".recaptcha-checkbox-border"
    BACK_TO_LOGIN_BUTTON = "#gotologin"

    # Логин форма
    USER_NAME_LOGIN = "#userName"
    PASSWORD_LOGIN = "#password"
    LOGIN_BUTTON = "#login"
    USER_DISPLAY = "#userName-value"  # отображается после успешного входа
