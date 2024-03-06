import random
import time
from logi.loger import LogTyper

def find_locators(page):
    input_elements = page.query_selector_all('input, textarea, [contenteditable=true]')
    visible_input_elements = [element for element in input_elements if
                              element.is_visible() and element.get_attribute("type") not in ["radio", "checkbox",
                                                                                             "submit", "button"]
                              and element.get_attribute('type') != 'url']
    return visible_input_elements


def send_text(page, indication, delay):
    page.wait_for_load_state("networkidle")
    random_text = ''.join(random.choices('12345678910!@#$%^&*(!"№;%:?*()=+abcdefghijklmnopqrstuvwxyz', k=5))
    random_input_element = random.choice(find_locators(page))
    x, y = random_input_element.bounding_box()["x"], random_input_element.bounding_box()["y"]
    try:
        if random_input_element:
            if random_input_element.get_attribute("value") is not None and random_input_element.get_attribute(
                    "value") != "":
                random_input_element.fill("")
            page.wait_for_load_state("networkidle")
            # random_input_element.fill(random_text)
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
                page.wait_for_load_state("networkidle")
    except Exception:
        LogTyper.logger.exception("Error: Typed text failed")
        exit()
    LogTyper.logger.info(f"Typed {random_text} into a text element at position {x, y}")
    time.sleep(delay / 1000)


def send_keys(page, indication, delay):
    page.wait_for_load_state("networkidle")
    random_input_element = random.choice(find_locators(page))
    x, y = random_input_element.get_attribute("x"), random_input_element.get_attribute("y")
    input_type = ['Shift', 'Backspace', 'Control', 'Escape', 'Alt', 'Delete', 'Enter']
    random_input_type = random.choice(input_type)
    try:
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
            page.wait_for_load_state("networkidle")
    except Exception:
        LogTyper.logger.exception("Error: Sent key failed")
        exit()
    LogTyper.logger.info(f"Sent {random_input_type} key to a text element at position {x, y}")
    time.sleep(delay / 1000)
    time.sleep(delay / 1000)


def get_random_action():
    rand_action = ['text', 'keys']
    return random.choice(rand_action)