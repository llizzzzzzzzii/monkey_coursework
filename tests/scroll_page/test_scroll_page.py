from playwright.sync_api import sync_playwright
import pytest
from monkey_species.scroller.scroller import scroll_to_random_position
from monkey_logging.monkey_logger import LogMonkey
from monkey_logging.monkey_logger import LogError


@pytest.fixture
def browser_page():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            yield page
            browser.close()
    except Exception as e:
        LogMonkey.logger.error("Error: Loading browser")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)


@pytest.mark.parametrize("width, height", [(1000, 500), (500, 1000)])
def test_scroll_page(browser_page, width, height):
    ignore_errors=True
    browser_page.set_viewport_size({"width": width, "height": height})
    scroll_to_random_position(browser_page,ignore_errors)

    scroll_x, scroll_y = browser_page.evaluate("() => [window.scrollX, window.scrollY]")

    assert 0 <= scroll_x <= width
    assert 0 <= scroll_y <= height