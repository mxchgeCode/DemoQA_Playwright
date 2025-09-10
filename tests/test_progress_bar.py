from tests.helpers.progress import progress_page, wait_for_progress


def test_progress_bar_stops_and_resets(progress_page):
    progress_page.start_progress()
    wait_for_progress(progress_page, target="50%", timeout=10)

    progress_page.stop_progress()
    partial_result = progress_page.get_progress_value()
    print(f"Progress bar stopped at: {partial_result}")
    assert "50%" in partial_result

    progress_page.start_progress()
    wait_for_progress(progress_page, target="100%", timeout=10)

    full_result = progress_page.get_progress_value()
    print(f"Progress bar reached: {full_result}")
    assert "100%" in full_result

    # Нажать кнопку сброса
    progress_page.reset_progress()
    reset_result = progress_page.get_progress_value()
    print(f"Progress bar reset to: {reset_result}")
    assert reset_result == "0%" or reset_result == ""  # в зависимости от поведения сайта
