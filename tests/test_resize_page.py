from playwright.sync_api import sync_playwright
import pytest
from specie.resizer import resize_page


@pytest.fixture
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        yield page
        browser.close()


def test_resize_page(browser_page):
    browser_page.goto("https://www.wikipedia.org/")
    initial_window_size = browser_page.viewport_size
    resize_page(browser_page)
    assert browser_page.viewport_size != initial_window_size
