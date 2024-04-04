from monkey_logging.monkey_logger import LogScroller
from monkey_logging.monkey_logger import LogError
import random


def scroll_to_random_position(page):
    try:
        width = page.evaluate('() => document.body.scrollWidth')
        height = page.evaluate('() => document.body.scrollHeight')

        random_x = random.randint(0, width)
        random_y = random.randint(0, height)

        page.evaluate('window.scrollTo({}, {})'.format(random_x, random_y))
        LogScroller.logger.info(f"Scrolled to position {random_x, random_y}")
    except Exception:
        LogError.logger.error("Scroll failed")

