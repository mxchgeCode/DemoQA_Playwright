from locators.interactions.dragabble_locators import DragabbleLocators


def test_drag_box_movement(dragabble_page):

    x_before, y_before = dragabble_page.get_drag_box_position()
    dragabble_page.drag_box(100, 100)
    x_after, y_after = dragabble_page.get_drag_box_position()

    assert (x_after != x_before) or (y_after != y_before), "Element did not move"


def test_axis_restricted_tab(dragabble_page):
    dragabble_page.axis_restricted_tab()

    elt_x = dragabble_page.page.locator(DragabbleLocators.DRAG_BOX_AXIS_X)
    box_x_before = elt_x.bounding_box()
    dragabble_page.drag_box_axis("x", 100)
    box_x_after = elt_x.bounding_box()
    assert box_x_before != box_x_after

    elt_y = dragabble_page.page.locator(DragabbleLocators.DRAG_BOX_AXIS_Y)
    box_y_before = elt_y.bounding_box()
    dragabble_page.drag_box_axis("y", 100)
    box_y_after = elt_y.bounding_box()
    assert box_y_before != box_y_after


def test_container_restricted_tab(dragabble_page):
    dragabble_page.container_restricted_tab()

    # Перемещение div элемента (все направления)
    div_locator = DragabbleLocators.DRAGGABLE_DIV_CONTAINER
    div_element = dragabble_page.page.locator(div_locator)
    box_div_before = div_element.bounding_box()
    dragabble_page.drag_box_container(div_locator, 50, 50)
    box_div_after = div_element.bounding_box()
    assert (
        box_div_before != box_div_after
    ), "Div container restricted drag box did not move"

    # Перемещение span элемента (только по вертикали)
    span_locator = DragabbleLocators.DRAGGABLE_SPAN_CONTAINER
    span_element = dragabble_page.page.locator(span_locator)
    box_span_before = span_element.bounding_box()

    dragabble_page.js_drag_vertical(span_locator, 50)

    box_span_after = span_element.bounding_box()
    assert (
        box_span_before != box_span_after
    ), "Span container restricted drag box did not move"


def test_cursor_style_tab(dragabble_page):
    dragabble_page.cursor_style_tab()

    # I will always stick to the center
    locator = DragabbleLocators.CURSOR_CENTER
    element = dragabble_page.page.locator(locator)
    box_before = element.bounding_box()
    dragabble_page.drag_box_cursor(locator, 40, 40)
    box_after = element.bounding_box()
    assert box_before != box_after, "Cursor Center box did not move"

    # My cursor is at top left
    locator = DragabbleLocators.CURSOR_TOP_LEFT
    element = dragabble_page.page.locator(locator)
    box_before = element.bounding_box()
    dragabble_page.drag_box_cursor(locator, 40, 40)
    box_after = element.bounding_box()
    assert box_before != box_after, "Cursor Top Left box did not move"

    # My cursor is at bottom
    locator = DragabbleLocators.CURSOR_BOTTOM
    element = dragabble_page.page.locator(locator)
    box_before = element.bounding_box()
    dragabble_page.drag_box_cursor(locator, 40, 40)
    box_after = element.bounding_box()
    assert box_before != box_after, "Cursor Bottom box did not move"
