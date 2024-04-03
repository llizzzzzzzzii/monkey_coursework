import time
import random
from monkey_logging.monkey_logger.monkey_logger import LogClicker
from monkey_logging.monkey_logger.monkey_logger import LogError


def blocking_movement(page, initial_url):
    current_url = page.url
    if current_url != initial_url:
        page.goto(initial_url)


def find_locators(page):
    page.wait_for_load_state("load")
    clickable_elements = page.query_selector_all('button, a, input, input[role="button"]')
    viewport_height = page.viewport_size['height']
    visible_clickable_elements = [element for element in clickable_elements if element.is_visible() and
                                  element.bounding_box()['y'] >= 0 and element.bounding_box()['y'] <= viewport_height
                                  and element.get_attribute('type') != 'url']
    return visible_clickable_elements


def draw_indicator(page, element):
    box = element.bounding_box()
    x = box['x'] + box['width'] / 2
    y = box['y'] + box['height'] / 2
    page.evaluate('''
      circle = document.createElement('div');
      circle.style.width = '15px';
      circle.style.height = '15px';
      circle.style.borderRadius = '50%';
      circle.style.backgroundColor = 'rgba(255, 0, 0, 0.7)';
      circle.style.position = 'absolute';
      circle.style.left = '{}px';
      circle.style.top = '{}px';
      circle.style.zIndex = '10000';
      circle.style.pointerEvents = 'none';
      document.body.appendChild(circle);
      setTimeout(() => circle.remove(), 1000);
    '''.format(x, y))


def random_action():
    actions = [hover, click, double_click, click_and_hold]
    get_random = random.choice(actions)
    return get_random


def get_element_and_coordinate(page):
    page.wait_for_load_state("load")
    visible_elements = find_locators(page)
    element = random.choice(visible_elements)
    x, y = element.bounding_box()["x"], element.bounding_box()["y"]
    height, width = element.bounding_box()["height"], element.bounding_box()["width"]
    x = int(x + width / 2)
    y = int(y + height / 2)
    return element, x, y


def click(page, indication, restricted_page):
    element, x, y = get_element_and_coordinate(page)
    initial_url = page.url
    try:
        if indication:
            draw_indicator(page, element)
        element.click()
        if restricted_page:
            blocking_movement(page, initial_url)
    except Exception:
        LogError.logger.exception("Click failed")
        exit()
    LogClicker.logger.info(f"Clicked at position {x, y}")


def double_click(page, indication, restricted_page):
    element, x, y = get_element_and_coordinate(page)
    initial_url = page.url
    try:
        if indication:
            draw_indicator(page, element)
            draw_indicator(page, element)
        element.dblclick()
        if restricted_page:
            blocking_movement(page, initial_url)
    except Exception:
        LogError.logger.exception("Double click failed")
        exit()
    LogClicker.logger.info(f"Clicked at position {x, y} 2 times")


def multiple_click(page, indication, restricted_page):
    element, x, y = get_element_and_coordinate(page)
    count = random.randint(3, 10)
    initial_url = page.url
    try:
        for i in range(count):
            if indication:
                draw_indicator(page, element)
            element.click()
            if restricted_page:
                blocking_movement(page, initial_url)
    except Exception:
        LogError.logger.exception("Multiple clicks failed")
        exit()
    LogClicker.logger.info(f"Clicked at position {x, y} {count} times")


def hover(page, indication, restricted_page):
    element, x, y = get_element_and_coordinate(page)
    try:
        if indication:
            draw_indicator(page, element)
        element.hover()
    except Exception:
        LogError.logger.exception("Hover failed")
        exit()
    LogClicker.logger.info(f"Hovered at position {x, y}")


def click_and_hold(page, indication, restricted_page):
    element, x, y = get_element_and_coordinate(page)
    initial_url = page.url
    try:
        if indication:
            draw_indicator(page, element)
        page.mouse.move(x, y)
        page.mouse.down()
        time.sleep(0.7)
        page.mouse.up()
        time.sleep(1)
        page.wait_for_load_state("load")
        if restricted_page:
            blocking_movement(page, initial_url)
    except Exception:
        LogError.logger.exception("Click and hold failed")
        exit()
    LogClicker.logger.info(f"Clicked and held at position {x, y}")
