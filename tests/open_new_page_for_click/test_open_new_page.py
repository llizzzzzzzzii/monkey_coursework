from playwright.sync_api import sync_playwright
import pytest
from monkey_logging.monkey_logger import LogMonkey
from monkey_logging.monkey_logger import LogError
from monkey_species.clicker.click_handler import open_new_tab
import time


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


def test_open_new_page(browser_page):
    page = browser_page
    page.goto(
        "https://cashpo-design.ru/news/kak-ukhazhivat-za-orkhideei-v-domashnikh-usloviyakh")
    new_page = open_new_tab(page, 856, 97, 1)
    assert new_page != page



