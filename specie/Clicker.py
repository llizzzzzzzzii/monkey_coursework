import time
import random
from logi.loger import LogClicker
from logi.loger import LogError

def find_locators(page):
    clickable_elements = page.query_selector_all('button, a, input, [role="button"]')
    viewport_height = page.viewport_size['height']
    visible_clickable_elements = [element for element in clickable_elements if element.is_visible() and
                        element.bounding_box()['y'] >= 0 and element.bounding_box()['y'] <= viewport_height]
    return visible_clickable_elements

def draw_indicator(page, x, y):
    script = (f'document.body.insertAdjacentHTML("beforeend", "<div style=\'position: absolute; left: {x}px; '
              f'top: {y}px; width: 15px; height: 15px; background-color: red; border-radius: 7.5px; opacity: 0.7;\'></div>");')
    page.evaluate(script)
    time.sleep(0.7)
    script_remove = 'document.body.lastChild.remove();'
    page.evaluate(script_remove)

def random_action():
    actions = [hover, click, double_click, click_and_hold]
    get_random = random.choice(actions)
    return get_random

def get_element_and_coordinate(page):
    visible_elements = find_locators(page)
    element = random.choice(visible_elements)
    x, y = element.bounding_box()["x"], element.bounding_box()["y"]
    height, width = element.bounding_box()["height"], element.bounding_box()["width"]
    x = int(x + width / 2)
    y = int(y + height / 2)
    return element, x, y

def click(page, indication):
    element, x, y = get_element_and_coordinate(page)
    try:
        if indication:
            draw_indicator(page, x, y)
        element.click()
    except Exception:
        LogError.logger.exception("Click failed")
        exit()
    LogClicker.logger.info(f"Clicked at position {x, y}")

def double_click(page, indication):
    element, x, y = get_element_and_coordinate(page)
    try:
        if indication:
            draw_indicator(page, x, y)
            draw_indicator(page, x, y)
        element.dblclick()
    except Exception:
        LogError.logger.exception("Double click failed")
        exit()
    LogClicker.logger.info(f"Clicked at position {x, y} 2 times")

def multiple_click(page, indication):
    element, x, y = get_element_and_coordinate(page)
    count = random.randint(3, 10)
    try:
        for i in range(count):
            if indication:
                draw_indicator(page, x, y)
            element.click()
    except Exception:
        LogError.logger.exception("Multiple clicks failed")
        exit()
    LogClicker.logger.info(f"Clicked at position {x, y} {count} times")

def hover(page, indication):
    element, x, y = get_element_and_coordinate(page)
    try:
        if indication:
            draw_indicator(page, x, y)
        element.hover()
    except Exception:
        LogError.logger.exception("Hover failed")
        exit()
    LogClicker.logger.info(f"Hovered at position {x, y}")

def click_and_hold(page, indication):
    element, x, y = get_element_and_coordinate(page)
    try:
        if indication:
            draw_indicator(page, x, y)
        page.mouse.move(x, y)
        page.mouse.down()
        time.sleep(0.7)
        page.mouse.up()
    except Exception:
        LogError.logger.exception("Click and hold failed")
        exit()
    LogClicker.logger.info(f"Clicked and held at position {x, y}")
