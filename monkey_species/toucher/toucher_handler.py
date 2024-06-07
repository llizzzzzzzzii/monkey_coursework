from locators.clicker_toucher_locators import find_locators
from monkey_logging.monkey_logger import LogToucher
import random


def get_element_and_coordinate(page):
    page.wait_for_load_state("domcontentloaded")
    visible_elements = find_locators(page)
    if not visible_elements:
        LogToucher.logger.warning("Warning: The element was not found")
        return [], -1, -1
    element = random.choice(visible_elements)
    bounding_box = element.bounding_box()
    x, y = int(bounding_box['x'] + bounding_box['width'] / 2), int(bounding_box['y'] + bounding_box['height'] / 2)
    return element, x, y


def blocking_movement(page, initial_url):
    current_url = page.url
    if current_url != initial_url:
        page.goto(initial_url)


def open_new_tab(page, x, y, restricted_page):
    with page.context.expect_page() as new_page_info:
        page.touchscreen.tap(x, y)
    if not restricted_page:
        new_page = new_page_info.value
        new_page.bring_to_front()
        return new_page
    return page
