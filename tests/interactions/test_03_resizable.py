from pages.interactions.resizable_page import ResizablePage


def test_resize_box_with_restriction(resizable_page: ResizablePage):
    before, after = resizable_page.resize_box(50, 50)
    assert after[0] > before[0], "Ширина блока должна увеличиться"
    assert after[1] > before[1], "Высота блока должна увеличиться"


def test_resize_button(resizable_page: ResizablePage):
    before, after = resizable_page.resize_button(100, 50)
    assert after[0] > before[0], "Ширина кнопки должна увеличиться"
    assert after[1] > before[1], "Высота кнопки должна увеличиться"
