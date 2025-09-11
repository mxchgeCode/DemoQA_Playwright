import time


def wait_for_progress(progress_page, target, timeout):
    start_time = time.time()
    while True:
        value = progress_page.get_progress_value()
        if target in value:
            break
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Progress did not reach {target} within {timeout} seconds")
        time.sleep(0.1)
