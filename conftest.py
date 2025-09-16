# conftest.py
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext
from datetime import datetime
from data import URLs
from locators.elements.dynamic_locators import DynamicPropertiesLocators
from pages.elements import (
    LinksPage,
    BrokenLinksPage,
    UploadDownloadPage,
    DynamicPropertiesPage,
)

from pages.widgets import (
    SliderPage,
    ProgressBarPage,
    AccordionPage,
    AutoCompletePage,
    DatePickerPage,
    TabsPage,
    ToolTipsPage,
    SelectMenuPage,
    MenuPage,
)
from locators.widgets import (
    ProgressBarLocators,
    ToolTipsLocators,
    TabsLocators,
    DatePickerLocators,
    AutoCompleteLocators,
)


# --- Список доменов для блокировки внешних и рекламных запросов ---
blocked_domains = [
    "doubleclick.net",
    "googlesyndication.com",
    "pagead2.googlesyndication.com",
    "adservice.google.com",
    "google-analytics.com",
    "analytics.google.com",
    "googletagmanager.com",
    "www.googletagmanager.com",
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
    "serving.stat-rock.com",
    "stat-rock.com",
    "ad.plus",
    "g.doubleclick.net",
    "googletagservices.com",
]


def block_external(route):
    """Блокирует загрузку внешних и ненужных ресурсов."""
    url = route.request.url.lower()
    resource_type = route.request.resource_type
    # Блокируем шрифты и изображения
    if resource_type in {"font", "image"}:
        route.abort()
        return
    # Блокируем известные рекламные/аналитические домены
    if any(domain in url for domain in blocked_domains):
        route.abort()
        return
    route.continue_()


def no_pic_block_external(route):
    url = route.request.url.lower()
    resource_type = route.request.resource_type
    # Блокируем шрифты и изображения
    if resource_type in {"font"}:
        route.abort()
        return
    # Блокируем известные рекламные/аналитические домены
    if any(domain in url for domain in blocked_domains):
        route.abort()
        return
    route.continue_()


@pytest.fixture(scope="session")
def browser() -> Browser:
    """Запускает браузер Chromium на всю сессию тестов."""
    pw = sync_playwright().start()
    browser = pw.chromium.launch(
        headless=False,  # Установите True для CI
        ignore_default_args=["--disable-extensions"],  # Помогает с CSP
    )
    yield browser
    browser.close()
    pw.stop()


@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    """Создаёт новый контекст браузера для каждого теста с отключёнными внешними ресурсами."""
    context = browser.new_context(
        ignore_https_errors=True,  # Игнорировать ошибки сертификатов
        bypass_csp=True,  # Обход политики безопасности контента
        viewport={"width": 1920, "height": 1080},  # Фиксированное разрешение
    )
    context.route("**/*", block_external)
    yield context
    context.close()


def create_page_with_wait(
    page,
    url: str,
    wait_selectors: list,
    stabilize_timeout: int = 1000,
    expected_status: int = 200,
):
    """
    Переходит по url с проверкой кода ответа и ожиданием появления указанных селекторов.
    Повторяет попытку до 3 раз при неудаче.
    """
    for attempt in range(3):
        try:
            print(f"Попытка {attempt + 1} перехода на {url}")

            response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
            status = response.status if response else None
            print(f"HTTP статус: {status}")

            if status != expected_status:
                raise Exception(
                    f"Неверный HTTP статус: {status}, ожидается {expected_status}"
                )

            break
        except Exception as e:
            print(f"Попытка {attempt + 1} не удалась: {e}")
            if attempt == 2:
                raise
            page.wait_for_timeout(2000)

    for selector, state, timeout in wait_selectors:
        try:
            print(
                f"Ожидание селектора '{selector}' в состоянии '{state}', таймаут {timeout}мс"
            )
            page.wait_for_selector(selector, state=state, timeout=timeout)
        except Exception as e:
            print(f"Не дождался селектора '{selector}': {e}")
    if stabilize_timeout > 0:
        print(f"Стабилизация: пауза {stabilize_timeout} мс")
        page.wait_for_timeout(stabilize_timeout)


# --- Фикстуры для страниц с более длительным scope, для повторного использования контекстов ---
@pytest.fixture(scope="module")
def progress_page(browser):
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

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


@pytest.fixture(scope="module")
def slider_page(browser):
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    wait_selectors = [
        (".range-slider", "visible", 10000),
        ("#sliderValue", "visible", 10000),
    ]
    create_page_with_wait(page, URLs.SLIDER_URL, wait_selectors, stabilize_timeout=2000)
    slider_page = SliderPage(page)

    yield slider_page

    page.close()
    context.close()


@pytest.fixture(scope="module")
def accordion_page(browser):
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    wait_selectors = [("div.accordion", "visible", 10000)]
    create_page_with_wait(
        page, URLs.ACCORDION_URL, wait_selectors, stabilize_timeout=1000
    )
    accordion_page = AccordionPage(page)

    yield accordion_page

    page.close()
    context.close()


