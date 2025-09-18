import time

import pytest
from playwright.sync_api import Browser, Page
from data import URLs
from pages.alerts.frames_page import FramesPage
from pages.alerts.nested_frames_page import NestedFramesPage

from pages.elements import (
    LinksPage,
    BrokenLinksPage,
    UploadDownloadPage,
    DynamicPropertiesPage,
    ButtonsPage,
    CheckBoxPage,
    RadioButtonPage,
    TextBoxPage,
    WebTablesPage,
)
from pages.forms import AutomationPracticeFormPage


from pages.alerts import (
    BrowserWindowsPage,
    AlertsPage,
    ModalDialogsPage,
)

from pages.widgets import (
    AccordionPage,
    AutoCompletePage,
    DatePickerPage,
    SliderPage,
    ProgressBarPage,
    TabsPage,
    ToolTipsPage,
    MenuPage,
    SelectMenuPage,
)


from pages.interactions import (
    SortablePage,
    SelectablePage,
    ResizablePage,
    DroppablePage,
    DragabblePage,
)

# Общий список блокировок ресурсов
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


# Функция блокировки запросов
def block_external(route):
    url = route.request.url.lower()
    resource_type = route.request.resource_type
    if resource_type in {"font", "image"}:
        route.abort()
        return
    if any(domain in url for domain in blocked_domains):
        route.abort()
        return
    route.continue_()


@pytest.fixture(scope="module")
def browser_context(playwright, browser_name, browser_context_args):
    # Основной браузерный контекст с блокировкой внешних запросов
    browser = getattr(playwright, browser_name).launch(headless=False)
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
        **browser_context_args,
    )
    context.route("**/*", block_external)
    yield context
    context.close()
    browser.close()


@pytest.fixture(scope="module")
def page(browser_context) -> Page:
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="module")
def context_without_blocking(browser: Browser):
    # Контекст без блокировки (для broken_links_page)
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    yield context
    context.close()


def create_page_with_wait(
    page: "Page",
    url: str,
    wait_selectors: list,
    stabilize_timeout: int = 1000,
    expected_status: int = 200,
):
    for attempt in range(3):
        try:
            url_with_cache_bypass = f"{url}?_={int(time.time())}"
            response = page.goto(
                url_with_cache_bypass, wait_until="domcontentloaded", timeout=30000
            )
            status = response.status if response else None
            if status not in (expected_status, 304):
                raise Exception(
                    f"HTTP статус {status}, ожидался {expected_status} или 304"
                )
            for selector, state, timeout in wait_selectors:
                page.locator(selector).wait_for(state=state, timeout=timeout)
            page.wait_for_timeout(stabilize_timeout)
            return
        except Exception as e:
            if attempt == 2:
                raise
            page.reload()


# Тестовые фикстуры для всех страниц раздела elements
@pytest.fixture(scope="module")
def links_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.LINKS_PAGE, selectors)
    yield LinksPage(page)


@pytest.fixture(scope="module")
def broken_links_page(browser: Browser):
    # Создаём контекст без блокировки
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
def upload_download_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.DOWNLOAD, selectors)
    yield UploadDownloadPage(page)


@pytest.fixture(scope="module")
def dynamic_properties_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.DYNAMIC, selectors)
    yield DynamicPropertiesPage(page)


@pytest.fixture(scope="module")
def buttons_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.PAGE_BTN, selectors)
    yield ButtonsPage(page)


@pytest.fixture(scope="function")
def check_box_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.CHECK_BOX, selectors)
    yield CheckBoxPage(page)


@pytest.fixture(scope="function")
def radio_button_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.RADIO_BTN, selectors)
    yield RadioButtonPage(page)


@pytest.fixture(scope="module")
def text_box_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.TEXT_BOX, selectors)
    yield TextBoxPage(page)


@pytest.fixture(scope="module")
def web_tables_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.WEB_TABLES, selectors)
    yield WebTablesPage(page)


@pytest.fixture(scope="module")
def slider_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.SLIDER, selectors)
    yield SliderPage(page)


@pytest.fixture(scope="module")
def progress_bar_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.PROGRESS_BAR, selectors)
    yield ProgressBarPage(page)


@pytest.fixture(scope="module")
def accordion_page(page: "Page"):
    selectors = [("#app", "visible", 60000)]
    create_page_with_wait(page, URLs.ACCORDION, selectors)
    yield AccordionPage(page)


@pytest.fixture(scope="module")
def autocomplete_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.AUTOCOMPLETE, selectors)
    yield AutoCompletePage(page)


@pytest.fixture(scope="module")
def datepicker_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.DATE_PICKER, selectors)
    yield DatePickerPage(page)


@pytest.fixture(scope="module")
def tabs_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.TABS, selectors)
    yield TabsPage(page)


@pytest.fixture(scope="module")
def tooltips_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.TOOLTIPS, selectors)
    yield ToolTipsPage(page)


@pytest.fixture(scope="module")
def select_menu_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.SELECT_MENU, selectors)
    yield SelectMenuPage(page)


@pytest.fixture(scope="module")
def menu_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.MENU, selectors)
    yield MenuPage(page)


@pytest.fixture(scope="module")
def practice_form_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.PRACTICE_FORM, selectors)
    yield AutomationPracticeFormPage(page)


@pytest.fixture(scope="module")
def browser_windows_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.BROWSER_WINDOWS, selectors)
    yield BrowserWindowsPage(page)


@pytest.fixture(scope="module")
def alerts_page(page: "Page"):
    page.set_default_timeout(10000)
    page.set_default_navigation_timeout(10000)
    selectors = [("#app", "visible", 10000)]
    # Изначальный переход с ожиданием нужных элементов
    create_page_with_wait(page, URLs.ALERTS, selectors)
    # Дальше дополнительный переход с нужными параметрами, если необходимо
    page.goto(URLs.ALERTS, wait_until="domcontentloaded", timeout=0)
    # Дополнительное ожидание конкретного элемента на странице
    page.wait_for_selector("#alertButton", timeout=10000)
    yield AlertsPage(page)


@pytest.fixture(scope="module")
def modal_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.MODAL_DIALOGS, selectors)
    yield ModalDialogsPage(page)


@pytest.fixture(scope="module")
def frames_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.FRAMES, selectors)
    yield FramesPage(page)


@pytest.fixture(scope="module")
def nested_frames_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.NESTED_FRAMES, selectors)
    yield NestedFramesPage(page)


import logging

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def sortable_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.SORTABLE, selectors)
    yield SortablePage(page)


@pytest.fixture(scope="module")
def selectable_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.SELECTABLE, selectors)
    yield SelectablePage(page)


@pytest.fixture(scope="module")
def resizable_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.RESIZABLE, selectors)
    yield ResizablePage(page)


@pytest.fixture(scope="module")
def droppable_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.DROPPABLE, selectors)
    yield DroppablePage(page)


@pytest.fixture(scope="module")
def dragabble_page(page: "Page"):
    selectors = [("#app", "visible", 10000)]
    create_page_with_wait(page, URLs.DRAGABBLE, selectors)
    yield DragabblePage(page)