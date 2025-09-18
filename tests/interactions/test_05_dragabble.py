import logging

from pages.interactions.dragabble_page import  DragabbleLocators

logger = logging.getLogger(__name__)

def test_simple_drag(dragabble_page):
    dragabble_page.activate_simple_tab()
    before = dragabble_page.get_position(DragabbleLocators.SIMPLE_DRAG)
    dragabble_page.drag_element_by(DragabbleLocators.SIMPLE_DRAG, dx=100, dy=100)
    after = dragabble_page.get_position(DragabbleLocators.SIMPLE_DRAG)
    logger.info(f"Simple drag before: {before}, after: {after}")
    assert after["x"] > before["x"] and after["y"] > before["y"]

def test_axis_restriction(dragabble_page):
    dragabble_page.activate_axis_restriction_tab()
    before_x = dragabble_page.get_position(DragabbleLocators.AXIS_X_DRAG)
    dragabble_page.drag_element_by(DragabbleLocators.AXIS_X_DRAG, dx=100, dy=50)
    after_x = dragabble_page.get_position(DragabbleLocators.AXIS_X_DRAG)
    logger.info(f"Axis X drag before: {before_x}, after: {after_x}")
    assert after_x["x"] > before_x["x"]
    assert abs(after_x["y"] - before_x["y"]) < 5

    before_y = dragabble_page.get_position(DragabbleLocators.AXIS_Y_DRAG)
    dragabble_page.drag_element_by(DragabbleLocators.AXIS_Y_DRAG, dx=100, dy=50)
    after_y = dragabble_page.get_position(DragabbleLocators.AXIS_Y_DRAG)
    logger.info(f"Axis Y drag before: {before_y}, after: {after_y}")
    assert abs(after_y["x"] - before_y["x"]) < 5
    assert after_y["y"] > before_y["y"]

def test_container_restriction(dragabble_page):
    dragabble_page.activate_container_restriction_tab()
    before = dragabble_page.get_position(DragabbleLocators.CONTAINER_DRAG)
    dragabble_page.drag_element_by(DragabbleLocators.CONTAINER_DRAG, dx=500, dy=500)
    after = dragabble_page.get_position(DragabbleLocators.CONTAINER_DRAG)
    logger.info(f"Container restriction drag before: {before}, after: {after}")
    # Элемент не должен выйти за пределы контейнера, значит позиция не должна сильно меняться
    assert after["x"] >= before["x"]
    assert after["y"] >= before["y"]

def test_cursor_style(dragabble_page):
    dragabble_page.activate_cursor_style_tab()
    before = dragabble_page.get_position(DragabbleLocators.CURSOR_DRAG)
    dragabble_page.drag_element_by(DragabbleLocators.CURSOR_DRAG, dx=50, dy=50)
    after = dragabble_page.get_position(DragabbleLocators.CURSOR_DRAG)
    logger.info(f"Cursor style drag before: {before}, after: {after}")
    assert after["x"] > before["x"] and after["y"] > before["y"]
