import random
import time
from locators.clicker_toucher_locators import is_image_and_has_target_blank_and_href
from indication.clicker_toucher_indication import draw_indicator
from monkey_logging.monkey_logger import LogClicker
from playwright._impl._errors import TimeoutError as PlaywrightTimeoutError


def mouse_click(page, x, y, count):
    if count == -1:
        page.mouse.click(x, y, delay=3000)
    elif count == 1:
        page.mouse.click(x, y)
    elif count == 2:
        page.mouse.dblclick(x, y)
    else:
        page.mouse.click(x, y, click_count=count)


def get_element_and_coordinate(page, selectors):
    page.wait_for_load_state("domcontentloaded")
    while selectors:
        selector = random.choice(selectors)
        element = page.query_selector(selector)
        if not element:
            return None, -1, -1
        bounding_box = element.bounding_box()
        element_top = bounding_box['y']
        element_bottom = element_top + bounding_box['height']
        viewport_height = page.viewport_size['height']
        if element_top >= 0 and element_bottom <= viewport_height:
            x, y = int(bounding_box['x'] + bounding_box['width'] / 2), int(
                bounding_box['y'] + bounding_box['height'] / 2)
            return element, x, y
        else:
            selectors.remove(selector)
    LogClicker.logger.warning("Warning: The element was not found")
    return None, -1, -1


def open_new_tab(page, x, y, count):
    with page.context.expect_page() as new_page_info:
        mouse_click(page, x, y, count)
    new_page = new_page_info.value
    new_page.bring_to_front()
    return new_page


def blocking_movement(page, element):
    page.evaluate("""
        (element) => {
            element.addEventListener('click', (event) => {
                event.preventDefault();
            });
        }
    """, element)


def actions_with_restriction(page, x, y, has_href, tag_name, count):
    mouse_click(page, x, y, count)
    if has_href and tag_name == 'img':
        time.sleep(0.2 + count * 0.1)
        page.keyboard.press("Escape")


def actions_unlimited(page, x, y, target_blank, has_href, tag_name, count):
    if target_blank:
        page = open_new_tab(page, x, y, count)
    elif has_href:
        with page.expect_navigation():
            mouse_click(page, x, y, count)
    if tag_name == 'img':
        time.sleep(0.2 + count * 0.1)
        page.keyboard.press("Escape")
    else:
        mouse_click(page, x, y, count)
        page.wait_for_load_state('networkidle')
    return page


def perform_click_action(page, indication, restricted_page, color, count, selectors):
    element, x, y = get_element_and_coordinate(page, selectors)
    if not element:
        return page, -1, -1
    if count == 0:
        if indication:
            draw_indicator(page, x, y, color)
        page.mouse.move(x, y)
        return page, x, y
    target_blank, has_href, tag_name = is_image_and_has_target_blank_and_href(page, element)
    if indication:
        for i in range(abs(count)):
            draw_indicator(page, x, y, color)
    try:
        if restricted_page:
            blocking_movement(page, element)
            actions_with_restriction(page, x, y, has_href, tag_name, count)
        else:
            page = actions_unlimited(page, x, y, target_blank, has_href, tag_name, count)
    except PlaywrightTimeoutError:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
        return page, -1, -1
    return page, x, y
