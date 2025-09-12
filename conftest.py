import pytest
from playwright.sync_api import sync_playwright
from pages.slider_page import SliderPage
from pages.progress_bar_page import ProgressBarPage
from data import URLs
from locators.progress_bar_locators import ProgressBarLocators
from locators.auto_complete_locators import AutoCompleteLocators
from locators.date_picker_locators import DatePickerLocators
from locators.tabs_locators import TabsLocators
from locators.tool_tips_locators import ToolTipsLocators


# --- Фикстура для ProgressBarPage - отдельный браузер для прогресс-бара ---
@pytest.fixture(scope="module")
def progress_browser():
    """Создаёт браузер для модуля прогресс-бара."""
    pw = None
    browser = None
    try:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=False)
        yield browser
    finally:
        if browser:
            try:
                browser.close()
            except:
                pass
        if pw:
            try:
                pw.stop()
            except:
                pass


@pytest.fixture(scope="function")
def progress_page(progress_browser):
    """Создаёт новую страницу для каждого теста progress bar."""
    context = progress_browser.new_context()
    page = context.new_page()

    progress_page = ProgressBarPage(page)

    # Навигация с повторными попытками
    for attempt in range(3):
        try:
            page.goto(URLs.PROGRESS_BAR, wait_until="domcontentloaded", timeout=30000)
            break
        except Exception as e:
            if attempt == 2:  # Последняя попытка
                raise e
            page.wait_for_timeout(2000)  # Ждем перед повторной попыткой

    # Ждем появления основного контейнера страницы
    page.wait_for_selector("#app", state="visible", timeout=10000)

    # Ждем появления кнопки Start/Stop с более гибкими условиями
    try:
        page.wait_for_selector(
            ProgressBarLocators.START_STOP_BUTTON, state="visible", timeout=15000
        )
    except:
        # Если не нашли по ID, пробуем найти кнопку по тексту
        page.wait_for_selector("button", state="visible", timeout=10000)

    # Ждем прогресс бар
    try:
        page.wait_for_selector(
            ProgressBarLocators.PROGRESS_BAR, state="visible", timeout=10000
        )
    except:
        pass  # Продолжаем, даже если прогресс бар не найден сразу

    # Увеличенная стабилизация страницы
    page.wait_for_timeout(4000)
    try:
        page.wait_for_load_state("networkidle")
    except:
        pass

    yield progress_page

    # Очистка с обработкой исключений
    try:
        page.close()
        context.close()
    except:
        pass


# --- Фикстура для SliderPage - отдельный браузер для слайдера ---
@pytest.fixture(scope="module")
def slider_browser():
    """Создаёт браузер для модуля слайдера."""
    pw = None
    browser = None
    try:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=False)
        yield browser
    finally:
        if browser:
            try:
                browser.close()
            except:
                pass
        if pw:
            try:
                pw.stop()
            except:
                pass


@pytest.fixture(scope="module")
def slider_context(slider_browser):
    """Создаёт контекст для всех тестов слайдера."""
    context = slider_browser.new_context()
    yield context
    try:
        context.close()
    except:
        pass


@pytest.fixture(scope="module")
def slider_page_instance(slider_context):
    """Создаёт одну страницу для всех тестов слайдера."""
    page = slider_context.new_page()
    slider_page = SliderPage(page)
    page.goto(URLs.SLIDER_URL, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_selector(".range-slider", state="visible", timeout=10000)
    page.wait_for_selector("#sliderValue", state="visible", timeout=10000)

    yield slider_page

    try:
        page.close()
    except:
        pass


@pytest.fixture(scope="function")
def slider_page(slider_page_instance):
    """Возвращает одну и ту же страницу для каждого теста слайдера."""
    yield slider_page_instance


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


# --- Фикстура для AccordionPage - отдельный браузер для аккордеона ---
@pytest.fixture(scope="module")
def accordion_browser():
    """Создаёт браузер для модуля аккордеона."""
    pw = None
    browser = None
    try:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=False)
        yield browser
    finally:
        if browser:
            try:
                browser.close()
            except:
                pass
        if pw:
            try:
                pw.stop()
            except:
                pass


