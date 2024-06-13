import pytest
from playwright.sync_api import sync_playwright
from monkey import Monkey


@pytest.fixture
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(has_touch=True)
        page = context.new_page()
        yield page
        browser.close()


def test_sign(browser):
    page = browser
    monkey = Monkey(url="https://account.mail.ru/signup",
        page=page, count=1, species=['typer'], delay=0, indication=True,
        ignore_errors=True, restricted_page=True, color='red')
    monkey.run()
    page.close()
