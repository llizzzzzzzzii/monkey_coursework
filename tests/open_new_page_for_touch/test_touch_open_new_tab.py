import pytest
from playwright.sync_api import sync_playwright
from monkey_species.toucher.toucher_handler import open_new_tab
from monkey_logging.monkey_logger import LogMonkey
from monkey_logging.monkey_logger import LogError


@pytest.fixture
def browser_page():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            yield browser
            browser.close()
    except Exception as e:
        LogMonkey.logger.error("Error: Loading browser")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)


def test_touch_without_change(browser_page):
    context = browser_page.new_context(has_touch=True)
    page = context.new_page()
    page.goto(
        "https://cashpo-design.ru/news/kak-ukhazhivat-za-orkhideei-v-domashnikh-usloviyakh")
    new_page = open_new_tab(page, 856, 97)
    assert new_page != page
