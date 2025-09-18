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

# def test_container_restricted_tab(dragabble_page):
#     dragabble_page.container_restricted_tab()
#
#     div_element = dragabble_page.page.locator(DragabbleLocators.DRAGGABLE_DIV_CONTAINER)
#     box_div_before = div_element.bounding_box()
#     dragabble_page.drag_box_container(DragabbleLocators.DRAGGABLE_DIV_CONTAINER, 50, 50)
#     box_div_after = div_element.bounding_box()
#     assert box_div_before != box_div_after, "Div container restricted drag box did not move"
#
#     span_element = dragabble_page.page.locator(DragabbleLocators.DRAGGABLE_SPAN_CONTAINER)
#     box_span_before = span_element.bounding_box()
#     dragabble_page.drag_box_container(DragabbleLocators.DRAGGABLE_SPAN_CONTAINER, 30, 30)
#     box_span_after = span_element.bounding_box()
#     assert box_span_before != box_span_after, "Span container restricted drag box did not move"

