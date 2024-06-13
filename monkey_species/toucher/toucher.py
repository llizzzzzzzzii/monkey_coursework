from monkey_logging.monkey_logger import LogToucher
from monkey_logging.monkey_logger import LogError
from playwright._impl._errors import TimeoutError as PlaywrightTimeoutError
from indication.clicker_toucher_indication import draw_indicator
from locators.clicker_toucher_locators import is_image_and_has_target_blank_and_href
from monkey_species.toucher.toucher_handler import get_element_and_coordinate
from monkey_species.toucher.toucher_handler import blocking_movement
from monkey_species.toucher.toucher_handler import actions_with_restriction
from monkey_species.toucher.toucher_handler import actions_unlimited

def touch(page, indication, restricted_page, color, selectors):
    element, x, y = get_element_and_coordinate(page, selectors)
    if not element:
        return page
    try:
        target_blank, has_href, tag_name = is_image_and_has_target_blank_and_href(page, element)
        if indication:
            draw_indicator(page, x, y, color)
        if restricted_page:
            blocking_movement(page, element)
            actions_with_restriction(page, x, y, has_href, tag_name)
        else:
            page = actions_unlimited(page, x, y, target_blank, has_href, tag_name)
        LogToucher.logger.info(f"Tapped on an element at position {x, y}")
    except PlaywrightTimeoutError:
        LogToucher.logger.warning("Warning: The waiting time for the action has been exceeded")
        return page
    except Exception as e:
        LogToucher.logger.error("Error: Touch failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
    return page
