"""
Тесты для страницы Resizable.
Проверяет функциональность изменения размеров элементов:
- Изменение размеров элементов с ограничениями
- Изменение размеров без ограничений
- Проверка минимальных и максимальных размеров
- Валидация изменений размеров
"""

import pytest
import allure
from pages.interactions.resizable_page import ResizablePage


@allure.epic("Interactions")
@allure.feature("Resizable")
@allure.story("Resize with Restrictions")
@pytest.mark.interactions
@pytest.mark.smoke
def test_resize_element_with_restrictions(resizable_page: ResizablePage):
    """
    Тест изменения размера элемента с ограничениями.

    Проверяет элемент который имеет минимальные и максимальные размеры.
    """
    with allure.step("Получаем начальные размеры элемента с ограничениями"):
        initial_size = resizable_page.get_restricted_box_size()
        resizable_page.log_step(f"Начальный размер ограниченного блока: {initial_size}")

        allure.attach(str(initial_size), "initial_restricted_size", allure.attachment_type.JSON)

        assert initial_size["width"] > 0, f"Начальная ширина должна быть больше 0: {initial_size['width']}"
        assert initial_size["height"] > 0, f"Начальная высота должна быть больше 0: {initial_size['height']}"

    with allure.step("Получаем ограничения размеров"):
        size_restrictions = resizable_page.get_restricted_box_limits()
        resizable_page.log_step(f"Ограничения размеров: {size_restrictions}")

        allure.attach(str(size_restrictions), "size_restrictions", allure.attachment_type.JSON)

    with allure.step("Пытаемся увеличить размер элемента"):
        resizable_page.log_step("Попытка увеличения размера ограниченного блока")

        # Попытка увеличить на 100px в каждом направлении
        resize_result = resizable_page.resize_restricted_box(100, 100)
        resizable_page.log_step(f"Результат изменения размера: {resize_result}")

        assert resize_result, "Операция изменения размера должна быть выполнена"

    with allure.step("Проверяем новые размеры после увеличения"):
        resizable_page.page.wait_for_timeout(1000)  # Пауза для обновления

        new_size_after_increase = resizable_page.get_restricted_box_size()
        resizable_page.log_step(f"Размер после увеличения: {new_size_after_increase}")

        size_change_increase = {
            "initial_size": initial_size,
            "new_size": new_size_after_increase,
            "width_changed": new_size_after_increase["width"] != initial_size["width"],
            "height_changed": new_size_after_increase["height"] != initial_size["height"],
            "width_increase": new_size_after_increase["width"] - initial_size["width"],
            "height_increase": new_size_after_increase["height"] - initial_size["height"]
        }

        resizable_page.log_step(f"Изменения при увеличении: {size_change_increase}")
        allure.attach(str(size_change_increase), "size_increase_result", allure.attachment_type.JSON)

        # Проверяем что размер изменился
        size_actually_changed = (
            size_change_increase["width_changed"] or 
            size_change_increase["height_changed"]
        )

        assert size_actually_changed, f"Размер должен измениться при увеличении: {size_change_increase}"

    with allure.step("Пытаемся уменьшить размер элемента"):
        resizable_page.log_step("Попытка уменьшения размера ограниченного блока")

        # Попытка уменьшить на 50px в каждом направлении
        resize_decrease_result = resizable_page.resize_restricted_box(-50, -50)
        resizable_page.page.wait_for_timeout(1000)

        new_size_after_decrease = resizable_page.get_restricted_box_size()
        resizable_page.log_step(f"Размер после уменьшения: {new_size_after_decrease}")

        size_change_decrease = {
            "size_before_decrease": new_size_after_increase,
            "size_after_decrease": new_size_after_decrease,
            "width_decreased": new_size_after_decrease["width"] < new_size_after_increase["width"],
            "height_decreased": new_size_after_decrease["height"] < new_size_after_increase["height"],
            "within_min_limits": (
                new_size_after_decrease["width"] >= size_restrictions.get("min_width", 0) and
                new_size_after_decrease["height"] >= size_restrictions.get("min_height", 0)
            )
        }

        resizable_page.log_step(f"Изменения при уменьшении: {size_change_decrease}")
        allure.attach(str(size_change_decrease), "size_decrease_result", allure.attachment_type.JSON)

        # Проверяем что ограничения соблюдаются
        if size_restrictions.get("min_width") and size_restrictions.get("min_height"):
            assert size_change_decrease["within_min_limits"], "Размеры не должны нарушать минимальные ограничения"


