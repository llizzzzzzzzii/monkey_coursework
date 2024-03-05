import random
import time


def send_keys_to_random_element(page, indication, delay):
    input_elements = page.query_selector_all('input, textarea, [contenteditable=true]')
    visible_input_elements = [element for element in input_elements if
                              element.is_visible() and element.get_attribute("type") not in ["radio", "checkbox"]]
    random_text = ''.join(random.choices('12345678910!@#$%^&*(!"№;%:?*()=+abcdefghijklmnopqrstuvwxyz', k=5))
    input_type = ['text', 'Shift', 'Backspace', 'Control', 'Escape', 'Alt', 'Delete', 'Enter']
    random_input_type = random.choice(input_type)
    random_input_element = random.choice(visible_input_elements)
    if visible_input_elements:
        if random_input_type == 'text':
            if random_input_element.get_attribute("value") is not None and random_input_element.get_attribute(
                    "value") != "":
                random_input_element.fill("")
            random_input_element.fill(random_text)
            if indication == True:
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
        else:
            random_input_element.press(random_input_type)
            if indication == True:
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
        time.sleep(delay)
