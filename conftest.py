# conftest.py
import pytest
from playwright.sync_api import sync_playwright

# --- Блокировка ресурсов ---
blocked_domains = [
    "doubleclick.net",
    "googlesyndication.com",
    "pagead2.googlesyndication.com",  # Добавлено из HAR
    "adservice.google.com",
    "google-analytics.com",
    "analytics.google.com",
    "googletagmanager.com",
    "www.googletagmanager.com",  # Добавлено из HAR
    "connect.facebook.net",
    "facebook.com",
    "twitter.com",
    "taboola.com",
    "outbrain.com",
    "adnxs.com",
    "c.amazon-adsystem.com",
    "scorecardresearch.com",
    "hotjar.com",
    "mouseflow.com",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "cdn.jsdelivr.net",
    "cdnjs.cloudflare.com",
    "unpkg.com",
    "serving.stat-rock.com",  # Добавлено из HAR
    "stat-rock.com",  # Добавлено из HAR
    "ad.plus",  # Добавлено из HAR
    "g.doubleclick.net",  # Добавлено из HAR
    "googletagservices.com",  # Добавлено из HAR
]


def block_external(route):
    """Блокирует внешние и ненужные ресурсы."""
    url = route.request.url.lower()  # Приводим к нижнему регистру для сравнения
    resource_type = route.request.resource_type
    # Блокируем шрифты и изображения для ускорения
    if resource_type in ["font", "image"]:
        route.abort()
        return
    # Блокируем запросы к известным рекламным/аналитическим доменам
    if any(domain in url for domain in blocked_domains):
        route.abort()
        return
    # Разрешаем всё остальное
    route.continue_()


# --- Фикстуры Playwright ---
@pytest.fixture(scope="session")  # Браузер на всю сессию
def browser():
    """Запускает браузер на всю сессию тестов."""
    pw = None
    browser = None
    try:
        pw = sync_playwright().start()
        # Запуск браузера с игнорированием HTTPS ошибок для тестовой среды
        browser = pw.chromium.launch(
            headless=False,  # Установи True для CI/headless режима
            ignore_default_args=["--disable-extensions"],  # Иногда помогает с CSP
        )
        yield browser
    finally:
        if browser and browser.is_connected():
            browser.close()
        if pw:
            try:
                pw.stop()
            except:
                pass


@pytest.fixture(scope="function")  # Новый контекст для каждой функции/теста
def context(browser):
    """Создает новый контекст браузера для каждого теста."""
    # Создаем контекст с полезными настройками
    context = browser.new_context(
        ignore_https_errors=True,  # Игнорировать ошибки SSL/HTTPS
        bypass_csp=True,  # Обход CSP (Content Security Policy)
        viewport={"width": 1920, "height": 1080},  # Фиксированное разрешение
    )
    # Применяем блокировку ко всем запросам в этом контексте
    context.route("**/*", block_external)
    yield context
    # Закрываем контекст после теста
    context.close()


@pytest.fixture(scope="function")  # Новая страница для каждого теста
def page(context):
    """Создает новую страницу в контексте для каждого теста."""
    page = context.new_page()
    yield page
    # Страница автоматически закрывается при закрытии контекста


# --- Вспомогательная функция для создания страниц с ожиданиями ---
def create_page_with_wait(page, url, wait_selectors, stabilize_timeout=1000):
    """Переходит на URL и ждет указанные селекторы.
    Args:
        page: Экземпляр страницы Playwright.
        url: URL для перехода.
        wait_selectors: Список кортежей (селектор, состояние, таймаут в мс).
        stabilize_timeout: Дополнительная пауза для стабилизации в мс.
    """
    # Переход с повторными попытками
    for attempt in range(3):
        try:
            print(f"Попытка {attempt + 1} перехода на {url}")
            # Используем domcontentloaded для скорости, networkidle может ждать заблокированные ресурсы
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            break
        except Exception as e:
            print(f"Попытка {attempt + 1} перехода не удалась: {e}")
            if attempt == 2:  # Последняя попытка
                raise e
            page.wait_for_timeout(2000)  # Пауза перед повторной попыткой

    # Ожидание ключевых селекторов
    for selector, state, timeout in wait_selectors:
        try:
            print(
                f"Ожидание селектора '{selector}' со статусом '{state}' (таймаут {timeout}мс)"
            )
            page.wait_for_selector(selector, state=state, timeout=timeout)
        except Exception as e:
            print(f"Не удалось дождаться селектора '{selector}': {e}")
            # Не прерываем выполнение, если селектор не критичен

    # Дополнительная стабилизация
    if stabilize_timeout > 0:
        print(f"Стабилизация: ожидание {stabilize_timeout}мс")
        page.wait_for_timeout(stabilize_timeout)

    # Попытка дождаться networkidle, но с меньшим таймаутом, чтобы не блокировать
    try:
        print("Ожидание networkidle (макс. 5 секунд)...")
        page.wait_for_load_state("networkidle", timeout=5000)
    except Exception as e:
        print(f"Не удалось дождаться networkidle: {e}. Продолжаем.")