@allure.epic("Interactions")
@allure.feature("Resizable")
@allure.story("Resize without Restrictions")
@pytest.mark.interactions
@pytest.mark.smoke
def test_resize_element_without_restrictions(resizable_page: ResizablePage):
    """
    Тест изменения размера элемента без ограничений.

    Проверяет элемент который может изменяться свободно.
    """
    with allure.step("Получаем начальные размеры свободного элемента"):
        initial_free_size = resizable_page.get_free_box_size()
        resizable_page.log_step(f"Начальный размер свободного элемента: {initial_free_size}")

        allure.attach(str(initial_free_size), "initial_free_size", allure.attachment_type.JSON)

        assert initial_free_size["width"] > 0, "Начальная ширина свободного элемента должна быть больше 0"
        assert initial_free_size["height"] > 0, "Начальная высота свободного элемента должна быть больше 0"

    with allure.step("Значительно увеличиваем размер свободного элемента"):
        resizable_page.log_step("Значительное увеличение размера свободного элемента")

        # Увеличиваем на 200px в каждом направлении
        large_resize_result = resizable_page.resize_free_box(200, 200)
        resizable_page.page.wait_for_timeout(1000)

        size_after_large_increase = resizable_page.get_free_box_size()
        resizable_page.log_step(f"Размер после значительного увеличения: {size_after_large_increase}")

        large_increase_change = {
            "initial_size": initial_free_size,
            "size_after_increase": size_after_large_increase,
            "width_change": size_after_large_increase["width"] - initial_free_size["width"],
            "height_change": size_after_large_increase["height"] - initial_free_size["height"],
            "significant_increase": (
                size_after_large_increase["width"] > initial_free_size["width"] + 50 or
                size_after_large_increase["height"] > initial_free_size["height"] + 50
            )
        }

        resizable_page.log_step(f"Результат значительного увеличения: {large_increase_change}")
        allure.attach(str(large_increase_change), "large_increase_result", allure.attachment_type.JSON)

        assert large_increase_change["significant_increase"], "Свободный элемент должен значительно увеличиваться"

    with allure.step("Значительно уменьшаем размер свободного элемента"):
        resizable_page.log_step("Значительное уменьшение размера свободного элемента")

        # Уменьшаем на 150px в каждом направлении
        large_decrease_result = resizable_page.resize_free_box(-150, -150)
        resizable_page.page.wait_for_timeout(1000)

        size_after_large_decrease = resizable_page.get_free_box_size()
        resizable_page.log_step(f"Размер после значительного уменьшения: {size_after_large_decrease}")

        large_decrease_change = {
            "size_before_decrease": size_after_large_increase,
            "size_after_decrease": size_after_large_decrease,
            "width_decrease": size_after_large_increase["width"] - size_after_large_decrease["width"],
            "height_decrease": size_after_large_increase["height"] - size_after_large_decrease["height"],
            "significant_decrease": (
                size_after_large_decrease["width"] < size_after_large_increase["width"] - 50 or
                size_after_large_decrease["height"] < size_after_large_increase["height"] - 50
            )
        }

        resizable_page.log_step(f"Результат значительного уменьшения: {large_decrease_change}")
        allure.attach(str(large_decrease_change), "large_decrease_result", allure.attachment_type.JSON)

        assert large_decrease_change["significant_decrease"], "Свободный элемент должен значительно уменьшаться"

    with allure.step("Проверяем финальные размеры"):
        final_size = resizable_page.get_free_box_size()

        resize_summary = {
            "initial_size": initial_free_size,
            "max_size_reached": size_after_large_increase,
            "final_size": final_size,
            "total_width_change": final_size["width"] - initial_free_size["width"],
            "total_height_change": final_size["height"] - initial_free_size["height"],
            "resize_operations_successful": large_resize_result and large_decrease_result
        }

        resizable_page.log_step(f"Итоги изменения размеров: {resize_summary}")
        allure.attach(str(resize_summary), "free_resize_summary", allure.attachment_type.JSON)

        assert resize_summary["resize_operations_successful"], "Все операции изменения размера должны быть успешными"


