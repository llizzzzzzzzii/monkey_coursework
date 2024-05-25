import time
import random
from monkey_logging.monkey_logger import LogClicker
from monkey_logging.monkey_logger import LogError
from matplotlib.colors import to_rgba


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


def draw_indicator(page, element, color):
    rgba_color = to_rgba(color, alpha=0.7)
    rgba_str = f"rgba({int(rgba_color[0] * 255)},{int(rgba_color[1] * 255)},{int(rgba_color[2] * 255)},{rgba_color[3]})"
    box = element.bounding_box()
    x = box['x'] + box['width'] / 2
    y = box['y'] + box['height'] / 2
    page.evaluate(f'''
      circle = document.createElement('div');
      circle.style.width = '15px';
      circle.style.height = '15px';
      circle.style.borderRadius = '50%';
      circle.style.backgroundColor = '{rgba_str}';
      circle.style.position = 'absolute';
      circle.style.left = '{x}px';
      circle.style.top = '{y}px';
      circle.style.zIndex = '10000';
      circle.style.pointerEvents = 'none';
      document.body.appendChild(circle);
      setTimeout(() => circle.remove(), 1000);
    ''')


def random_action():
    actions = [hover, click, double_click, multiple_click, click_and_hold]
    get_random = random.choice(actions)
    return get_random


def get_element_and_coordinate(page):
    page.wait_for_load_state("load")
    visible_elements = find_locators(page)
    if not visible_elements:
        LogClicker.logger.warning("Warning: The element was not found")
        return [], 0, 0
    element = random.choice(visible_elements)
    x, y = int(element.bounding_box()["x"]), int(element.bounding_box()["y"])
    return element, x, y


def click(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    if not element:
        return
    initial_url = page.url
    try:
        if indication:
            draw_indicator(page, element, color)
        page.mouse.click(x, y)
        if restricted_page:
            blocking_movement(page, initial_url)
        LogClicker.logger.info(f"Clicked at position {x, y}")
    except TimeoutError as e:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogClicker.logger.error("Error: Click failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)


def double_click(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    if not element:
        return
    initial_url = page.url
    try:
        if indication:
            draw_indicator(page, element, color)
            draw_indicator(page, element, color)
        page.mouse.dblclick(x, y)
        if restricted_page:
            blocking_movement(page, initial_url)
        LogClicker.logger.info(f"Clicked at position {x, y} 2 times")
    except TimeoutError as e:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogClicker.logger.error("Double click failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)


def multiple_click(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    if not element:
        return
    count = random.randint(3, 10)
    initial_url = page.url
    try:
        for i in range(count):
            if indication:
                draw_indicator(page, element, color)
                time.sleep(1)
        page.mouse.click(x, y, click_count=count)
        if restricted_page:
            blocking_movement(page, initial_url)
        LogClicker.logger.info(f"Clicked at position {x, y} {count} times")
        page.wait_for_load_state("load")
    except TimeoutError as e:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogClicker.logger.error("Multiple clicks failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)


def hover(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    if not element:
        return
    try:
        if indication:
            draw_indicator(page, element, color)
        page.mouse.move(x, y)
        LogClicker.logger.info(f"Hovered at position {x, y}")
    except TimeoutError as e:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogClicker.logger.error("Hover failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)

def click_and_hold(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    if not element:
        return
    initial_url = page.url
    try:
        if indication:
            draw_indicator(page, element, color)
        page.mouse.click(x, y, delay=3000)
        if restricted_page:
            blocking_movement(page, initial_url)
        LogClicker.logger.info(f"Clicked and held at position {x, y}")
    except TimeoutError as e:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogClicker.logger.error("Click and hold failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
