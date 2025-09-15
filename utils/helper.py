import time


def wait_for_progress(progress_page, target, timeout=60):
    """Ожидание достижения значения прогресса с таймаутом."""
    start_time = time.time()
    target_value = int(target.replace("%", ""))
    while True:
        try:
            current_value_text = progress_page.get_progress_value()
            current_value = int("".join(filter(str.isdigit, current_value_text)))
            if current_value >= target_value - 1:  # Допуск 1%
                return True
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    f"Progress did not reach {target} within {timeout} seconds. Last: {current_value_text}"
                )
            time.sleep(0.5)
        except ValueError:
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    f"Progress did not reach {target} within {timeout} seconds. Couldn't parse value."
                )
            time.sleep(0.5)
        except Exception as e:
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    f"Progress did not reach {target} within {timeout} seconds. Error: {str(e)}"
                )
            time.sleep(0.5)
