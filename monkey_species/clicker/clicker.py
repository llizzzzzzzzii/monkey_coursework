from monkey_logging.monkey_logger import LogClicker
from monkey_logging.monkey_logger import LogError
from monkey_species.clicker.click_handler import perform_click_action
import random


def random_action():
    actions = [click, double_click, multiple_click, click_and_hold, hover]
    get_random = random.choice(actions)
    return get_random


def click(page, indication, restricted_page, color, selectors):
    try:
        page, x, y = perform_click_action(page, indication, restricted_page, color, 1, selectors)
        if x == -1 and y == -1:
            return page
        LogClicker.logger.info(f"Clicked at position {x, y}")
    except Exception as e:
        LogClicker.logger.error("Error: Click failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
    return page


def double_click(page, indication, restricted_page, color, selectors):
    try:
        page, x, y = perform_click_action(page, indication, restricted_page, color, 2, selectors)
        if x == -1 and y == -1:
            return page
        LogClicker.logger.info(f"Clicked at position {x, y} 2 times")
    except Exception as e:
        LogClicker.logger.error("Double click failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
    return page


def multiple_click(page, indication, restricted_page, color, selectors):
    try:
        count = random.randint(3, 10)
        page, x, y = perform_click_action(page, indication, restricted_page, color, count, selectors)
        if x == -1 and y == -1:
            return page
        LogClicker.logger.info(f"Clicked at position {x, y} {count} times")
    except Exception as e:
        LogClicker.logger.error("Multiple clicks failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
    return page


def click_and_hold(page, indication, restricted_page, color, selectors):
    try:
        page, x, y = perform_click_action(page, indication, restricted_page, color, -1, selectors)
        if x == -1 and y == -1:
            return page
        LogClicker.logger.info(f"Clicked and held at position {x, y}")
    except Exception as e:
        LogClicker.logger.error("Click and hold failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
    return page


def hover(page, indication, restricted_page, color, selectors):
    try:
        page, x, y = perform_click_action(page, indication, restricted_page, color, 0, selectors)
        if x == -1 and y == -1:
            return page
        LogClicker.logger.info(f"Hovered at position {x, y}")
    except TimeoutError:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
        return page
    except Exception as e:
        LogClicker.logger.error("Hover failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
    return page

