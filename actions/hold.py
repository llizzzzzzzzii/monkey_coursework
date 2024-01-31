import time
from main import get_random_coordinate
from fixtures.deco import *


def hold(self, duration, w_size, page, size):
    x, y = get_random_coordinate(w_size)
    try:
        page.mouse.move(x, y)
        page.mouse.down()
        self.draw_and_clear_circle(page, x, y, size, duration * 1000)
        page.wait_for_timeout(duration * 1000)
        page.mouse.up()
    except Exception:
        LogMonkey.logger.exception("Error hold")
        exit()
    LogAction.logger.info(f"Hold the mouse for {duration} s at position: {x, y}")


def click_and_hold(self, duration, w_size, page, size):
    x, y = get_random_coordinate(w_size)
    try:
        page.mouse.move(x, y)
        page.mouse.click(x, y)
        page.mouse.down()
        self.draw_and_clear_circle(page, x, y, size, duration * 1000)
        page.wait_for_timeout(duration * 1000)
        page.mouse.up()
    except Exception:
        LogMonkey.logger.exception("Error click and hold")
        exit()
    LogAction.logger.info(f"Click and hold the mouse for {duration} s at position: {x, y}")


def hold_and_move_mouse(self, duration, w_size, page, size):
    start_x, start_y = get_random_coordinate(w_size)
    end_x, end_y = get_random_coordinate(w_size)
    try:
        page.mouse.move(start_x, start_y)
        page.mouse.down()
        self.draw_and_clear_circle(page, start_x, start_y, size, duration * 1000)
        page.wait_for_timeout(duration * 1000)

        # рисование пути
        steps = 5
        for i in range(steps):
            x = start_x + (end_x - start_x) * (i + 1) / steps
            y = start_y + (end_y - start_y) * (i + 1) / steps
            self.draw_and_clear_circle(page, x, y, size, 300)
            time.sleep(0.2)

        self.draw_and_clear_circle(page, end_x, end_y, size, duration * 1000)
        page.mouse.move(end_x, end_y)
        page.wait_for_timeout(duration * 1000)  # удерживаем кол-во секунд?
        page.mouse.up()
    except Exception:
        LogMonkey.logger.exception("Error hold and move")
        exit()
    LogAction.logger.info(f"Hold and moving from position {start_x, start_y} to {end_x, end_y}")