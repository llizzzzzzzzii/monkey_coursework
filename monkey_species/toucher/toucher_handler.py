from monkey_logging.monkey_logger import LogToucher
import random
import time


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
    LogToucher.logger.warning("Warning: The element was not found")
    return None, -1, -1


def blocking_movement(page, element):
    page.evaluate("""
        (element) => {
            element.addEventListener('click', (event) => {
                event.preventDefault();
            });
        }
    """, element)


def open_new_tab(page, x, y):
    with page.context.expect_page() as new_page_info:
        page.touchscreen.tap(x, y)
    new_page = new_page_info.value
    new_page.bring_to_front()
    return new_page


def actions_with_restriction(page, x, y, has_href, tag_name):
    page.touchscreen.tap(x, y)
    if has_href and tag_name == 'img':
        time.sleep(0.3)
        page.keyboard.press("Escape")


def actions_unlimited(page, x, y, target_blank, has_href, tag_name):
    if target_blank:
        page = open_new_tab(page, x, y)
    elif has_href:
        with page.expect_navigation():
            page.touchscreen.tap(x, y)
        if tag_name == 'img':
            time.sleep(0.3)
            page.keyboard.press("Escape")
    else:
        page.touchscreen.tap(x, y)
        page.wait_for_load_state('networkidle')
    return page