@allure.epic("Interactions")
@allure.feature("Resizable")
@allure.story("Resize Handles")
@pytest.mark.interactions
@pytest.mark.regression
def test_resize_handles_functionality(resizable_page: ResizablePage):
    """
    Тест функциональности ручек изменения размера.

    Проверяет различные ручки для изменения размеров.
    """
    handle_tests = []

    with allure.step("Тестируем различные ручки изменения размера"):
        # Список ручек для тестирования
        handles_to_test = [
            ("bottom-right", "Нижняя правая ручка"),
            ("right", "Правая ручка"),
            ("bottom", "Нижняя ручка")
        ]

        initial_size = resizable_page.get_restricted_box_size()
        resizable_page.log_step(f"Начальный размер для тестирования ручек: {initial_size}")

        for handle_position, handle_description in handles_to_test:
            with allure.step(f"Тестируем {handle_description}"):
                resizable_page.log_step(f"Тест ручки: {handle_description} ({handle_position})")

                # Проверяем видимость ручки
                handle_visible = resizable_page.is_resize_handle_visible(handle_position)

                if handle_visible:
                    # Пытаемся изменить размер через эту ручку
                    handle_resize_result = resizable_page.resize_by_handle(handle_position, 50, 50)
                    resizable_page.page.wait_for_timeout(500)

                    # Проверяем результат
                    size_after_handle = resizable_page.get_restricted_box_size()

                    handle_test_result = {
                        "handle_position": handle_position,
                        "handle_description": handle_description,
                        "handle_visible": handle_visible,
                        "resize_attempted": True,
                        "resize_successful": handle_resize_result,
                        "size_before": initial_size,
                        "size_after": size_after_handle,
                        "size_changed": size_after_handle != initial_size
                    }

                    # Возвращаем к исходному размеру для следующего теста
                    if handle_resize_result and size_after_handle != initial_size:
                        resizable_page.reset_restricted_box_size()
                        resizable_page.page.wait_for_timeout(500)

                else:
                    handle_test_result = {
                        "handle_position": handle_position,
                        "handle_description": handle_description,
                        "handle_visible": handle_visible,
                        "resize_attempted": False,
                        "resize_successful": False,
                        "size_before": initial_size,
                        "size_after": initial_size,
                        "size_changed": False
                    }

                handle_tests.append(handle_test_result)
                resizable_page.log_step(f"Результат тестирования ручки {handle_position}: {handle_test_result}")

    with allure.step("Анализируем функциональность ручек"):
        allure.attach(str(handle_tests), "handle_tests_results", allure.attachment_type.JSON)

        visible_handles = sum(1 for test in handle_tests if test["handle_visible"])
        working_handles = sum(1 for test in handle_tests if test["resize_successful"])
        handles_that_changed_size = sum(1 for test in handle_tests if test["size_changed"])

        handles_summary = {
            "total_handles_tested": len(handle_tests),
            "visible_handles": visible_handles,
            "working_handles": working_handles,
            "handles_that_changed_size": handles_that_changed_size,
            "any_handle_works": working_handles > 0,
            "handle_details": handle_tests
        }

        resizable_page.log_step(f"Итоги тестирования ручек: {handles_summary}")
        allure.attach(str(handles_summary), "handles_functionality_summary", allure.attachment_type.JSON)

        # Проверяем что хотя бы одна ручка работает
        assert handles_summary["any_handle_works"], f"Хотя бы одна ручка должна работать: работающих {working_handles}/{len(handle_tests)}"

        # Проверяем что есть видимые ручки
        assert visible_handles > 0, f"Должна быть видима хотя бы одна ручка: видимых {visible_handles}/{len(handle_tests)}"


