from playwright.sync_api import sync_playwright
import pytest
from monkey_species.reloader.reloader import reload_page
@pytest.fixture
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        yield page
        browser.close()

def test_reload_page(browser_page):
    browser_page.goto("https://www.wikipedia.org/")
    reload_page(browser_page)
    assert browser_page.url == "https://www.wikipedia.org/"