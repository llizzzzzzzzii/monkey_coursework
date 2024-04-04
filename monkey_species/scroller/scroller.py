from monkey_logging.monkey_logger import LogScroller
from monkey_logging.monkey_logger import LogError
import random


def scroll_to_random_position(page, ignore_errors):
    try:
        width = page.evaluate('() => document.body.scrollWidth')
        height = page.evaluate('() => document.body.scrollHeight')

        random_x = random.randint(0, width)
        random_y = random.randint(0, height)

        page.evaluate('window.scrollTo({}, {})'.format(random_x, random_y))
        LogScroller.logger.info(f"Scrolled to position {random_x, random_y}")
    except Exception as e:
        LogScroller.logger.error("Error: Scroll failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
        if not ignore_errors:
            return False
    return True
