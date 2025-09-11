import pytest
from playwright.sync_api import Page, BrowserContext
from pages.slider_page import SliderPage
from pages.progress_bar_page import ProgressBarPage
from data import URLs
from locators.progress_bar_locators import ProgressBarLocators


@pytest.fixture(scope="function")
def progress_page(page: Page):
    """Фикстура для ProgressBar — работает с отдельной страницей."""
    progress_page = ProgressBarPage(page)
    page.goto(URLs.PROGRESS_BAR, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_selector(
        ProgressBarLocators.START_STOP_BUTTON, state="visible", timeout=10000
    )
    page.wait_for_selector(
        ProgressBarLocators.PROGRESS_BAR, state="visible", timeout=10000
    )
    yield progress_page


@pytest.fixture(scope="module")
def browser_context():
    """Создаёт один контекст браузера для всех тестов слайдера."""
    from playwright.sync_api import sync_playwright

    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)  # Для CI: headless=True
    context = browser.new_context()
    yield context
    context.close()
    browser.close()
    p.stop()


@pytest.fixture(scope="module")
def slider_page(browser_context: BrowserContext):
    """Создаёт одну страницу и возвращает SliderPage — один раз на модуль."""
    page = browser_context.new_page()
    slider_page = SliderPage(page)
    page.goto(URLs.SLIDER_URL, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_selector(".range-slider", state="visible", timeout=10000)
    page.wait_for_selector("#sliderValue", state="visible", timeout=10000)
    yield slider_page


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
