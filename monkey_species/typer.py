import random
import time
import string
from monkey_logging.monkey_logger import LogTyper
from monkey_logging.monkey_logger import LogError

def get_random_string():
    length = random.randint(1, 255)
    random_string = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
    return random_string

def blocking_movement(page, initial_url):
    current_url = page.url
    if current_url != initial_url:
        page.goto(initial_url)


def find_locators(page):
    page.wait_for_load_state("networkidle")
    input_elements = page.query_selector_all('input, textarea, div[contenteditable=true]')
    viewport_height = page.viewport_size['height']
    visible_input_elements = [element for element in input_elements if
                              element.is_visible() and element.bounding_box()['y'] >= 0 and
                              element.bounding_box()['y'] <= viewport_height and
                              element.get_attribute("type") not in ["radio", "checkbox", "submit", "button", "file"]
                              and element.get_attribute('type') != 'url']
    return visible_input_elements


def send_text(page, indication, restricted_page):
    page.wait_for_load_state("networkidle")
    random_text = get_random_string()
    random_input_element = random.choice(find_locators(page))
    x, y = int(random_input_element.bounding_box()["x"]), int(random_input_element.bounding_box()["y"])
    try:
        if random_input_element:
            if random_input_element.get_attribute("value") is not None and random_input_element.get_attribute(
                    "value") != "":
                random_input_element.fill("")
            page.wait_for_load_state("networkidle")
            if indication is True:
                page.evaluate(
                    """(element) => {
                           element.style.backgroundColor = "rgba(255,0,0,0.7)";
                       }""",
                    random_input_element,
                )
                time.sleep(0.5)
                page.evaluate(
                    """(element) => {
                           element.style.backgroundColor = "transparent";
                       }""",
                    random_input_element,
                )
            random_input_element.fill(random_text)
    except Exception:
        LogError.logger.exception("Typed text failed")
        exit()
    LogTyper.logger.info(f"Typed {random_text} into a text element at position {x, y}")


def send_keys(page, indication, restricted_page):
    initial_url = page.url
    page.wait_for_load_state("networkidle")
    random_input_element = random.choice(find_locators(page))
    x, y = int(random_input_element.bounding_box()["x"]), int(random_input_element.bounding_box()["y"])
    input_type = ['Enter']
    # input_type = ['Shift', 'Backspace', 'Control', 'Escape', 'Alt', 'Delete', 'Enter']
    random_input_type = random.choice(input_type)
    try:
        if random_input_element:
            page.wait_for_load_state("networkidle")
            if indication is True:
                page.evaluate(
                    """(element) => {
                           element.style.backgroundColor = "rgba(255,0,0,0.7)";
                       }""",
                    random_input_element,
                )
                time.sleep(0.5)
                page.evaluate(
                    """(element) => {
                           element.style.backgroundColor = "transparent";
                       }""",
                    random_input_element,
                )
            random_input_element.press(random_input_type)
            if restricted_page:
                blocking_movement(page, initial_url)
    except Exception:
        LogError.logger.exception("Sent key failed")
        exit()
    LogTyper.logger.info(f"Sent {random_input_type} key to a text element at position {x, y}")


def get_random_action():
    rand_action = ['text', 'keys']
    return random.choice(rand_action)
