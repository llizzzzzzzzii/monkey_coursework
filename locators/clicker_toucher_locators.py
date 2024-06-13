def find_locators(page):
    page.wait_for_load_state("load")
    clickable_elements = page.query_selector_all('button, a, input, img, [role="button"], [class="button"]')
    visible_clickable_elements = [get_selector(page, element) for element in clickable_elements
                                  if is_element_visible(page, element)]
    return visible_clickable_elements

def get_selector(page, element):
    tag_name = page.evaluate("element => element.tagName.toLowerCase()", element)
    attributes_values = {
        'id': element.get_attribute('id'),
        'title': element.get_attribute('title'),
        'alt': element.get_attribute('alt'),
        'class': element.get_attribute('class'),
        'href': element.get_attribute('href')
    }
    attributes = [f"[{key}='{value}']" for key, value in attributes_values.items() if value]
    attribute_selector = ''.join(attributes)
    return f"{tag_name}{attribute_selector}"


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
