import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from data import URLs
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
from pages.forms import AutomationPracticeFormPage

# Общий список блокировок ресурсов
blocked_domains = [
    "doubleclick.net",
    "googlesyndication.com",
    "pagead2.googlesyndication.com",
    "adservice.google.com",
    "google-analytics.com",
    "analytics.google.com",
    "googletagmanager.com",
    "facebook.com",
]


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
def browser():
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False)
    yield browser
    browser.close()
    pw.stop()


@pytest.fixture(scope="module")
def context(browser: "Browser"):
    context = browser.new_context(
        ignore_https_errors=True,
        bypass_csp=True,
        viewport={"width": 1920, "height": 1080},
    )
    context.route("**/*", block_external)
    yield context
    context.close()


@pytest.fixture(scope="module")
def page(context: "BrowserContext"):
    page = context.new_page()
    yield page
    page.close()


# Универсальная функция для создания странички с ожиданиями
def create_page_with_wait(
    page: "Page",
    url: str,
    wait_selectors: list,
    stabilize_timeout: int = 1000,
    expected_status: int = 200,
):
    for attempt in range(3):
        try:
            response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
            status = response.status if response else None
            if status != expected_status:
                raise Exception(f"HTTP статус {status}, ожидался {expected_status}")
            break
        except Exception:
            if attempt == 2:
                raise
            page.wait_for_timeout(2000)
    for selector, state, timeout in wait_selectors:
        page.wait_for_selector(selector, state=state, timeout=timeout)
    if stabilize_timeout > 0:
        page.wait_for_timeout(stabilize_timeout)


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
