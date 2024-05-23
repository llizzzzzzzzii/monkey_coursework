from monkey_logging.monkey_logger import LogToucher
from monkey_logging.monkey_logger import LogError
import random
from matplotlib.colors import to_rgba
import time


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

def draw_indicator(page, x, y, color):
    rgba_color = to_rgba(color, alpha=0.7)
    rgba_str = f"rgba({int(rgba_color[0] * 255)},{int(rgba_color[1] * 255)},{int(rgba_color[2] * 255)},{rgba_color[3]})"
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


def touch(page, indication, restricted_page, ignore_errors,color):
    try:
        page.wait_for_load_state("load")
        time.sleep(0.5)
        initial_url = page.url
        visible_elements = find_locators(page)
        element = random.choice(visible_elements)
        box = element.bounding_box()
        x = box['x']
        y = box['y']
        if indication:
            draw_indicator(page, x, y,color)
        page.touchscreen.tap(x, y)
        if restricted_page:
            blocking_movement(page, initial_url)
        LogToucher.logger.info(f"Tapped on an element at position {x, y}")
    except Exception as e:
        LogToucher.logger.error("Error: Touch failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
        if not ignore_errors:
            return False
    return True
