from monkey_logging.monkey_logger import LogToucher
from monkey_logging.monkey_logger import LogError
from playwright._impl._errors import TimeoutError as PlaywrightTimeoutError
import random
from matplotlib.colors import to_rgba
import time


def blocking_movement(page, initial_url):
    current_url = page.url
    if current_url != initial_url:
        page.goto(initial_url)


def is_element_visible(page, element):
    if not (element.is_visible() and
            element.get_attribute('type') != 'url' and
            0 <= element.bounding_box()['y'] <= page.viewport_size['height']):
        return False
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


def find_locators(page):
    page.wait_for_load_state("load")
    clickable_elements = page.query_selector_all('button, a, input, img, [role="button"], [class="button"]')
    visible_clickable_elements = [element for element in clickable_elements if is_element_visible(page, element)]
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
        setTimeout(() => indicator.remove(), 700);
    """)
    time.sleep(0.7)


def touch(page, indication, restricted_page, color):
    try:
        page.wait_for_load_state("load")
        time.sleep(0.5)
        initial_url = page.url
        visible_elements = find_locators(page)
        if not visible_elements:
            LogToucher.logger.warning("Warning: The element was not found")
        element = random.choice(visible_elements)
        tag_name = page.evaluate("(element) => element.tagName.toLowerCase()", element)
        box = element.bounding_box()
        x = int(box['x'])
        y = int(box['y'])
        if indication:
            draw_indicator(page, x, y, color)
        with page.expect_navigation():
            page.touchscreen.tap(x, y)
        if tag_name == 'img':
            page.keyboard.press("Escape")
        if restricted_page:
            blocking_movement(page, initial_url)
        LogToucher.logger.info(f"Tapped on an element at position {x, y}")
    except PlaywrightTimeoutError:
        LogToucher.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogToucher.logger.error("Error: Touch failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
