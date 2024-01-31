import time
from fixtures.deco import LogAction
from conftest import get_random_coordinate

def hover(monkey, w_size, page):
    x, y = get_random_coordinate(w_size)
    try:
        page.mouse.move(x, y)
        if monkey.indication:
            monkey.draw_and_clear_circle(page, x, y)
    except Exception:
        LogAction.logger.exception("Error mouse hover")
        exit()
    LogAction.logger.info(f"Hover at position: {x, y}")


def one_click(monkey, w_size, page):
    x, y = get_random_coordinate(w_size)
    try:
        page.mouse.move(x, y)
        if monkey.indication:
            monkey.draw_and_clear_circle(page, x, y)
        page.mouse.click(x, y)
    except Exception:
        LogAction.logger.exception("Error mouse click")
        exit()
    LogAction.logger.info(f"Click at position: {x, y}")

def double_click(monkey, w_size, page):
    x, y = get_random_coordinate(w_size)
    try:
        page.mouse.move(x, y)
        if monkey.indication:
            monkey.draw_and_clear_circle(page, x, y)
            monkey.draw_and_clear_circle(page, x, y)
        page.mouse.dblclick(x, y)
    except Exception:
        LogAction.logger.exception("Error mouse double click")
        exit()
    LogAction.logger.info(f"Double click at position: {x, y}")


def multi_click(monkey, w_size, page, count=5):
    x, y = get_random_coordinate(w_size)
    try:
        page.mouse.move(x, y)
        for i in range(count):
            if monkey.indication:
                monkey.draw_and_clear_circle(page, x, y)
            page.mouse.click(x, y)
            time.sleep(0.1)
    except Exception:
        LogAction.logger.exception("Error mouse multi clicks")
        exit()
    LogAction.logger.info(f"{count} clicks at position: {x, y}")