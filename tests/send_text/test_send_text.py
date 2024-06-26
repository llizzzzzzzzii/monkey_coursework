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
    browser_page.goto(
        "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
    indication = True
    restricted_page = False
    color = 'blue'
    selector = "input[id='searchInput'][title='Искать в Википедии [alt-shift-f]'][class='vector-search-box-input']"
    element = [selector]
    send_text(browser_page, indication, restricted_page, color, element)
    input_value = browser_page.evaluate('''() => {
            return document.querySelector('input').value;
        }''')
    assert input_value is not None
