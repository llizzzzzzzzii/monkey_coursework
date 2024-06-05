import random
import time
import string
from matplotlib.colors import to_rgba
from monkey_logging.monkey_logger import LogTyper
from monkey_logging.monkey_logger import LogError


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


def is_element_visible(page, element):
    if not (element.is_visible() and
            0 <= element.bounding_box()['y'] <= page.viewport_size['height']
            and element.get_attribute("type") not in ["radio", "checkbox", "submit", "button", "file",
                                                      "reset", 'color', 'range']
            and element.get_attribute('type') != 'url'
            and element.get_attribute('aria-disabled') != 'true'
            and element.get_attribute('aria-readonly') != 'true'):
        return False
    return page.evaluate("""
        (element) => {
            const style = window.getComputedStyle(element);
            if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0' ||
                element.offsetWidth === 0 || element.offsetHeight === 0) {
                return false;
            }

            const rect = element.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            const topElement = document.elementFromPoint(centerX, centerY);

            return element === topElement || element.contains(topElement);
        }
    """, element)


def find_locators(page):
    page.wait_for_load_state("networkidle")
    input_elements = page.query_selector_all('input:not([readonly]):not([disabled]), textarea:not([disabled]), '
                                             'div[contenteditable=true]:not([disabled]),'
                                             '[role="textbox"]:not([disabled])')
    visible_input_elements = [element for element in input_elements if is_element_visible(page, element)]
    return visible_input_elements


def draw_indicator(page, element, color):
    rgba_color = to_rgba(color, alpha=0.7)
    rgba_str = f"rgba({int(rgba_color[0] * 255)},{int(rgba_color[1] * 255)},{int(rgba_color[2] * 255)},{rgba_color[3]})"
    page.evaluate(
        f"""(element) => {{
                element.style.backgroundColor = '{rgba_str}';
                element.style.zIndex = '2147483647';
                element.style.position = 'relative';  // Ensures zIndex is respected
            }}""",
        element
    )
    time.sleep(0.5)
    page.evaluate(
        """(element) => {
            element.style.backgroundColor = '';
            element.style.zIndex = '';
            element.style.position = '';
        }""",
        element
    )


def send_text(page, indication, restricted_page, color):
    try:
        page.wait_for_load_state("load")
        random_text = get_random_string()
        random_number = get_random_number()
        visible_elements = find_locators(page)
        if not visible_elements:
            LogTyper.logger.warning("Warning: The element was not found")
            return
        random_input_element = random.choice(visible_elements)
        input_type = random_input_element.get_attribute('type')
        input_mode = random_input_element.get_attribute('inputmode')
        x, y = int(random_input_element.bounding_box()["x"]), int(random_input_element.bounding_box()["y"])
        page.wait_for_load_state("networkidle")
        if indication is True:
            draw_indicator(page, random_input_element, color)
        if ((input_type == 'text') or (input_type is None) or (input_type == 'email') or (input_type == 'password')) and (input_mode!='numeric'):
            random_input_element.type(random_text)
            LogTyper.logger.info(f"Typed {random_text} into a text element at position {x, y}")
        else:
            random_input_element.type(random_number)
            LogTyper.logger.info(f"Typed {random_number} into a text element at position {x, y}")
    except TimeoutError:
        LogTyper.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogTyper.logger.error("Error: Typed text failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)


def send_keys(page, indication, restricted_page, color):
    try:
        initial_url = page.url
        page.wait_for_load_state("load")
        visible_elements = find_locators(page)
        if not visible_elements:
            LogTyper.logger.warning("Warning: The element was not found")
            return
        random_input_element = random.choice(visible_elements)
        x, y = int(random_input_element.bounding_box()["x"]), int(random_input_element.bounding_box()["y"])
        input_type = ['Shift', 'Backspace', 'Control', 'Escape', 'Alt', 'Delete', 'Enter']
        random_input_type = random.choice(input_type)
        page.wait_for_load_state("networkidle")
        if indication is True:
            draw_indicator(page, random_input_element, color)
        random_input_element.press(random_input_type)
        if restricted_page:
            blocking_movement(page, initial_url)
        LogTyper.logger.info(f"Sent {random_input_type} key to a text element at position {x, y}")
    except TimeoutError:
        LogTyper.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogTyper.logger.error("Error: Sent key failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)


def get_random_action():
    rand_action = ['text', 'keys']
    return random.choice(rand_action)