@allure.epic("Interactions")
@allure.feature("Resizable")
@allure.story("Size Validation")
@pytest.mark.interactions
def test_resize_size_validation(resizable_page: ResizablePage):
    """
    Тест валидации размеров при изменении.

    Проверяет корректность размеров и ограничений.
    """
    validation_tests = []

    with allure.step("Получаем информацию о размерах элементов"):
        restricted_info = {
            "current_size": resizable_page.get_restricted_box_size(),
            "limits": resizable_page.get_restricted_box_limits(),
            "css_properties": resizable_page.get_restricted_box_css_properties()
        }

        free_info = {
            "current_size": resizable_page.get_free_box_size(),
            "css_properties": resizable_page.get_free_box_css_properties()
        }

        resizable_page.log_step(f"Информация об ограниченном элементе: {restricted_info}")
        resizable_page.log_step(f"Информация о свободном элементе: {free_info}")

        allure.attach(str(restricted_info), "restricted_element_info", allure.attachment_type.JSON)
        allure.attach(str(free_info), "free_element_info", allure.attachment_type.JSON)

    with allure.step("Тестируем валидность текущих размеров"):
        # Проверяем что текущие размеры логичны
        restricted_size_valid = (
            restricted_info["current_size"]["width"] > 0 and
            restricted_info["current_size"]["height"] > 0 and
            restricted_info["current_size"]["width"] < 2000 and  # Разумные пределы
            restricted_info["current_size"]["height"] < 2000
        )

        free_size_valid = (
            free_info["current_size"]["width"] > 0 and
            free_info["current_size"]["height"] > 0 and
            free_info["current_size"]["width"] < 2000 and
            free_info["current_size"]["height"] < 2000
        )

        current_sizes_validation = {
            "restricted_size_valid": restricted_size_valid,
            "free_size_valid": free_size_valid,
            "both_sizes_reasonable": restricted_size_valid and free_size_valid
        }

        validation_tests.append(("current_sizes", current_sizes_validation))
        resizable_page.log_step(f"Валидация текущих размеров: {current_sizes_validation}")

    with allure.step("Тестируем соблюдение ограничений"):
        limits = restricted_info["limits"]
        current_restricted_size = restricted_info["current_size"]

        limits_compliance = {
            "has_min_width": limits.get("min_width") is not None,
            "has_min_height": limits.get("min_height") is not None,
            "has_max_width": limits.get("max_width") is not None,
            "has_max_height": limits.get("max_height") is not None,
            "width_within_limits": True,
            "height_within_limits": True
        }

        # Проверяем соблюдение ограничений по ширине
        if limits.get("min_width"):
            limits_compliance["width_within_limits"] = current_restricted_size["width"] >= limits["min_width"]
        if limits.get("max_width"):
            limits_compliance["width_within_limits"] = limits_compliance["width_within_limits"] and current_restricted_size["width"] <= limits["max_width"]

        # Проверяем соблюдение ограничений по высоте
        if limits.get("min_height"):
            limits_compliance["height_within_limits"] = current_restricted_size["height"] >= limits["min_height"]
        if limits.get("max_height"):
            limits_compliance["height_within_limits"] = limits_compliance["height_within_limits"] and current_restricted_size["height"] <= limits["max_height"]

        limits_compliance["all_limits_respected"] = (
            limits_compliance["width_within_limits"] and 
            limits_compliance["height_within_limits"]
        )

        validation_tests.append(("limits_compliance", limits_compliance))
        resizable_page.log_step(f"Соблюдение ограничений: {limits_compliance}")

    with allure.step("Тестируем экстремальные изменения размеров"):
        # Пытаемся сделать элемент очень маленьким
        extreme_small_result = resizable_page.resize_restricted_box(-1000, -1000)
        resizable_page.page.wait_for_timeout(1000)

        size_after_extreme_small = resizable_page.get_restricted_box_size()

        # Возвращаем к нормальному размеру
        resizable_page.reset_restricted_box_size()
        resizable_page.page.wait_for_timeout(500)

        # Пытаемся сделать элемент очень большим
        extreme_large_result = resizable_page.resize_restricted_box(1000, 1000)
        resizable_page.page.wait_for_timeout(1000)

        size_after_extreme_large = resizable_page.get_restricted_box_size()

        extreme_resize_test = {
            "extreme_small_attempted": extreme_small_result,
            "size_after_extreme_small": size_after_extreme_small,
            "extreme_large_attempted": extreme_large_result,
            "size_after_extreme_large": size_after_extreme_large,
            "prevented_too_small": (
                size_after_extreme_small["width"] > 10 and 
                size_after_extreme_small["height"] > 10
            ),
            "handled_extreme_large": (
                size_after_extreme_large["width"] < 2000 and 
                size_after_extreme_large["height"] < 2000
            )
        }

        validation_tests.append(("extreme_resize", extreme_resize_test))
        resizable_page.log_step(f"Экстремальные изменения размеров: {extreme_resize_test}")

    with allure.step("Создаем итоговый отчет валидации"):
        allure.attach(str(validation_tests), "size_validation_tests", allure.attachment_type.JSON)

        validation_summary = {
            "total_validation_tests": len(validation_tests),
            "current_sizes_valid": validation_tests[0][1]["both_sizes_reasonable"],
            "limits_respected": validation_tests[1][1]["all_limits_respected"] if len(validation_tests) > 1 else True,
            "extreme_cases_handled": validation_tests[2][1]["prevented_too_small"] if len(validation_tests) > 2 else True,
            "overall_validation_passed": True
        }

        # Общая валидация
        validation_summary["overall_validation_passed"] = (
            validation_summary["current_sizes_valid"] and
            validation_summary["limits_respected"] and
            validation_summary["extreme_cases_handled"]
        )

        resizable_page.log_step(f"Итоги валидации размеров: {validation_summary}")
        allure.attach(str(validation_summary), "size_validation_summary", allure.attachment_type.JSON)

        assert validation_summary["current_sizes_valid"], "Текущие размеры должны быть валидными"
        assert validation_summary["overall_validation_passed"], "Общая валидация размеров должна пройти успешно"