# --- Фикстуры для конкретных страниц с измененным scope ---
# Изменяем scope на "module" для страниц, где элементы не влияют друг на друга

@pytest.fixture(scope="module")  # Изменено с "function"
def progress_page(browser):  # Зависимость от browser, а не от context/page
    """Фикстура для страницы Progress Bar."""
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    from pages.progress_bar_page import ProgressBarPage
    from data import URLs
    from locators.progress_bar_locators import ProgressBarLocators

    wait_selectors = [
        ("#app", "visible", 10000),
        (ProgressBarLocators.START_STOP_BUTTON, "visible", 10000),
        (ProgressBarLocators.PROGRESS_BAR, "visible", 10000),
    ]
    create_page_with_wait(
        page, URLs.PROGRESS_BAR, wait_selectors, stabilize_timeout=2000
    )
    progress_page = ProgressBarPage(page)
    yield progress_page

    page.close()
    context.close()


@pytest.fixture(scope="module")  # Изменено с "function"
def slider_page(browser):  # Зависимость от browser
    """Фикстура для страницы Slider."""
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    from pages.slider_page import SliderPage
    from data import URLs

    wait_selectors = [
        (".range-slider", "visible", 10000),
        ("#sliderValue", "visible", 10000),
    ]
    create_page_with_wait(page, URLs.SLIDER_URL, wait_selectors, stabilize_timeout=2000)
    slider_page = SliderPage(page)
    yield slider_page

    page.close()
    context.close()


@pytest.fixture(scope="module")  # Изменено с "function"
def accordion_page(browser):  # Зависимость от browser
    """Фикстура для страницы Accordion."""
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    from pages.accordion_page import AccordionPage
    from data import URLs

    wait_selectors = [
        ("div.accordion", "visible", 10000),
    ]
    create_page_with_wait(
        page, URLs.ACCORDION_URL, wait_selectors, stabilize_timeout=1000
    )
    accordion_page = AccordionPage(page)
    yield accordion_page

    page.close()
    context.close()


@pytest.fixture(scope="module")  # Изменено с "function"
def autocomplete_page(browser):  # Зависимость от browser
    """Фикстура для страницы Auto Complete."""
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    from pages.auto_complete_page import AutoCompletePage
    from data import URLs
    from locators.auto_complete_locators import AutoCompleteLocators

    wait_selectors = [
        (AutoCompleteLocators.SINGLE_COLOR_INPUT, "visible", 10000),
    ]
    create_page_with_wait(
        page, URLs.AUTO_COMPLETE_URL, wait_selectors, stabilize_timeout=1000
    )
    autocomplete_page = AutoCompletePage(page)
    yield autocomplete_page

    page.close()
    context.close()


@pytest.fixture(scope="module")  # Изменено с "function"
def datepicker_page(browser):  # Зависимость от browser
    """Фикстура для страницы Date Picker."""
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    from pages.date_picker_page import DatePickerPage
    from data import URLs
    from locators.date_picker_locators import DatePickerLocators

    wait_selectors = [
        (DatePickerLocators.DATE_INPUT, "visible", 10000),
    ]
    create_page_with_wait(
        page, URLs.DATE_PICKER_URL, wait_selectors, stabilize_timeout=2000
    )
    datepicker_page = DatePickerPage(page)
    yield datepicker_page

    page.close()
    context.close()


@pytest.fixture(scope="module")  # Изменено с "function"
def tabs_page(browser):  # Зависимость от browser
    """Фикстура для страницы Tabs."""
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    from pages.tabs_page import TabsPage
    from data import URLs
    from locators.tabs_locators import TabsLocators

    wait_selectors = [
        (TabsLocators.TAB_WHAT, "visible", 10000),
    ]
    create_page_with_wait(page, URLs.TABS_URL, wait_selectors, stabilize_timeout=2000)
    tabs_page = TabsPage(page)
    yield tabs_page

    page.close()
    context.close()


