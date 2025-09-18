def test_parent_frame_text(nested_frames_page):
    text = nested_frames_page.get_parent_frame_text()
    assert text == "Parent frame", f"Unexpected parent frame text: {text}"


def test_child_frame_text(nested_frames_page):
    text = nested_frames_page.get_child_frame_text()
    assert text == "Child Iframe", f"Unexpected child frame text: {text}"