@allure.epic("Interactions")
@allure.feature("Resizable")
@allure.story("Responsive Behavior")
@pytest.mark.interactions
def test_resizable_responsive_behavior(resizable_page: ResizablePage):
    """
    Тест отзывчивого поведения изменяемых элементов.

    Проверяет как элементы ведут себя при различных размерах экрана.
    """
    viewport_tests = []

    # Различные размеры окна для тестирования
    viewport_sizes = [
        (1920, 1080, "Desktop Large"),
        (1366, 768, "Desktop Medium"),
        (1024, 768, "Desktop Small"),
        (768, 1024, "Tablet Portrait")
    ]

    with allure.step("Тестируем поведение при различных размерах окна"):
        for width, height, description in viewport_sizes:
            with allure.step(f"Тест для {description} ({width}x{height})"):
                resizable_page.log_step(f"Изменение размера окна на {description}: {width}x{height}")

                # Изменяем размер окна браузера
                resizable_page.page.set_viewport_size({"width": width, "height": height})
                resizable_page.page.wait_for_timeout(1000)

                # Получаем размеры элементов после изменения viewport
                restricted_size_viewport = resizable_page.get_restricted_box_size()
                free_size_viewport = resizable_page.get_free_box_size()

                # Проверяем видимость элементов
                restricted_visible = resizable_page.is_restricted_box_visible()
                free_visible = resizable_page.is_free_box_visible()

                # Тестируем изменение размера в новом viewport
                resize_works_in_viewport = resizable_page.resize_restricted_box(20, 20)
                resizable_page.page.wait_for_timeout(500)

                size_after_viewport_resize = resizable_page.get_restricted_box_size()

                viewport_test = {
                    "viewport_size": {"width": width, "height": height},
                    "description": description,
                    "restricted_size": restricted_size_viewport,
                    "free_size": free_size_viewport,
                    "restricted_visible": restricted_visible,
                    "free_visible": free_visible,
                    "resize_works": resize_works_in_viewport,
                    "size_after_resize": size_after_viewport_resize,
                    "elements_fit_viewport": (
                        restricted_size_viewport["width"] <= width and
                        restricted_size_viewport["height"] <= height and
                        free_size_viewport["width"] <= width and
                        free_size_viewport["height"] <= height
                    )
                }

                viewport_tests.append(viewport_test)
                resizable_page.log_step(f"Результат для {description}: {viewport_test}")

                # Возвращаем элемент к исходному размеру
                if resize_works_in_viewport:
                    resizable_page.reset_restricted_box_size()

    with allure.step("Возвращаем стандартный размер окна"):
        resizable_page.page.set_viewport_size({"width": 1920, "height": 1080})
        resizable_page.page.wait_for_timeout(1000)

    with allure.step("Анализируем отзывчивое поведение"):
        allure.attach(str(viewport_tests), "viewport_tests_results", allure.attachment_type.JSON)

        viewports_with_visible_elements = sum(1 for test in viewport_tests if test["restricted_visible"] and test["free_visible"])
        viewports_with_working_resize = sum(1 for test in viewport_tests if test["resize_works"])
        viewports_with_fitting_elements = sum(1 for test in viewport_tests if test["elements_fit_viewport"])

        responsive_summary = {
            "total_viewport_tests": len(viewport_tests),
            "viewports_with_visible_elements": viewports_with_visible_elements,
            "viewports_with_working_resize": viewports_with_working_resize,
            "viewports_with_fitting_elements": viewports_with_fitting_elements,
            "responsive_behavior_good": viewports_with_visible_elements >= len(viewport_tests) // 2,
            "resize_works_across_viewports": viewports_with_working_resize >= len(viewport_tests) // 2,
            "viewport_details": viewport_tests
        }

        resizable_page.log_step(f"Итоги отзывчивого поведения: {responsive_summary}")
        allure.attach(str(responsive_summary), "responsive_behavior_summary", allure.attachment_type.JSON)

        # Проверяем что элементы ведут себя разумно в большинстве viewport
        assert responsive_summary["responsive_behavior_good"], f"Элементы должны быть видимы в большинстве размеров экрана: {viewports_with_visible_elements}/{len(viewport_tests)}"
        assert responsive_summary["resize_works_across_viewports"], f"Изменение размеров должно работать в большинстве viewport: {viewports_with_working_resize}/{len(viewport_tests)}"
