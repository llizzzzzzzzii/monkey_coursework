from indicattion.typer_indication import draw_indicator
from monkey_logging.monkey_logger import LogTyper
from monkey_logging.monkey_logger import LogError
from monkey_species.typer.typer_handler import get_random_string
from monkey_species.typer.typer_handler import get_random_number
from monkey_species.typer.typer_handler import get_element_and_coordinate
from monkey_species.typer.typer_handler import blocking_movement
import random


def get_random_action():
    rand_action = [send_text, send_keys]
    return random.choice(rand_action)


def send_text(page, indication, restricted_page, color):
    try:
        page.wait_for_load_state("domcontentloaded")
        random_text = get_random_string()
        random_number = get_random_number()
        element, x, y = get_element_and_coordinate(page)
        if not element:
            return
        input_type = element.get_attribute('type')
        input_mode = element.get_attribute('inputmode')
        if indication is True:
            draw_indicator(page, element, color)
        if (((input_type == 'text') or (input_type is None) or (input_type == 'email') or (input_type == 'password'))
                and (input_mode != 'numeric')):
            element.type(random_text)
            LogTyper.logger.info(f"Typed {random_text} into a text element at position {x, y}")
        else:
            element.type(random_number)
            LogTyper.logger.info(f"Typed {random_number} into a text element at position {x, y}")
    except TimeoutError:
        LogTyper.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogTyper.logger.error("Error: Typed text failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)


def send_keys(page, indication, restricted_page, color):
    try:
        page.wait_for_load_state("domcontentloaded")
        initial_url = page.url
        element, x, y = get_element_and_coordinate(page)
        if not element:
            return
        input_type = ['Shift', 'Backspace', 'Control', 'Escape', 'Alt', 'Delete', 'Enter']
        random_input_type = random.choice(input_type)
        if indication is True:
            draw_indicator(page, element, color)
        element.press(random_input_type)
        if restricted_page:
            blocking_movement(page, initial_url)
        LogTyper.logger.info(f"Sent {random_input_type} key to a text element at position {x, y}")
    except TimeoutError:
        LogTyper.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogTyper.logger.error("Error: Sent key failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
