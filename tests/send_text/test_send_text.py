from playwright.sync_api import sync_playwright
import pytest
from monkey_species.typer.typer import send_text
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

def test_send_text(browser_page):
    browser_page.goto("https://account.mail.ru/signup")
    indication = True
    restricted_page = False
    ignore_errors = True
    color = 'blue'
    send_text(browser_page, indication, restricted_page,ignore_errors, color)
    input_value = browser_page.evaluate('''() => {
            return document.querySelector('input').value;
        }''')
    assert input_value is not None
