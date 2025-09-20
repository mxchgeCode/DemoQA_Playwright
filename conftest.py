"""
Основной конфигурационный файл pytest с фикстурами для всех страниц проекта.
Содержит браузерные контексты, фикстуры страниц и интеграцию с Allure.
"""

import os
import shutil
import subprocess
import time
import logging
from typing import List, Tuple

import allure
import pytest
from playwright.sync_api import Browser, Page, BrowserContext
from data import URLs

# Импорты всех страниц
from pages.base_page import BasePage
from pages.alerts.alerts_page import AlertsPage
from pages.alerts.browser_windows_page import BrowserWindowsPage
from pages.alerts.frames_page import FramesPage
from pages.alerts.modal_page import ModalPage
from pages.alerts.nested_frames_page import NestedFramesPage
from pages.bookstore.login_page import LoginPage
from pages.elements.broken_links_page import BrokenLinksPage
from pages.elements.buttons_page import ButtonsPage
from pages.elements.check_box_page import CheckBoxPage
from pages.elements.dynamic_properties_page import DynamicPropertiesPage
from pages.elements.links_page import LinksPage
from pages.elements.radio_button_page import RadioButtonPage
from pages.elements.text_box_page import TextBoxPage
from pages.elements.upload_download_page import UploadDownloadPage
from pages.elements.web_tables_page import WebTablesPage
from pages.forms.practice_form_page import AutomationPracticeFormPage
from pages.interactions.dragabble_page import DragabblePage
from pages.interactions.droppable_page import DroppablePage
from pages.interactions.resizable_page import ResizablePage
from pages.interactions.selectable_page import SelectablePage
from pages.interactions.sortable_page import SortablePage
from pages.widgets.accordion_page import AccordionPage
from pages.widgets.auto_complete_page import AutoCompletePage
from pages.widgets.date_picker_page import DatePickerPage
from pages.widgets.menu_page import MenuPage
from pages.widgets.progress_bar_page import ProgressBarPage
from pages.widgets.select_menu_page import SelectMenuPage
from pages.widgets.slider_page import SliderPage
from pages.widgets.tabs_page import TabsPage
from pages.widgets.tool_tips_page import ToolTipsPage

logger = logging.getLogger(__name__)

# Домены для блокировки внешних ресурсов
BLOCKED_DOMAINS = [
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
]


def block_external_resources(route):
    """
    Блокирует внешние ресурсы (шрифты, изображения, рекламу) для ускорения тестов.

    Args:
        route: Playwright route объект для перехвата запросов
    """
    url = route.request.url.lower()
    resource_type = route.request.resource_type

    # Блокируем шрифты и изображения
    if resource_type in {"font", "image"}:
        route.abort()
        return

    # Блокируем домены из черного списка
    if any(domain in url for domain in BLOCKED_DOMAINS):
        route.abort()
        return

    route.continue_()


@pytest.fixture(scope="session")
def auth_storage(tmp_path_factory, browser):
    """
    Создает storage_state.json для авторизованного пользователя один раз за сессию.
    Используется для тестов, требующих аутентификации.

    Returns:
        str: Путь к файлу с сохраненным состоянием авторизации
    """
    storage = tmp_path_factory.mktemp("auth") / "state.json"
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    page = context.new_page()

    try:
        page.goto(URLs.LOGIN_PAGE)
        page.fill("#userName", "asd")
        page.fill("#password", "Password123###")
        page.click("#login")
        page.wait_for_selector("#userName-value", timeout=10000)
        context.storage_state(path=str(storage))
    except Exception as e:
        logger.warning(f"Не удалось создать авторизованное состояние: {e}")
    finally:
        context.close()

    return str(storage)


@pytest.fixture(scope="module")
def browser_context(playwright, browser_name, browser_context_args):
    """
    Создает основной браузерный контекст с блокировкой внешних запросов.

    Args:
        playwright: Playwright instance
        browser_name: Имя браузера (chromium, firefox, webkit)
        browser_context_args: Дополнительные аргументы контекста

    Yields:
        BrowserContext: Настроенный контекст браузера
    """
    browser = getattr(playwright, browser_name).launch(headless=False, slow_mo=100)
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
        **browser_context_args,
    )
    context.route("**/*", block_external_resources)
    yield context
    context.close()
    browser.close()


