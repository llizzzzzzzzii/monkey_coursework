from playwright.sync_api import sync_playwright
import pytest
from monkey_logging.monkey_logger import LogMonkey
from monkey_logging.monkey_logger import LogError
from monkey_species.clicker.clicker import open_new_tab
import time

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


def test_open_new_page(browser_page):
    page = browser_page
    page.goto(
        "https://alfabank.ru/alfastudents/")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    new_page = open_new_tab(page, 904, 453, False, 1)
    assert new_page != page


