import time
from logi.loger import LogClicker
from locators import get_random_coordinate


def hover(monkey, w_size, page):
    x, y = get_random_coordinate(w_size)
    try:
        page.mouse.move(x, y)
        if monkey.indication:
            monkey.draw_and_clear_circle(page, x, y)
    except Exception:
        LogClicker.logger.exception("Error: Hover failed")
        exit()
    LogClicker.logger.info(f"Hovered at position ({x, y})")


def one_click(monkey, w_size, page):
    x, y = get_random_coordinate(w_size)
    try:
        page.mouse.move(x, y)
        if monkey.indication:
            monkey.draw_and_clear_circle(page, x, y)
        page.mouse.click(x, y)
    except Exception:
        LogClicker.logger.exception("Error: Click failed")
        exit()
    LogClicker.logger.info(f"Clicked at position ({x, y})")

def double_click(monkey, w_size, page):
    x, y = get_random_coordinate(w_size)
    try:
        page.mouse.move(x, y)
        if monkey.indication:
            monkey.draw_and_clear_circle(page, x, y)
            monkey.draw_and_clear_circle(page, x, y)
        page.mouse.dblclick(x, y)
    except Exception:
        LogClicker.logger.exception("Error: Double click failed")
        exit()
    LogClicker.logger.info(f"Clicked at position ({x, y}) 2 times")


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
        LogClicker.logger.exception("Error: Multiple clicks failed")
        exit()
    LogClicker.logger.info(f"Clicked at position ({x, y}) {count} times")