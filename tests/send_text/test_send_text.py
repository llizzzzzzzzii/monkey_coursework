from playwright.sync_api import sync_playwright
import pytest
from monkey_species.typer.typer import send_text


@pytest.fixture
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        yield page
        browser.close()


def test_send_text(browser_page):
    browser_page.goto("https://account.mail.ru/signup")
    indication = True
    restricted_page = False
    send_text(browser_page, indication, restricted_page)
    input_value = browser_page.evaluate('''() => {
            return document.querySelector('input').value;
        }''')
    assert input_value is not None
