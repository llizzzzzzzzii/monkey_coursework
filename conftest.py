import pytest
import random

@pytest.fixture()
def find_locators(page):
    clickable_elements = page.query_selector_all('button, a, input, [role="button"]')
    locators_info = {
        "click": [],
        "input": [],
    }
    for element in clickable_elements:
        tag_name = element.get_property('tagName')
        locators_info['click'] = tag_name

    input_info = {}
    input_elements = page.query_selector_all('input, textarea, [contenteditable=true]')
    for element in input_elements:
        try:
            element.fill('')
            tag_name = element.get_property('tagName')
            locators_info['input'] = tag_name
        except Exception as e:
            input_info[element] = "Error: " + str(e)

    clickable_images = page.query_selector_all('img')
    for image in clickable_images:
        clickable = image.evaluate('(node) => node.parentElement.tagName === "A"')
        if clickable:
            locators_info['click'] = image
    return locators_info

def get_random_coordinate(w_size):
    x = random.randint(0, w_size['width'])
    y = random.randint(0, w_size['height'])
    return x, y
