from playwright.sync_api import sync_playwright
import pytest
from monkey_logging.monkey_logger import LogMonkey
from monkey_logging.monkey_logger import LogError
from locators.clicker_toucher_locators import is_image_and_has_target_blank_and_href


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
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    element = page.locator(('img[alt="Mir"][src="userfiles/image/mir-min.png"].var')).element_handle()
    assert is_image_and_has_target_blank_and_href(page, element) == (False, False, 'img')


def test_element_has_href(browser_page):
    page = browser_page
    page.goto(
        "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
    element = page.locator(
        'a[href="/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0"][title="Перейти на заглавную страницу [alt-shift-z]"][accesskey="z"]').element_handle()
    assert is_image_and_has_target_blank_and_href(page, element) == (False, True, 'a')


def test_image_has_target(browser_page):
    page = browser_page
    page.goto(
        "https://alfabank.ru/alfastudents/")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    element = page.locator(
        'img.aDNQV.gDNQV[height="24"][width="24"][loading="lazy"][src="https://alfabank.servicecdn.ru/site-upload/ad/cd/7467/Alfabank_icon_24px.png"]').element_handle()
    assert is_image_and_has_target_blank_and_href(page, element) == (True, True, 'img')
