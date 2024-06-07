import random
import time
from locators.clicker_toucher_locators import find_locators
from locators.clicker_toucher_locators import is_image_and_has_target_blank_and_href
from indicattion.clicker_toucher_indication import draw_indicator
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


def get_element_and_coordinate(page):
    page.wait_for_load_state("domcontentloaded")
    visible_elements = find_locators(page)
    if not visible_elements:
        LogClicker.logger.warning("Warning: The element was not found")
        return [], -1, -1
    element = random.choice(visible_elements)
    bounding_box = element.bounding_box()
    x, y = int(bounding_box['x'] + bounding_box['width'] / 2), int(bounding_box['y'] + bounding_box['height'] / 2)
    return element, x, y


def open_new_tab(page, x, y, restricted_page, count):
    with page.context.expect_page() as new_page_info:
        mouse_click(page, x, y, count)
    if not restricted_page:
        new_page = new_page_info.value
        new_page.bring_to_front()
        return new_page
    return page


def blocking_movement(page, initial_url):
    current_url = page.url
    if current_url != initial_url:
        page.goto(initial_url)

def perform_click_action(page, indication, restricted_page, color, count):
    element, x, y = get_element_and_coordinate(page)
    if not element:
        return page, -1, -1
    if count == 0:
        if indication:
            draw_indicator(page, x, y, color)
        page.mouse.move(x, y)
        return page, x, y
    target_blank, has_href, tag_name = is_image_and_has_target_blank_and_href(page, element)
    initial_url = page.url
    if indication:
        for i in range(abs(count)):
            draw_indicator(page, x, y, color)
    try:
        if target_blank:
            page = open_new_tab(page, x, y, restricted_page, count)
        elif has_href:
            with page.expect_navigation():
                mouse_click(page, x, y, count)
        else:
            mouse_click(page, x, y, count)
            page.wait_for_load_state('networkidle')
        if tag_name == 'img':
            time.sleep(0.2+count*0.1)
            page.keyboard.press("Escape")
        if restricted_page:
            blocking_movement(page, initial_url)
    except PlaywrightTimeoutError:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
        return page, -1, -1
    return page, x, y
