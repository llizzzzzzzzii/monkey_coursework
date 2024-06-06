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


def blocking_movement(page, initial_url):
    current_url = page.url
    if current_url != initial_url:
        page.goto(initial_url)


def get_element_and_coordinate(page):
    visible_elements = find_locators(page)
    if not visible_elements:
        LogTyper.logger.warning("Warning: The element was not found")
        return [], -1, -1
    element = random.choice(visible_elements)
    x, y = int(element.bounding_box()["x"]), int(element.bounding_box()["y"])
    return element, x, y
