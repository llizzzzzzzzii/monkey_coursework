import time
from main import get_random_coordinate
from deco import *


def hover(self, w_size, page, size):
    x, y = get_random_coordinate(w_size)
    try:
        page.mouse.move(x, y)
        self.draw_and_clear_circle(page, x, y, size)
    except Exception:
        LogMonkey.logger.exception("Error mouse hover")
        exit()
    LogAction.logger.info(f"Hover at position: {x, y}")


def one_click(self, w_size, page, size):
    x, y = get_random_coordinate(w_size)
    try:
        page.mouse.move(x, y)
        self.draw_and_clear_circle(page, x, y, size)
        page.mouse.click(x, y)
    except Exception:
        LogMonkey.logger.exception("Error mouse click")
        exit()
    LogAction.logger.info(f"Click at position: {x, y}")


def double_click(self, w_size, page, size):
    x, y = get_random_coordinate(w_size)
    try:
        page.mouse.move(x, y)
        self.draw_and_clear_circle(page, x, y, size)
        page.mouse.dblclick(x, y)
        self.draw_and_clear_circle(page, x, y, size)
    except Exception:
        LogMonkey.logger.exception("Error mouse double click")
        exit()
    LogAction.logger.info(f"Double click at position: {x, y}")


def multi_click(self, count, w_size, page, size):
    x, y = get_random_coordinate(w_size)
    try:
        page.mouse.move(x, y)
        for i in range(count):
            self.draw_and_clear_circle(page, x, y, size)
            page.mouse.click(x, y)
            time.sleep(0.3)
    except Exception:
        LogMonkey.logger.exception("Error mouse multi clicks")
        exit()
    LogAction.logger.info(f"{count} clicks at position: {x, y}")