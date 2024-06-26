from playwright.sync_api import sync_playwright
from locators.clicker_toucher_locators import find_locators
import pytest
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


def test_find_locators(browser_page):
    browser_page.goto("https://alfabank.ru/financial/")
    visible_clickable_elements = find_locators(browser_page)
    assert len(visible_clickable_elements) > 0
    for element in visible_clickable_elements:
        assert browser_page.query_selector(element).bounding_box()['y'] >= 0
        assert browser_page.query_selector(element).bounding_box()['y'] <= browser_page.viewport_size['height']
        assert browser_page.query_selector(element).get_attribute('type') != 'url'


