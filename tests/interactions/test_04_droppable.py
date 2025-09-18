import logging

from locators.interactions.droppable_locators import DroppableLocators

logger = logging.getLogger(__name__)


def test_simple_droppable(droppable_page):
    droppable_page.activate_simple_tab()
    droppable_page.drag_simple()
    text = droppable_page.get_simple_drop_text()
    logger.info(f"Simple drop result text: {text}")
    assert text == "Dropped!", "Simple tab: drop failed"


def test_accept_droppable_non_accept(droppable_page):
    droppable_page.activate_accept_tab()

    # Непринимаемый элемент
    droppable_page.drag_accept(accepted=False)
    text_non_accept = droppable_page.get_accept_drop_text()
    logger.info(f"Accept drop text for non-accepted element: {text_non_accept}")
    # Здесь проверяем, что текст НЕ стал "Dropped!"

    assert (
        text_non_accept != "Dropped!"
    ), "Непринимаемый элемент не должен вызывать изменение текста зоны"

    # Принимаемый элемент
    droppable_page.drag_accept(accepted=True)
    text_accept = droppable_page.get_accept_drop_text()
    logger.info(f"Accept drop text for accepted element: {text_accept}")

    assert (
        text_accept == "Dropped!"
    ), "Принимаемый элемент должен вызвать изменение текста зоны"


def test_prevent_propagation(droppable_page):
    droppable_page.activate_prevent_tab()

    zones = [
        DroppableLocators.NOT_GREEDY_DROP_BOX,
        DroppableLocators.NOT_GREEDY_INNER_DROP_BOX,
        DroppableLocators.GREEDY_DROP_BOX,
        DroppableLocators.GREEDY_DROP_BOX_INNER,
    ]
    relative_positions = [
        (0.1, 0.5),  # Сдвиг к левому краю текста Outer droppable
        (0.5, 0.5),  # Центр для внутренней зоны
        (0.1, 0.5),  # Аналогично для greedy зоны
        (0.5, 0.5),
    ]

    for zone, rel_pos in zip(zones, relative_positions):
        logger.info(f"Dragging to {zone} at relative position {rel_pos}")
        droppable_page.drag_and_drop_to_position(
            DroppableLocators.DRAG_BOX, zone, rel_pos[0], rel_pos[1]
        )
        assert droppable_page.is_drop_zone_highlighted(
            zone
        ), f"Зона {zone} должна быть подсвечена после дропа"


def test_revert_draggable_non_revert(droppable_page):
    droppable_page.activate_revert_tab()

    before = droppable_page.get_position(DroppableLocators.REVERT_DRAG_NOT_REVERT)
    droppable_page.drag_revert(revert=True)
    after = droppable_page.get_position(DroppableLocators.REVERT_DRAG_NOT_REVERT)
    logger.info(f"Revert drag position before: {before}")
    logger.info(f"Revert drag position after: {after}")
    assert abs(after["x"] - before["x"]) < 5 and abs(after["y"] - before["y"]) < 5

    before = droppable_page.get_position(DroppableLocators.REVERT_DRAG_REVERT)
    droppable_page.drag_revert(revert=False)
    after = droppable_page.get_position(DroppableLocators.REVERT_DRAG_REVERT)
    logger.info(f"Revert drag position before: {before}")
    logger.info(f"Revert drag position after: {after}")
    assert abs(after["x"] - before["x"]) < 5 and abs(after["y"] - before["y"]) < 5
