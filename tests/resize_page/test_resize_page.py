from playwright.sync_api import sync_playwright
import pytest
from monkey_species.resizer.resizer import resize_page
from monkey_logging.monkey_logger import LogMonkey
from monkey_logging.monkey_logger import LogError


@pytest.fixture
def browser_page():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            yield page
            browser.close()
    except Exception as e:
        LogMonkey.logger.error("Error: Loading browser")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)

def test_resize_page(browser_page):
    color = 'blue'
    initial_viewport = browser_page.viewport_size
    resize_page(browser_page, color)
    assert browser_page.viewport_size != initial_viewport