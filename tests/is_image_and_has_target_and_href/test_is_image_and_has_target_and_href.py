from playwright.sync_api import sync_playwright
import pytest
from monkey_logging.monkey_logger import LogMonkey
from monkey_logging.monkey_logger import LogError
from monkey_species.clicker.clicker import is_image_and_has_target_blank_and_href


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


def test_image_has_href(browser_page):
    page = browser_page
    page.goto('https://alfabank.ru/financial/')
    index = 0
    element = page.locator(
        'img[alt="иконка карточки"].a2lPS.e2lPS[loading="lazy"][height="40"][src="https://alfabank.servicecdn.ru/media/main-page-assets/main-page_selfemployed-icon.svg"][width="40"]').nth(
        index).element_handle()
    assert is_image_and_has_target_blank_and_href(page, element) == (False, True, 'img')


def test_image_has_not_href(browser_page):
    page = browser_page
    page.goto('https://cashpo-design.ru/news/kak-ukhazhivat-za-orkhideei-v-domashnikh-usloviyakh')
    element = page.locator(
        'img[src="userfiles/новости/orkhidei-2.jpg"][alt="Орхидеи в горшках в интерьере"].js-qazy-loaded').element_handle()
    print(element)
    assert is_image_and_has_target_blank_and_href(page, element) == (False, False, 'img')
