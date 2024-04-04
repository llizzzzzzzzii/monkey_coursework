from playwright.sync_api import sync_playwright
import pytest
from monkey_species.reloader.reloader import reload_page
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


def test_reload_page(browser_page):
    browser_page.goto("https://www.wikipedia.org/")
    ignore_errors = True
    reload_page(browser_page,ignore_errors)
    assert browser_page.url == "https://www.wikipedia.org/"