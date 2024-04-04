from monkey_logging.monkey_logger import LogToucher
from monkey_logging.monkey_logger import LogError
import random

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

def draw_indicator(page, x, y):
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


def touch(page, indication, restricted_page):
    try:
        page.wait_for_load_state("load")
        initial_url = page.url
        visible_elements = find_locators(page)
        element = random.choice(visible_elements)
        box = element.bounding_box()
        x = int(box['x'] + box['width'] / 2)
        y = int(box['y'] + box['height'] / 2)
        if indication:
            draw_indicator(page, x, y)
        element.tap()
        if restricted_page:
            blocking_movement(page, initial_url)
        LogToucher.logger.info(f"Tapped on an element at position {x, y}")
    except Exception:
        LogError.logger.error("Touch failed")
