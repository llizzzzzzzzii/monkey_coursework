import time
import random
from logi.loger import LogClicker

def block_movement(page, element):
    page.evaluate('(element) => { element.addEventListener("click", (e) => { e.preventDefault(); }); }', element)

def find_locators(page):
    clickable_elements = page.query_selector_all('button, a, input, [role="button"]')
    visible_clickable_elements = [element for element in clickable_elements if element.is_visible()]
    return visible_clickable_elements

def draw_indicator(page, x, y):
    script = (f'document.body.insertAdjacentHTML("beforeend", "<div style=\'position: absolute; left: {x}px; '
              f'top: {y}px; width: 10px; height: 10px; background-color: red; border-radius: 50%;\'></div>");')
    page.evaluate(script)
    time.sleep(0.7)
    script_remove = 'document.body.lastChild.remove();'
    page.evaluate(script_remove)

def random_action():
    actions = [hover, click, double_click, multiple_click, click_and_hold]
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

def click(page, indication, restricted_page):
    element, x, y = get_element_and_coordinate(page)
    try:
        if indication:
            draw_indicator(page, x, y)
        if restricted_page:
            block_movement(page, element)
        element.click()
    except Exception:
        LogClicker.logger.exception("Error: Click failed")
        exit()
    LogClicker.logger.info(f"Clicked at position {x, y}")

def double_click(page, indication, restricted_page):
    element, x, y = get_element_and_coordinate(page)
    try:
        if indication:
            draw_indicator(page, x, y)
            draw_indicator(page, x, y)
        if restricted_page:
            block_movement(page, element)
        element.dblclick()
    except Exception:
        LogClicker.logger.exception("Error: Double click failed")
        exit()
    LogClicker.logger.info(f"Clicked at position {x, y} 2 times")

def multiple_click(page, indication, restricted_page):
    element, x, y = get_element_and_coordinate(page)
    count = random.randint(3, 10)
    try:
        for i in range(count):
            if indication:
                draw_indicator(page, x, y)
            if restricted_page:
                block_movement(page, element)
            element.click()
    except Exception:
        LogClicker.logger.exception("Error: Multiple clicks failed")
        exit()
    LogClicker.logger.info(f"Clicked at position {x, y} {count} times")

def hover(page, indication, restricted_page):
    element, x, y = get_element_and_coordinate(page)
    try:
        if indication:
            draw_indicator(page, x, y)
        element.hover()
    except Exception:
        LogClicker.logger.exception("Error: Hover failed")
        exit()
    LogClicker.logger.info(f"Hovered at position {x, y}")

def click_and_hold(page, indication, restricted_page):
    element, x, y = get_element_and_coordinate(page)
    try:
        if indication:
            draw_indicator(page, x, y)
        if restricted_page:
            block_movement(page, element)
        page.mouse.move(x, y)
        page.mouse.down()
        time.sleep(0.7)
        page.mouse.up()
    except Exception:
        LogClicker.logger.exception("Error: Click and hold failed")
        exit()
    LogClicker.logger.info(f"Clicked and held at position {x, y}")
