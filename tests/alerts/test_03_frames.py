from pages.alerts.frames_page import FramesPage


def test_frame1_heading(frames_page: FramesPage):
    heading = frames_page.get_frame1_heading_text()
    assert heading == "This is a sample page", f"Unexpected frame1 heading: {heading}"


def test_frame2_heading(frames_page: FramesPage):
    heading = frames_page.get_frame2_heading_text()
    assert heading == "This is a sample page", f"Unexpected frame2 heading: {heading}"