@pytest.fixture(scope="module")
def page(browser_context) -> Page:
    """
    Создает страницу в основном браузерном контексте.

    Args:
        browser_context: Браузерный контекст

    Yields:
        Page: Страница браузера
    """
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="module")
def auth_context(browser, auth_storage):
    """
    Создает контекст браузера с предварительной авторизацией.

    Args:
        browser: Browser instance
        auth_storage: Путь к файлу с сохраненным состоянием авторизации

    Yields:
        BrowserContext: Авторизованный контекст браузера
    """
    context = browser.new_context(
        storage_state=auth_storage if os.path.exists(auth_storage) else None,
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    yield context
    context.close()


def create_page_with_wait(
    page: Page,
    url: str,
    wait_selectors: List[Tuple[str, str, int]],
    stabilize_timeout: int = 1000,
    expected_status: int = 200,
):
    """
    Универсальная функция для создания страницы с ожиданием загрузки элементов.

    Args:
        page: Страница браузера
        url: URL для перехода
        wait_selectors: Список селекторов для ожидания [(selector, state, timeout)]
        stabilize_timeout: Время стабилизации после загрузки
        expected_status: Ожидаемый HTTP статус ответа

    Raises:
        Exception: При неудачной загрузке после 3 попыток
    """
    for attempt in range(3):
        try:
            # Добавляем cache-buster для обхода кеша
            url_with_cache_bypass = f"{url}?_={int(time.time())}"
            response = page.goto(
                url_with_cache_bypass, wait_until="domcontentloaded", timeout=30000
            )

            status = response.status if response else None
            if status not in (expected_status, 304):
                raise Exception(
                    f"HTTP статус {status}, ожидался {expected_status} или 304"
                )

            # Ожидание всех указанных селекторов
            for selector, state, timeout in wait_selectors:
                page.locator(selector).wait_for(state=state, timeout=timeout)

            # Дополнительная пауза для стабилизации
            page.wait_for_timeout(stabilize_timeout)
            return

        except Exception as e:
            if attempt == 2:
                raise Exception(f"Не удалось загрузить страницу {url}: {e}")
            logger.warning(f"Попытка {attempt + 1} загрузки {url} неудачна: {e}")
            page.reload()


# ======================== ФИКСТУРЫ СТРАНИЦ ========================


@pytest.fixture(scope="module")
def make_page():
    """
    Фабрика для создания экземпляров страниц с универсальной инициализацией.

    Returns:
        callable: Функция для создания страниц
    """

    def _make_page(page: Page, url: str, page_class, wait_selectors=None):
        if wait_selectors is None:
            wait_selectors = [("#app", "visible", 10000)]
        create_page_with_wait(page, url, wait_selectors)
        return page_class(page)

    return _make_page


# Elements fixtures
@pytest.fixture(scope="module")
def text_box_page(page: Page):
    """Фикстура для страницы Text Box."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.TEXT_BOX, selectors)
    yield TextBoxPage(page)


@pytest.fixture(scope="module")
def check_box_page(page: Page):
    """Фикстура для страницы Check Box."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.CHECK_BOX, selectors)
    yield CheckBoxPage(page)


@pytest.fixture(scope="module")
def radio_button_page(page: Page):
    """Фикстура для страницы Radio Button."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.RADIO_BUTTON, selectors)
    yield RadioButtonPage(page)


@pytest.fixture(scope="module")
def web_tables_page(page: Page):
    """Фикстура для страницы Web Tables."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.WEB_TABLES, selectors)
    yield WebTablesPage(page)


@pytest.fixture(scope="module")
def buttons_page(page: Page):
    """Фикстура для страницы Buttons."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.BUTTONS, selectors)
    yield ButtonsPage(page)


@pytest.fixture(scope="module")
def links_page(page: Page):
    """Фикстура для страницы Links."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.LINKS_PAGE, selectors)
    yield LinksPage(page)


@pytest.fixture(scope="module")
def broken_links_page(browser: Browser):
    """Фикстура для страницы Broken Links без блокировки запросов."""
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    page = context.new_page()

    wait_selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.BROKEN_LINKS, wait_selectors)

    yield BrokenLinksPage(page)
    page.close()
    context.close()


@pytest.fixture(scope="module")
def upload_download_page(page: Page):
    """Фикстура для страницы Upload/Download."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.DOWNLOAD, selectors)
    yield UploadDownloadPage(page)


@pytest.fixture(scope="module")
def dynamic_properties_page(page: Page):
    """Фикстура для страницы Dynamic Properties."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.DYNAMIC, selectors)
    yield DynamicPropertiesPage(page)


# Forms fixtures
@pytest.fixture(scope="module")
def practice_form_page(page: Page):
    """Фикстура для страницы Practice Form."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.PRACTICE_FORM, selectors)
    yield AutomationPracticeFormPage(page)


# Alerts fixtures
@pytest.fixture(scope="module")
def browser_windows_page(page: Page):
    """Фикстура для страницы Browser Windows."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.BROWSER_WINDOWS, selectors)
    yield BrowserWindowsPage(page)


@pytest.fixture(scope="module")
def alerts_page(page: Page):
    """Фикстура для страницы Alerts."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.ALERTS_PAGE, selectors)
    yield AlertsPage(page)


@pytest.fixture(scope="module")
def frames_page(page: Page):
    """Фикстура для страницы Frames."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.FRAMES_PAGE, selectors)
    yield FramesPage(page)


@pytest.fixture(scope="module")
def nested_frames_page(page: Page):
    """Фикстура для страницы Nested Frames."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.NESTED_FRAMES_PAGE, selectors)
    yield NestedFramesPage(page)


@pytest.fixture(scope="module")
def modal_page(page: Page):
    """Фикстура для страницы Modal Dialogs."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.MODAL_DIALOGS, selectors)
    yield ModalPage(page)


