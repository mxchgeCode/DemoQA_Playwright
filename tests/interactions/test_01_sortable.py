import logging
from pages.interactions.sortable_page import SortablePage

logger = logging.getLogger(__name__)


def test_list_sortable_drag_and_drop(sortable_page: SortablePage):
    sortable_page.activate_list_tab()
    original_items = sortable_page.get_item_texts()
    logger.info(f"Исходный порядок List: {original_items}")
    assert len(original_items) > 1

    sortable_page.drag_and_drop_item(0, len(original_items) - 1)
    # Пауза для наблюдения результата
    sortable_page.page.wait_for_timeout(2000)

    new_items = sortable_page.get_item_texts()
    logger.info(f"Новый порядок List: {new_items}")
    assert new_items[-1] == original_items[0], "Первый элемент должен стать последним"
    assert new_items != original_items


def test_grid_sortable_drag_and_drop(sortable_page: SortablePage):
    sortable_page.activate_grid_tab()
    original_grid_items = sortable_page.get_grid_item_texts()
    logger.info(f"Исходный порядок Grid: {original_grid_items}")
    assert len(original_grid_items) > 1

    sortable_page.drag_and_drop_grid_item(0, len(original_grid_items) - 1)
    # Пауза для наблюдения результата
    sortable_page.page.wait_for_timeout(2000)

    new_grid_items = sortable_page.get_grid_item_texts()
    logger.info(f"Новый порядок Grid: {new_grid_items}")
    assert (
        new_grid_items[-1] == original_grid_items[0]
    ), "Первый grid элемент должен стать последним"
    assert new_grid_items != original_grid_items
