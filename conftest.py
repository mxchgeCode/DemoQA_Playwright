import pytest
from playwright.sync_api import sync_playwright


# Общая фикстура для запуска Playwright и браузера
@pytest.fixture(scope="module")
def browser():
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False)
    yield browser
    try:
        browser.close()
    except:
        pass
    try:
        pw.stop()
    except:
        pass


def create_page_with_wait(browser, url, wait_selectors, stabilize_timeout=1000):
    """Создаёт контекст и страницу с переходом на url и ожиданиями селекторов.

    wait_selectors - список кортежей (селектор, состояние, таймаут в мс)
    stabilize_timeout - дополнительная пауза для стабилизации в мс
    """
    context = browser.new_context()
    page = context.new_page()

    # Переход с повторными попытками
    for attempt in range(3):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            break
        except Exception as e:
            if attempt == 2:
                raise e
            page.wait_for_timeout(2000)

    # Ожидание селекторов
    for selector, state, timeout in wait_selectors:
        try:
            page.wait_for_selector(selector, state=state, timeout=timeout)
        except:
            pass

    page.wait_for_timeout(stabilize_timeout)

    try:
        page.wait_for_load_state("networkidle")
    except:
        pass

    return context, page


# Пример фикстур страниц с использованием общей логики

@pytest.fixture(scope="function")
def progress_page(browser):
    from pages.progress_bar_page import ProgressBarPage
    from data import URLs
    from locators.progress_bar_locators import ProgressBarLocators

    wait_selectors = [
        ("#app", "visible", 10000),
        (ProgressBarLocators.START_STOP_BUTTON, "visible", 15000),
        (ProgressBarLocators.PROGRESS_BAR, "visible", 10000),
    ]

    context, page = create_page_with_wait(browser, URLs.PROGRESS_BAR, wait_selectors, stabilize_timeout=4000)

    progress_page = ProgressBarPage(page)
    yield progress_page

    try:
        page.close()
        context.close()
    except:
        pass


@pytest.fixture(scope="module")
def slider_context(browser):
    context = browser.new_context()
    yield context
    try:
        context.close()
    except:
        pass


@pytest.fixture(scope="module")
def slider_page_instance(slider_context):
    from pages.slider_page import SliderPage
    from data import URLs

    context = slider_context
    page = context.new_page()

    page.goto(URLs.SLIDER_URL, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_selector(".range-slider", state="visible", timeout=10000)
    page.wait_for_selector("#sliderValue", state="visible", timeout=10000)

    slider_page = SliderPage(page)
    yield slider_page

    try:
        page.close()
    except:
        pass


@pytest.fixture(scope="function")
def slider_page(slider_page_instance):
    yield slider_page_instance


@pytest.fixture(scope="function")
def accordion_page(browser):
    from pages.accordion_page import AccordionPage
    from data import URLs

    wait_selectors = [
        ("div.accordion", "visible", 10000),
    ]

    context, page = create_page_with_wait(browser, URLs.ACCORDION_URL, wait_selectors, stabilize_timeout=1000)

    accordion_page = AccordionPage(page)
    yield accordion_page

    try:
        page.close()
        context.close()
    except:
        pass


@pytest.fixture(scope="function")
def autocomplete_page(browser):
    from pages.auto_complete_page import AutoCompletePage
    from data import URLs
    from locators.auto_complete_locators import AutoCompleteLocators

    wait_selectors = [
        (AutoCompleteLocators.SINGLE_COLOR_INPUT, "visible", 10000),
    ]

    context, page = create_page_with_wait(browser, URLs.AUTO_COMPLETE_URL, wait_selectors, stabilize_timeout=1000)

    autocomplete_page = AutoCompletePage(page)
    yield autocomplete_page

    try:
        page.close()
        context.close()
    except:
        pass


@pytest.fixture(scope="function")
def datepicker_page(browser):
    from pages.date_picker_page import DatePickerPage
    from data import URLs
    from locators.date_picker_locators import DatePickerLocators

    wait_selectors = [
        (DatePickerLocators.DATE_INPUT, "visible", 10000),
    ]

    context, page = create_page_with_wait(browser, URLs.DATE_PICKER_URL, wait_selectors, stabilize_timeout=2000)

    datepicker_page = DatePickerPage(page)
    yield datepicker_page

    try:
        page.close()
        context.close()
    except:
        pass


@pytest.fixture(scope="function")
def tabs_page(browser):
    from pages.tabs_page import TabsPage
    from data import URLs
    from locators.tabs_locators import TabsLocators

    wait_selectors = [
        (TabsLocators.TAB_WHAT, "visible", 10000),
    ]

    context, page = create_page_with_wait(browser, URLs.TABS_URL, wait_selectors, stabilize_timeout=2000)

    tabs_page = TabsPage(page)
    yield tabs_page

    try:
        page.close()
        context.close()
    except:
        pass


@pytest.fixture(scope="function")
def tooltips_page(browser):
    from pages.tool_tips_page import ToolTipsPage
    from data import URLs
    from locators.tool_tips_locators import ToolTipsLocators

    wait_selectors = [
        (ToolTipsLocators.HOVER_BUTTON, "visible", 10000),
    ]

    context, page = create_page_with_wait(browser, URLs.TOOL_TIPS_URL, wait_selectors, stabilize_timeout=3000)

    tooltips_page = ToolTipsPage(page)
    yield tooltips_page

    try:
        page.close()
        context.close()
    except:
        pass


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