# Widgets fixtures
@pytest.fixture(scope="module")
def accordion_page(page: Page):
    """Фикстура для страницы Accordion."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.ACCORDION, selectors)
    yield AccordionPage(page)


@pytest.fixture(scope="module")
def auto_complete_page(page: Page):
    """Фикстура для страницы Auto Complete."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.AUTO_COMPLETE, selectors)
    yield AutoCompletePage(page)


@pytest.fixture(scope="module")
def date_picker_page(page: Page):
    """Фикстура для страницы Date Picker."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.DATE_PICKER, selectors)
    yield DatePickerPage(page)


@pytest.fixture(scope="module")
def slider_page(page: Page):
    """Фикстура для страницы Slider."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.SLIDER, selectors)
    yield SliderPage(page)


@pytest.fixture(scope="module")
def progress_bar_page(page: Page):
    """Фикстура для страницы Progress Bar."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.PROGRESS_BAR, selectors)
    yield ProgressBarPage(page)


@pytest.fixture(scope="module")
def tabs_page(page: Page):
    """Фикстура для страницы Tabs."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.TABS, selectors)
    yield TabsPage(page)


@pytest.fixture(scope="module")
def tool_tips_page(page: Page):
    """Фикстура для страницы Tool Tips."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.TOOL_TIPS, selectors)
    yield ToolTipsPage(page)


@pytest.fixture(scope="module")
def menu_page(page: Page):
    """Фикстура для страницы Menu."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.MENU, selectors)
    yield MenuPage(page)


@pytest.fixture(scope="module")
def select_menu_page(page: Page):
    """Фикстура для страницы Select Menu."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.SELECT_MENU, selectors)
    yield SelectMenuPage(page)


# Interactions fixtures
@pytest.fixture(scope="module")
def sortable_page(page: Page):
    """Фикстура для страницы Sortable."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.SORTABLE, selectors)
    yield SortablePage(page)


@pytest.fixture(scope="module")
def selectable_page(page: Page):
    """Фикстура для страницы Selectable."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.SELECTABLE, selectors)
    yield SelectablePage(page)


@pytest.fixture(scope="module")
def resizable_page(page: Page):
    """Фикстура для страницы Resizable."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.RESIZABLE, selectors)
    yield ResizablePage(page)


@pytest.fixture(scope="module")
def droppable_page(page: Page):
    """Фикстура для страницы Droppable."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.DROPPABLE, selectors)
    yield DroppablePage(page)


@pytest.fixture(scope="module")
def dragabble_page(page: Page):
    """Фикстура для страницы Dragabble."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.DRAGABBLE, selectors)
    yield DragabblePage(page)


# BookStore fixtures
@pytest.fixture(scope="module")
def login_page(page: Page):
    """Фикстура для страницы Login."""
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.LOGIN_PAGE, selectors)
    yield LoginPage(page)


@pytest.fixture(scope="module")
def authenticated_page(auth_context):
    """Фикстура для авторизованной страницы bookstore."""
    page = auth_context.new_page()
    yield LoginPage(page)
    page.close()


def pytest_configure(config):
    """Регистрирует кастомные маркеры pytest."""
    config.addinivalue_line(
        "markers", "dependency: marks tests with dependencies between them"
    )
    config.addinivalue_line("markers", "smoke: marks tests as smoke tests")
    config.addinivalue_line("markers", "regression: marks tests as regression tests")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для создания Allure аттачментов при падении тестов.
    Добавляет скриншоты и HTML снепшоты страницы.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Получаем page из фикстур теста
        page = None
        for fixture_name in [
            "page",
            "login_page",
            "links_page",
            "text_box_page",
            "buttons_page",
            "alerts_page",
            "practice_form_page",
        ]:
            if fixture_name in item.funcargs:
                page_obj = item.funcargs[fixture_name]
                page = getattr(page_obj, "page", page_obj)
                break

        if page and hasattr(page, "screenshot"):
            try:
                # Прикрепляем скриншот
                allure.attach(
                    page.screenshot(full_page=True),
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG,
                )

                # Прикрепляем HTML снепшот
                html_content = page.content()
                allure.attach(
                    html_content,
                    name="page_source",
                    attachment_type=allure.attachment_type.HTML,
                )
            except Exception as e:
                logger.warning(f"Не удалось создать аттачменты: {e}")


def pytest_sessionfinish(session, exitstatus):
    """
    Автоматически генерирует HTML отчет Allure после завершения тестов.
    Работает только если установлен allure CLI.
    """
    if shutil.which("allure"):
        results_dir = os.path.abspath("allure-results")
        report_dir = os.path.abspath("allure-report")

        if os.path.exists(results_dir):
            try:
                subprocess.run(
                    ["allure", "generate", results_dir, "-o", report_dir, "--clean"],
                    check=False,
                    capture_output=True,
                )
                logger.info(f"Allure отчет сгенерирован в: {report_dir}")
            except Exception as e:
                logger.warning(f"Не удалось сгенерировать Allure отчет: {e}")