@pytest.fixture(scope="module")  # Изменено с "function"
def tooltips_page(browser):  # Зависимость от browser
    """Фикстура для страницы Tool Tips."""
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    from pages.tool_tips_page import ToolTipsPage
    from data import URLs
    from locators.tool_tips_locators import ToolTipsLocators

    wait_selectors = [
        (ToolTipsLocators.HOVER_BUTTON, "visible", 10000),
    ]
    create_page_with_wait(
        page, URLs.TOOL_TIPS_URL, wait_selectors, stabilize_timeout=3000
    )
    tooltips_page = ToolTipsPage(page)
    yield tooltips_page

    page.close()
    context.close()


# --- Изменено: scope="module" для Menu ---
@pytest.fixture(scope="module")  # Изменено с "function"
def menu_page(browser):  # Зависимость от browser
    """Фикстура для страницы Menu."""
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    from pages.menu_page import MenuPage
    from data import URLs

    # Для Menu увеличиваем таймауты из-за его специфики
    wait_selectors = [
        ("#app", "visible", 15000),  # Увеличенный таймаут
        # Добавь селекторы для конкретных элементов меню, если они стабильны
    ]

    # Используем 'load' вместо 'domcontentloaded' для Menu, если это помогает
    for attempt in range(3):
        try:
            print(f"[MenuPage Fixture] Попытка {attempt + 1} перехода на {URLs.MENU_URL}")
            page.goto(URLs.MENU_URL, wait_until="load", timeout=40000)
            break
        except Exception as e:
            print(f"[MenuPage Fixture] Попытка {attempt + 1} перехода не удалась: {e}")
            if attempt == 2:
                # Если все попытки неудачны, пробуем domcontentloaded
                try:
                    page.goto(
                        URLs.MENU_URL, wait_until="domcontentloaded", timeout=30000
                    )
                    break
                except Exception as e2:
                    print(f"[MenuPage Fixture] Все попытки перехода неудачны: {e2}")
                    page.close()
                    context.close()
                    raise e2  # Выбрасываем последнюю ошибку
            page.wait_for_timeout(3000)

    # Ожидание ключевых селекторов
    for selector, state, timeout in wait_selectors:
        try:
            print(f"[MenuPage Fixture] Ожидание селектора '{selector}'")
            page.wait_for_selector(selector, state=state, timeout=timeout)
        except Exception as e:
            print(f"[MenuPage Fixture] Не удалось дождаться селектора '{selector}': {e}")
            page.close()
            context.close()
            raise e

    # Увеличенная стабилизация для Menu
    print("[MenuPage Fixture] Стабилизация Menu: ожидание 5000мс")
    page.wait_for_timeout(5000)

    menu_page = MenuPage(page)
    yield menu_page

    print("[MenuPage Fixture] Закрытие страницы и контекста Menu...")
    page.close()
    context.close()
    print("[MenuPage Fixture] Страница и контекст Menu закрыты.")


# --- Изменено: scope="module" для Select Menu ---
@pytest.fixture(scope="module")  # Изменено с "function"
def select_menu_page(browser):  # Зависимость от browser
    """Фикстура для страницы Select Menu."""
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    from pages.select_menu_page import SelectMenuPage
    from data import URLs

    wait_selectors = [
        ("#app", "visible", 10000),
        ("select, .css-yk16ysz-control", "visible", 10000),  # Ждем любые select элементы
    ]
    create_page_with_wait(
        page, URLs.SELECT_MENU_URL, wait_selectors, stabilize_timeout=2000
    )
    select_menu_page = SelectMenuPage(page)
    yield select_menu_page

    page.close()
    context.close()


# --- Настройка профилей ---
def pytest_addoption(parser):
    parser.addoption(
        "--profile",
        action="store",
        default="default",
        help="Test profile: smoke, full, demo",
    )


def pytest_configure(config):
    profile = config.getoption("--profile")
    if profile == "smoke":
        config.option.browser = ["chromium"]
    elif profile == "full":
        config.option.browser = ["chromium", "firefox"]
        config.option.headed = True
    elif profile == "demo":
        config.option.browser = ["chromium"]
        config.option.headed = True