@pytest.fixture(scope="module")
def autocomplete_page(browser):
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    wait_selectors = [(AutoCompleteLocators.SINGLE_COLOR_INPUT, "visible", 10000)]
    create_page_with_wait(
        page, URLs.AUTO_COMPLETE_URL, wait_selectors, stabilize_timeout=1000
    )
    autocomplete_page = AutoCompletePage(page)

    yield autocomplete_page

    page.close()
    context.close()


@pytest.fixture(scope="module")
def datepicker_page(browser):
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    wait_selectors = [(DatePickerLocators.DATE_INPUT, "visible", 10000)]
    create_page_with_wait(
        page, URLs.DATE_PICKER_URL, wait_selectors, stabilize_timeout=2000
    )
    datepicker_page = DatePickerPage(page)

    yield datepicker_page

    page.close()
    context.close()


@pytest.fixture(scope="module")
def tabs_page(browser):
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    wait_selectors = [(TabsLocators.TAB_WHAT, "visible", 10000)]
    create_page_with_wait(page, URLs.TABS_URL, wait_selectors, stabilize_timeout=2000)
    tabs_page = TabsPage(page)

    yield tabs_page

    page.close()
    context.close()


@pytest.fixture(scope="module")
def tooltips_page(browser):
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    wait_selectors = [(ToolTipsLocators.HOVER_BUTTON, "visible", 10000)]
    create_page_with_wait(
        page, URLs.TOOL_TIPS_URL, wait_selectors, stabilize_timeout=3000
    )
    tooltips_page = ToolTipsPage(page)

    yield tooltips_page

    page.close()
    context.close()


@pytest.fixture(scope="module")
def menu_page(browser):
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    wait_selectors = [("#app", "visible", 3000)]

    for attempt in range(3):
        try:
            now = datetime.now().strftime("%H:%M:%S")
            print(
                f"[MenuPage Fixture] Попытка {attempt + 1} перехода на {URLs.MENU_URL} в {now}"
            )
            page.goto(URLs.MENU_URL, wait_until="load", timeout=5000)
            break
        except Exception as e:
            print(f"[MenuPage Fixture] Попытка {attempt + 1} не удалась: {e}")
            if attempt == 2:
                raise
            page.wait_for_timeout(1000)

    for selector, state, timeout in wait_selectors:
        try:
            now = datetime.now().strftime("%H:%M:%S")
            print(f"[MenuPage Fixture] Ожидание селектора '{selector}' в {now}")
            page.wait_for_selector(selector, state=state, timeout=timeout)
        except Exception as e:
            print(f"[MenuPage Fixture] Не дождался селектора '{selector}': {e}")
            raise

    page.wait_for_timeout(3000)
    menu_page = MenuPage(page)

    yield menu_page

    page.close()
    context.close()


# --- Настройка профилей тестов ---
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


@pytest.fixture(scope="session")
def select_menu_page(browser):
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    create_page_with_wait(
        page,
        URLs.SELECT_MENU_URL,
        wait_selectors=[
            ("#app", "visible", 10000),
            ("select, .css-yk16ysz-control", "visible", 10000),
        ],
        stabilize_timeout=2000,
    )

    select_menu_page = SelectMenuPage(page)
    yield select_menu_page

    page.close()
    context.close()


@pytest.fixture(scope="session")
def links_page(browser):
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    create_page_with_wait(
        page,
        URLs.LINKS_PAGE,
        wait_selectors=[
            ("#app", "visible", 10000),
            ("select, .css-yk16ysz-control", "visible", 10000),
        ],
        stabilize_timeout=2000,
    )

    links_page = LinksPage(page)
    yield links_page

    page.close()
    context.close()


@pytest.fixture(scope="session")
def broken_links_page(browser):
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", no_pic_block_external)
    page = context.new_page()

    create_page_with_wait(
        page,
        URLs.BROKEN_LINKS,
        wait_selectors=[
            ("#app", "visible", 10000),
            ("select, .css-yk16ysz-control", "visible", 10000),
        ],
        stabilize_timeout=2000,
    )

    broken_links_page = BrokenLinksPage(page)
    yield broken_links_page
    page.close()
    context.close()


@pytest.fixture(scope="session")
def upload_download_page(browser):
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    create_page_with_wait(
        page,
        URLs.DOWNLOAD,
        wait_selectors=[
            ("#app", "visible", 10000),
            ("select, .css-yk16ysz-control", "visible", 10000),
        ],
        stabilize_timeout=2000,
    )

    upload_download_page = UploadDownloadPage(page)
    yield upload_download_page
    page.close()
    context.close()


@pytest.fixture(scope="session")
def dynamic_properties_page(browser):

    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    page = context.new_page()

    create_page_with_wait(
        page,
        URLs.DYNAMIC,
        wait_selectors=[
            ("#app", "visible", 10000),
            ("select, .css-yk16ysz-control", "visible", 10000),
        ],
        stabilize_timeout=2000,
    )

    dynamic_properties_page = DynamicPropertiesPage(page)
    yield dynamic_properties_page
    page.close()
    context.close()
