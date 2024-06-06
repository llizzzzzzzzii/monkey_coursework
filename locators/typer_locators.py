def find_locators(page):
    page.wait_for_load_state("networkidle")
    input_elements = page.query_selector_all('input:not([readonly]):not([disabled]), textarea:not([disabled]), '
                                             'div[contenteditable=true]:not([disabled]),'
                                             '[role="textbox"]:not([disabled])')
    visible_input_elements = [element for element in input_elements if is_element_visible(page, element)]
    return visible_input_elements


def is_element_visible(page, element):
    if not (element.is_visible() and
            0 <= element.bounding_box()['y'] <= page.viewport_size['height']
            and element.get_attribute("type") not in ["radio", "checkbox", "submit", "button", "file",
                                                      "reset", 'color', 'range']
            and element.get_attribute('type') != 'url'
            and element.get_attribute('aria-disabled') != 'true'
            and element.get_attribute('aria-readonly') != 'true'):
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
