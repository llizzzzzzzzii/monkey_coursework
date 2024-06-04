import time
import random
from monkey_logging.monkey_logger import LogClicker
from monkey_logging.monkey_logger import LogError
from matplotlib.colors import to_rgba
from playwright._impl._errors import TimeoutError as PlaywrightTimeoutError


def random_action():
    actions = [hover, click, double_click, multiple_click, click_and_hold]
    get_random = random.choice(actions)
    return get_random


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


def blocking_movement(page, initial_url):
    current_url = page.url
    if current_url != initial_url:
        page.goto(initial_url)


def has_target_blank_and_href(page, element):
    target_blank = page.evaluate("(element) => element.getAttribute('target') === '_blank'", element)
    has_href = page.evaluate("(element) => element.hasAttribute('href')", element)
    return target_blank, has_href

def is_image_and_has_target_blank_and_href(page, element):
    tag_name = page.evaluate("(element) => element.tagName.toLowerCase()", element)
    if tag_name == 'img':
        link_element_handle = page.evaluate_handle("""
                (element) => {
                    while (element.parentElement) {
                        if (element.parentElement.tagName.toLowerCase() === 'a') {
                            return element.parentElement;
                        }
                        element = element.parentElement;
                    }
                    return null;
                }
            """, element)
        if link_element_handle.as_element():
            target_blank, has_href = has_target_blank_and_href(page, link_element_handle)
            return target_blank, has_href, tag_name

    target_blank, has_href = has_target_blank_and_href(page, element)
    return target_blank, has_href, tag_name


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


def open_new_tab(page, x, y, restricted_page, count):
    with page.context.expect_page() as new_page_info:
        if count == 1:
            page.mouse.click(x, y)
        elif count == 2:
            page.mouse.dblclick(x, y)
        else:
            page.mouse.click(x, y, click_count=count)
    if not restricted_page:
        new_page = new_page_info.value
        new_page.bring_to_front()
        return new_page
    return page


def click(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    if not element:
        return page
    target_blank, has_href, tag_name = is_image_and_has_target_blank_and_href(page, element)
    initial_url = page.url
    try:
        if indication:
            draw_indicator(page, x, y, color)
        if target_blank:
            page = open_new_tab(page, x, y, restricted_page, 1)
        elif has_href:
            with page.expect_navigation():
                page.mouse.click(x, y)
        else:
            page.mouse.click(x, y)
            page.wait_for_load_state('networkidle')
        if tag_name == 'img':
            time.sleep(0.3)
            page.keyboard.press("Escape")
        if restricted_page:
            blocking_movement(page, initial_url)
        LogClicker.logger.info(f"Clicked at position {x, y}")
    except PlaywrightTimeoutError:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
        return page
    except Exception as e:
        LogClicker.logger.error("Error: Click failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
    return page


def double_click(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    if not element:
        return page
    target_blank, has_href, tag_name = is_image_and_has_target_blank_and_href(page, element)
    initial_url = page.url
    try:
        if indication:
            draw_indicator(page, x, y, color)
            draw_indicator(page, x, y, color)
        if target_blank:
            page = open_new_tab(page, x, y, restricted_page, 2)
        elif has_href:
            with page.expect_navigation():
                page.mouse.dblclick(x, y)
        else:
            page.mouse.dblclick(x, y)
            page.wait_for_load_state('networkidle')
        if tag_name == 'img':
            time.sleep(0.3)
            page.keyboard.press("Escape")
        if restricted_page:
            blocking_movement(page, initial_url)
        LogClicker.logger.info(f"Clicked at position {x, y} 2 times")
    except PlaywrightTimeoutError:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
        return page
    except Exception as e:
        LogClicker.logger.error("Double click failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
    return page


def multiple_click(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    if not element:
        return
    tag_name = page.evaluate("(element) => element.tagName.toLowerCase()", element)
    has_href = page.evaluate("(element) => element.hasAttribute('href')", element)
    count = random.randint(3, 10)
    initial_url = page.url
    try:
        for i in range(count):
            if indication:
                draw_indicator(page, x, y, color)
        if has_href:
            with page.expect_navigation():
                page.mouse.click(x, y, click_count=count)
        else:
            page.mouse.click(x, y, click_count=count)
            page.wait_for_load_state('networkidle')
        if tag_name == 'img':
            time.sleep(0.1*count)
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
            draw_indicator(page, x, y, color)
        page.mouse.move(x, y)
        LogClicker.logger.info(f"Hovered at position {x, y}")
    except TimeoutError:
        LogClicker.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogClicker.logger.error("Hover failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)


def click_and_hold(page, indication, restricted_page, color):
    element, x, y = get_element_and_coordinate(page)
    if not element:
        return
    tag_name = page.evaluate("(element) => element.tagName.toLowerCase()", element)
    has_href = page.evaluate("(element) => element.hasAttribute('href')", element)
    initial_url = page.url
    try:
        if indication:
            draw_indicator(page, x, y, color)
        if has_href:
            with page.expect_navigation():
                page.mouse.click(x, y, delay=3000)
        else:
            page.mouse.click(x, y, delay=3000)
            page.wait_for_load_state('networkidle')
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

