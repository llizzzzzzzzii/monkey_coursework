import time
import random
from monkey_logging.monkey_logger import LogClicker
from monkey_logging.monkey_logger import LogError
from matplotlib.colors import to_rgba
from playwright._impl._errors import TimeoutError as PlaywrightTimeoutError


def blocking_movement(page, initial_url):
    current_url = page.url
    if current_url != initial_url:
        page.goto(initial_url)


def find_locators(page):
    page.wait_for_load_state("load")
    clickable_elements = page.query_selector_all('button, a, input, img, input[role="button"]')
    viewport_height = page.viewport_size['height']
    visible_clickable_elements = [element for element in clickable_elements if is_element_visible(page, element) and
                                  0 <= element.bounding_box()['y'] <= viewport_height]
    # visible_clickable_elements = [element for element in clickable_elements if element.is_visible() and
    #                               0 <= element.bounding_box()['y'] <= viewport_height
    #                               and element.get_attribute('type') != 'url']
    return visible_clickable_elements


def draw_indicator(page, x, y, color):
    rgba_color = to_rgba(color, alpha=0.7)
    rgba_str = f"rgba({int(rgba_color[0] * 255)},{int(rgba_color[1] * 255)},{int(rgba_color[2] * 255)},{rgba_color[3]})"
    radius = 15
    page.evaluate(f"""
        const indicator = document.createElement('div');
        indicator.style.cssText = `
            position: fixed !important;
            background-color: {rgba_str} !important;
            width: {radius}px !important;
            height: {radius}px !important;
            border: 2px solid red !important;
            border-radius: 50% !important;
            left: {x}px !important;
            top: {y}px !important;
            transform: translate(-50%, -50%) !important;
            z-index: 2147483647 !important;
        `;
        document.body.appendChild(indicator);
        setTimeout(() => indicator.remove(), 1000);
    """)


def random_action():
    # actions = [hover, click, double_click, multiple_click, click_and_hold]
    actions = [click]
    get_random = random.choice(actions)
    return get_random


def get_element_and_coordinate(page):
    page.wait_for_load_state("domcontentloaded")
    visible_elements = find_locators(page)
    if not visible_elements:
        LogClicker.logger.warning("Warning: The element was not found")
        return [], 0, 0
    element = random.choice(visible_elements)
    bounding_box = element.bounding_box()
    x, y = int(bounding_box['x'] + bounding_box['width'] / 2), int(bounding_box['y'] + bounding_box['height'] / 2)
    return element, x, y


def is_element_visible(page, element):
    return page.evaluate("""
        (element) => {
            const style = window.getComputedStyle(element);
            if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0' ||
                element.offsetWidth === 0 || element.offsetHeight === 0) {
                return false;
            }

            const rect = element.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            const topElement = document.elementFromPoint(centerX, centerY);

            return element === topElement || element.contains(topElement);
        }
    """, element)


def click(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    tag_name = page.evaluate("(element) => element.tagName.toLowerCase()", element)
    has_href = page.evaluate("(element) => element.hasAttribute('href')", element)
    if not element:
        return
    initial_url = page.url
    try:
        if indication:
            draw_indicator(page, x, y, color)
            time.sleep(1)
        if has_href:
            with page.expect_navigation():
                page.mouse.click(x, y)
        else:
            page.mouse.click(x, y)
        if tag_name == 'img':
            time.sleep(0.1)
            page.keyboard.press("Escape")
        if restricted_page:
            blocking_movement(page, initial_url)
        LogClicker.logger.info(f"Clicked at position {x, y}")
    except PlaywrightTimeoutError:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogClicker.logger.error("Error: Click failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)


def double_click(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    tag_name = page.evaluate("(element) => element.tagName.toLowerCase()", element)
    if not element:
        return
    initial_url = page.url
    try:
        if indication:
            draw_indicator(page, element, color)
            draw_indicator(page, element, color)
        with page.expect_navigation():
            page.mouse.dblclick(x, y)
        if tag_name == 'img':
            time.sleep(0.1)
            page.keyboard.press("Escape")
        if restricted_page:
            blocking_movement(page, initial_url)
        LogClicker.logger.info(f"Clicked at position {x, y} 2 times")
    except PlaywrightTimeoutError:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogClicker.logger.error("Double click failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)


def multiple_click(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    tag_name = page.evaluate("(element) => element.tagName.toLowerCase()", element)
    if not element:
        return
    count = random.randint(3, 10)
    initial_url = page.url
    try:
        for i in range(count):
            if indication:
                draw_indicator(page, element, color)
                time.sleep(1)
        with page.expect_navigation():
            page.mouse.click(x, y, click_count=count)
        if tag_name == 'img':
            time.sleep(0.1)
            page.keyboard.press("Escape")
        if restricted_page:
            blocking_movement(page, initial_url)
        LogClicker.logger.info(f"Clicked at position {x, y} {count} times")
        page.wait_for_load_state("load")
    except PlaywrightTimeoutError:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogClicker.logger.error("Multiple clicks failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)


def hover(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    if not element:
        return
    try:
        if indication:
            draw_indicator(page, element, color)
        page.mouse.move(x, y)
        LogClicker.logger.info(f"Hovered at position {x, y}")
    except TimeoutError:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogClicker.logger.error("Hover failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)


def click_and_hold(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    tag_name = page.evaluate("(element) => element.tagName.toLowerCase()", element)
    if not element:
        return
    initial_url = page.url
    try:
        if indication:
            draw_indicator(page, element, color)
        with page.expect_navigation():
            page.mouse.click(x, y, delay=3000)
        if tag_name == 'img':
            page.keyboard.press("Escape")
        if restricted_page:
            blocking_movement(page, initial_url)
        LogClicker.logger.info(f"Clicked and held at position {x, y}")
    except PlaywrightTimeoutError:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogClicker.logger.error("Click and hold failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)

