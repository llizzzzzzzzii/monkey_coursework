import random
import time


def find_locators(page):
    input_elements = page.query_selector_all('input, textarea, [contenteditable=true]')
    visible_input_elements = [element for element in input_elements if
                              element.is_visible() and element.get_attribute("type") not in ["radio", "checkbox"]]
    return visible_input_elements


def send_text(page, indication):
    random_text = ''.join(random.choices('12345678910!@#$%^&*(!"№;%:?*()=+abcdefghijklmnopqrstuvwxyz', k=5))
    random_input_element = random.choice(find_locators(page))
    if random_input_element:
        if random_input_element.get_attribute("value") is not None and random_input_element.get_attribute(
                "value") != "":
            random_input_element.fill("")
        random_input_element.fill(random_text)
        if indication is True:
            page.evaluate(
                """(element) => {
                       element.style.backgroundColor = "rgba(255,0,0,0.7)";
                   }""",
                random_input_element,
            )
            time.sleep(1)
            page.evaluate(
                """(element) => {
                       element.style.backgroundColor = "transparent";
                   }""",
                random_input_element,
            )


def send_keys(page, indication):
    random_input_element = random.choice(find_locators(page))
    input_type = ['Shift', 'Backspace', 'Control', 'Escape', 'Alt', 'Delete', 'Enter']
    random_input_type = random.choice(input_type)
    random_input_element.press(random_input_type)
    if indication is True:
        page.evaluate(
            """(element) => {
                   element.style.backgroundColor = "rgba(255,0,0,0.7)";
               }""",
            random_input_element,
        )
        time.sleep(1)
        page.evaluate(
            """(element) => {
                   element.style.backgroundColor = "transparent";
               }""",
            random_input_element,
        )


def get_random_action():
    rand_action = ['text', 'keys']
    return random.choice(rand_action)