@pytest.fixture(scope="function")
def accordion_page(accordion_browser):
    """Создаёт новую страницу для каждого теста accordion."""
    from pages.accordion_page import AccordionPage

    context = accordion_browser.new_context()
    page = context.new_page()

    accordion_page = AccordionPage(page)
    page.goto(URLs.ACCORDION_URL, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_selector("div.accordion", state="visible", timeout=10000)

    # Небольшая задержка для стабилизации страницы
    page.wait_for_timeout(1000)

    yield accordion_page

    # Очистка
    try:
        page.close()
        context.close()
    except:
        pass


# --- Фикстура для AutoCompletePage - отдельный браузер для auto complete ---
@pytest.fixture(scope="module")
def autocomplete_browser():
    """Создаёт браузер для модуля auto complete."""
    pw = None
    browser = None
    try:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=False)
        yield browser
    finally:
        if browser:
            try:
                browser.close()
            except:
                pass
        if pw:
            try:
                pw.stop()
            except:
                pass


@pytest.fixture(scope="function")
def autocomplete_page(autocomplete_browser):
    """Создаёт новую страницу для каждого теста auto complete."""
    from pages.auto_complete_page import AutoCompletePage

    context = autocomplete_browser.new_context()
    page = context.new_page()

    autocomplete_page = AutoCompletePage(page)
    page.goto(URLs.AUTO_COMPLETE_URL, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_selector(
        AutoCompleteLocators.SINGLE_COLOR_INPUT, state="visible", timeout=10000
    )

    # Небольшая задержка для стабилизации страницы
    page.wait_for_timeout(1000)

    yield autocomplete_page

    # Очистка
    try:
        page.close()
        context.close()
    except:
        pass


# --- Фикстура для DatePickerPage - отдельный браузер для date picker ---
@pytest.fixture(scope="module")
def datepicker_browser():
    """Создаёт браузер для модуля date picker."""
    pw = None
    browser = None
    try:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=False)
        yield browser
    finally:
        if browser:
            try:
                browser.close()
            except:
                pass
        if pw:
            try:
                pw.stop()
            except:
                pass


@pytest.fixture(scope="function")
def datepicker_page(datepicker_browser):
    """Создаёт новую страницу для каждого теста date picker."""
    from pages.date_picker_page import DatePickerPage

    context = datepicker_browser.new_context()
    page = context.new_page()

    datepicker_page = DatePickerPage(page)
    page.goto(URLs.DATE_PICKER_URL, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_selector(
        DatePickerLocators.DATE_INPUT, state="visible", timeout=10000
    )

    # Небольшая задержка для стабилизации страницы
    page.wait_for_timeout(2000)

    yield datepicker_page

    # Очистка
    try:
        page.close()
        context.close()
    except:
        pass


# --- Фикстура для TabsPage - отдельный браузер для tabs ---
@pytest.fixture(scope="module")
def tabs_browser():
    """Создаёт браузер для модуля tabs."""
    pw = None
    browser = None
    try:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=False)
        yield browser
    finally:
        if browser:
            try:
                browser.close()
            except:
                pass
        if pw:
            try:
                pw.stop()
            except:
                pass


@pytest.fixture(scope="function")
def tabs_page(tabs_browser):
    """Создаёт новую страницу для каждого теста tabs."""
    from pages.tabs_page import TabsPage

    context = tabs_browser.new_context()
    page = context.new_page()

    tabs_page = TabsPage(page)
    page.goto(URLs.TABS_URL, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_selector(TabsLocators.TAB_WHAT, state="visible", timeout=10000)

    # Небольшая задержка для стабилизации страницы
    page.wait_for_timeout(2000)

    yield tabs_page

    # Очистка
    try:
        page.close()
        context.close()
    except:
        pass


# --- Фикстура для ToolTipsPage - отдельный браузер для tool tips ---
@pytest.fixture(scope="module")
def tooltips_browser():
    """Создаёт браузер для модуля tool tips."""
    pw = None
    browser = None
    try:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=False)
        yield browser
    finally:
        if browser:
            try:
                browser.close()
            except:
                pass
        if pw:
            try:
                pw.stop()
            except:
                pass


@pytest.fixture(scope="function")
def tooltips_page(tooltips_browser):
    """Создаёт новую страницу для каждого теста tool tips."""
    from pages.tool_tips_page import ToolTipsPage

    context = tooltips_browser.new_context()
    page = context.new_page()

    tooltips_page = ToolTipsPage(page)
    page.goto(URLs.TOOL_TIPS_URL, wait_until="domcontentloaded", timeout=30000)

    # Ждем загрузку основных элементов
    page.wait_for_selector(
        ToolTipsLocators.HOVER_BUTTON, state="visible", timeout=10000
    )

    # Небольшая задержка для стабилизации страницы
    page.wait_for_timeout(3000)

    yield tooltips_page

    # Очистка
    try:
        page.close()
        context.close()
    except:
        pass
