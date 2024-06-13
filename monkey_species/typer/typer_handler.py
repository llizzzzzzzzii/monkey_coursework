from locators.typer_locators import find_locators
from monkey_logging.monkey_logger import LogTyper
import string
import random


def get_random_string():
    length = random.randint(1, 255)
    random_string = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
    return random_string


def get_random_number():
    length = random.randint(1, 255)
    random_string = ''.join(random.choices(string.digits, k=length))
    return random_string


def blocking_movement(page, element):
    page.evaluate("""
        (element) => {
            element.addEventListener('click', (event) => {
                event.preventDefault();
            });
        }
    """, element)


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
            x, y = int(element.bounding_box()["x"]), int(element.bounding_box()["y"])
            return element, x, y
        else:
            selectors.remove(selector)
    LogTyper.logger.warning("Warning: The element was not found")
    return None, -1, -1
