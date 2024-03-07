import random
import time
from logi.loger import LogTyper
from logi.loger import LogError


def blocking_movement(page, element):
    page.evaluate(
        '(element) => { element.addEventListener("keydown", (e) => { if (!element.classList.contains("no-enter") && '
        'e.key === "Enter") { e.preventDefault(); e.stopPropagation(); } }); }',
        element)


def find_locators(page):
    input_elements = page.query_selector_all('input, textarea, div[contenteditable=true]')
    viewport_height = page.viewport_size['height']
    visible_input_elements = [element for element in input_elements if
                              element.is_visible() and element.bounding_box()['y'] >= 0 and
                              element.bounding_box()['y'] <= viewport_height and
                              element.get_attribute("type") not in ["radio", "checkbox", "submit", "button"]]
    return visible_input_elements


def send_text(page, indication, restricted_page):
    page.wait_for_load_state("networkidle")
    random_text = ''.join(random.choices('12345678910!@#$%^&*(!"№;%:?*()=+abcdefghijklmnopqrstuvwxyz', k=5))
    random_input_element = random.choice(find_locators(page))
    x, y = int(random_input_element.bounding_box()["x"]), int(random_input_element.bounding_box()["y"])
    try:
        if random_input_element:
            if random_input_element.get_attribute("value") is not None and random_input_element.get_attribute(
                    "value") != "":
                random_input_element.fill("")
            page.wait_for_load_state("networkidle")
            if restricted_page:
                blocking_movement(page, random_input_element)
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
    page.wait_for_load_state("networkidle")
    random_input_element = random.choice(find_locators(page))
    x, y = int(random_input_element.bounding_box()["x"]), int(random_input_element.bounding_box()["y"])
    input_type = ['Shift', 'Backspace', 'Control', 'Escape', 'Alt', 'Delete', 'Enter']
    random_input_type = random.choice(input_type)
    try:
        if random_input_element:
            if restricted_page:
                if random_input_element.get_attribute("value") is not None and random_input_element.get_attribute(
                        "value") != "":
                    random_input_element.fill("")

                blocking_movement(page, random_input_element)

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
    except Exception:
        LogError.logger.exception("Sent key failed")
        exit()
    LogTyper.logger.info(f"Sent {random_input_type} key to a text element at position {x, y}")


def get_random_action():
    rand_action = ['text', 'keys']
    return random.choice(rand_action)
