import pytest
from pages.progress_bar_page import ProgressBarPage
from data import URLs
from locators.progress_bar_locators import ProgressBarLocators


@pytest.fixture(scope="function")
def progress_page(page):
    progress_page = ProgressBarPage(page)
    page.goto(URLs.PROGRESS_BAR, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_selector(
        ProgressBarLocators.START_STOP_BUTTON, state="visible", timeout=10000
    )
    page.wait_for_selector(
        ProgressBarLocators.PROGRESS_BAR, state="visible", timeout=10000
    )
    yield progress_page


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
        # config.option.slowmo = 1000
