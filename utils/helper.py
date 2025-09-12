import time


def wait_for_progress(progress_page, target, timeout=60):
    """Улучшенная функция ожидания прогресса."""
    start_time = time.time()
    target_value = int(target.replace("%", ""))

    while True:
        try:
            current_value_text = progress_page.get_progress_value()
            # Извлекаем числовое значение из строки (например, "50%" -> 50)
            current_value = int("".join(filter(str.isdigit, current_value_text)))

            # Проверяем, достигли ли мы целевого значения (с небольшим допуском)
            if current_value >= target_value - 1:  # Допуск в 1%
                return True

            # Проверяем таймаут
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    f"Progress did not reach {target} within {timeout} seconds. Last value: {current_value_text}"
                )

            # Небольшая пауза
            time.sleep(0.5)

        except ValueError:
            # Если не удалось преобразовать значение, продолжаем ожидание
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    f"Progress did not reach {target} within {timeout} seconds. Could not parse value: {current_value_text}"
                )
            time.sleep(0.5)
        except Exception as e:
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    f"Progress did not reach {target} within {timeout} seconds. Error: {str(e)}"
                )
            time.sleep(0.5)
