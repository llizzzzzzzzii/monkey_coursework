import pytest
from playwright.sync_api import sync_playwright
from monkey import Monkey


@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


def test_sign(browser):
    context = browser.new_context(has_touch=True)
    page = context.new_page()
    monkey = Monkey(url="https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0",
                    page=page, count=5, species=['toucher'], delay=2, indication=True,
                    ignore_errors=True, restricted_page=False)
    monkey.run()
    page.close()
