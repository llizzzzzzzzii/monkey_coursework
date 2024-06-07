from monkey_logging.monkey_logger import LogToucher
from monkey_logging.monkey_logger import LogError
from playwright._impl._errors import TimeoutError as PlaywrightTimeoutError
from indicattion.clicker_toucher_indication import draw_indicator
from locators.clicker_toucher_locators import is_image_and_has_target_blank_and_href
from monkey_species.toucher.toucher_handler import get_element_and_coordinate
from monkey_species.toucher.toucher_handler import open_new_tab
from monkey_species.toucher.toucher_handler import blocking_movement
import time


def touch(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    if not element:
        return page
    try:
        target_blank, has_href, tag_name = is_image_and_has_target_blank_and_href(page, element)
        initial_url = page.url
        if indication:
            draw_indicator(page, x, y, color)
        if target_blank:
            page = open_new_tab(page, x, y, restricted_page)
        elif has_href:
            with page.expect_navigation():
                page.touchscreen.tap(x, y)
        else:
            page.touchscreen.tap(x, y)
            page.wait_for_load_state('networkidle')
        if tag_name == 'img':
            time.sleep(0.3)
            page.keyboard.press("Escape")
        if restricted_page:
            blocking_movement(page, initial_url)
        LogToucher.logger.info(f"Tapped on an element at position {x, y}")
    except PlaywrightTimeoutError:
        LogToucher.logger.warning("Warning: The waiting time for the action has been exceeded")
        return page
    except Exception as e:
        LogToucher.logger.error("Error: Touch failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
    return page
