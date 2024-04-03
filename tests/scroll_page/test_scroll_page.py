from playwright.sync_api import sync_playwright
import pytest
from monkey_species.scroller.scroller import scroll_to_random_position


@pytest.fixture
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()


@pytest.mark.parametrize("width, height", [(1000, 500), (500, 1000)])
def test_scroll_page(browser_page, width, height):
    browser_page.set_viewport_size({"width": width, "height": height})
    scroll_to_random_position(browser_page)

    scroll_x, scroll_y = browser_page.evaluate("() => [window.scrollX, window.scrollY]")

    assert 0 <= scroll_x <= width
    assert 0 <= scroll_y <= height