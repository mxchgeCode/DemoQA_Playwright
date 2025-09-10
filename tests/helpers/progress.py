import time
import pytest
from pages.progress_bar_page import ProgressBarPage

@pytest.fixture(scope="function")
def progress_page(page):
    progress_page = ProgressBarPage(page)
    page.goto("https://demoqa.com/progress-bar", timeout=60000)  # 60 секунд
    yield progress_page

def wait_for_progress(progress_page, target="50%", timeout=10):
    start_time = time.time()
    while True:
        value = progress_page.get_progress_value()
        if target in value:
            break
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Progress did not reach {target} within {timeout} seconds")
        time.sleep(0.1)