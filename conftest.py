import pytest

@pytest.fixture()
def find_locators(page):
    locator_elements = page.query_selector_all('button, a, input, [role="button"]')
    locators_info={
        "click": [],
        "input": [],
    }
    for element in locator_elements:
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
    return locators_info
