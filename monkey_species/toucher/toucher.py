from monkey_logging.monkey_logger import LogToucher
from monkey_logging.monkey_logger import LogError
from playwright._impl._errors import TimeoutError as PlaywrightTimeoutError
from indicattion.clicker_toucher_indication import draw_indicator
from locators.clicker_toucher_locators import find_locators
from locators.clicker_toucher_locators import is_image_and_has_target_blank_and_href
import random
import time


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


def touch(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    if not element:
        return page
    try:
        target_blank, has_href, tag_name = is_image_and_has_target_blank_and_href(page, element)
        initial_url = page.url
        if indication:
            draw_indicator(page, x, y, color)
        if target_blank:
            page = open_new_tab(page, x, y, restricted_page)
        elif has_href:
            with page.expect_navigation():
                page.touchscreen.tap(x, y)
        else:
            page.touchscreen.tap(x, y)
            page.wait_for_load_state('networkidle')
        if tag_name == 'img':
            time.sleep(0.3)
            page.keyboard.press("Escape")
        if restricted_page:
            blocking_movement(page, initial_url)
        LogToucher.logger.info(f"Tapped on an element at position {x, y}")
    except PlaywrightTimeoutError:
        LogToucher.logger.warning("Warning: The waiting time for the action has been exceeded")
        return page
    except Exception as e:
        LogToucher.logger.error("Error: Touch failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
    return page
