# DemoQA_Playwright


## КОМАНДЫ ДЛЯ ЗАПУСКА И ГЕНЕРАЦИИ ОТЧЕТОВ

### Установка зависимостей

 Через uv
```bash
uv add --dev pytest allure-pytest pytest-dependency
```

 Или через pip
```bash
pip install pytest allure-pytest pytest-dependency
```

### Запуск тестов
```bash
# Все тесты с Allure
pytest --alluredir=allure-results

# Только smoke тесты
pytest -m smoke --alluredir=allure-results

# Конкретная категория
pytest -m elements --alluredir=allure-results

# С детальным выводом
pytest -v -s --alluredir=allure-results

# Параллельный запуск (если установлен pytest-xdist)
pytest -n auto --alluredir=allure-results
```

### Генерация отчетов Allure
```bash
# Интерактивный отчет
allure serve allure-results

# Статический HTML отчет
allure generate allure-results -o allure-report --clean

# Открыть готовый отчет
allure open allure-report
```


Автоматизированные тесты созданные с использованием pytest и playwright

Реализованы проверки:

Раздел Elements
   1. Заполнение формы регистрации (https://demoqa.com/text-box)
   2. Чек бокс дерево каталога (https://demoqa.com/checkbox)
   3. Радиокнопки на странице (https://demoqa.com/radio-button)
   4. Таблица данных на странице (https://demoqa.com/webtables) 
   5. Кнопки на странице (https://demoqa.com/buttons)
   6. Ссылки на странице (https://demoqa.com/links)
   7. Ссылки на странице (https://demoqa.com/broken)
   8. Страница загрузки файлов (https://demoqa.com/upload-download)
   9. Страница эффектов (https://demoqa.com/dynamic-properties)

Раздел Alerts:
   1. Новые окна (https://demoqa.com/browser-windows)
   2. Алерты (https://demoqa.com/alerts)
   3. Фреймы (https://demoqa.com/frames)
   4. Вложенные фреймы (https://demoqa.com/nestedframes)
   5. Модальные окна (https://demoqa.com/modal-dialogs)

Раздел Forms:
   1. Заполнение формы регистрации (https://demoqa.com/automation-practice-form)  

Раздел Widgets:
   1. Прогресс бар на странице (https://demoqa.com/progress-bar)
   2. Слайдер на странице (https://demoqa.com/slider)
   3. Текстовый аккордеон на странице (https://demoqa.com/accordian)
   4. Поля ввода с автозаполнением на странице (https://demoqa.com/auto-complete)
   5. Календарь на странице (https://demoqa.com/date-picker)
   6. Вкладки на странице (https://demoqa.com/tabs)
   7. Всплывающие подсказки на странице (https://demoqa.com/tool-tips)
   8. Меню на странице (http://demoqa.com/menu)
   9. Dropdown меню на странице (https://demoqa.com/select-menu)

Раздел Interactions:
   1. Сортируемые списки (https://demoqa.com/sortable)
   2. Выбираемые списки (https://demoqa.com/selectable)
   3. Изменяемые элементы (https://demoqa.com/resizable)
   4. Перемещаемые элементы (https://demoqa.com/droppable)
   5. Перемещаемые элементы 2 (https://demoqa.com/dragabble)

Раздел Book Store Application:
   1. Страница авторизации (https://demoqa.com/login)
   2. Страница магазина (https://demoqa.com/books)
   3. Страница профиля (https://demoqa.com/profile)
 
