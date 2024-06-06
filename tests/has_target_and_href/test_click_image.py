from playwright.sync_api import sync_playwright
import pytest
from monkey_logging.monkey_logger import LogMonkey
from monkey_logging.monkey_logger import LogError
from monkey_species.clicker.clicker import has_target_blank_and_href


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


def test_has_href(browser_page):
    page = browser_page
    page.goto(
        "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
    selector = 'a[href="/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0"][title="Перейти на заглавную страницу [alt-shift-z]"][accesskey="z"]'
    element = page.locator(selector).element_handle()
    assert has_target_blank_and_href(page, element) == (False, True)


def test_has_target(browser_page):
    page = browser_page
    page.goto('http://devtoolschallenger.com/')
    selector = 'a.download.non-ff[href="https://www.mozilla.org/firefox/developer/"][target="_blank"]:text("Get yours today »")'
    element = page.locator(selector).element_handle()
    assert has_target_blank_and_href(page, element) == (True, True)


def test_has_not_target_and_href(browser_page):
    page = browser_page
    page.goto('https://testpages.eviltester.com/styled/html5-form-test.html')
    selector = 'input.styled-click-button[type="reset"]'
    element = page.locator(selector).element_handle()
    assert has_target_blank_and_href(page, element) == (False, False)
