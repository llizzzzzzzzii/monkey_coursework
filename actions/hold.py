import time
from conftest import get_random_coordinate
from fixtures.deco import LogAction

def hold(monkey, w_size, page, duration=5):
    x, y = get_random_coordinate(w_size)
    try:
        page.mouse.move(x, y)
        page.mouse.down()
        if monkey.indication:
            monkey.draw_and_clear_circle(page, x, y, duration * 1000)
        else:
            page.wait_for_timeout(duration * 1000)
        page.mouse.up()
    except Exception:
        LogAction.logger.exception("Error hold")
        exit()
    LogAction.logger.info(f"Hold the mouse for {duration} s at position: {x, y}")


def click_and_hold(monkey, w_size, page, duration=5):
    x, y = get_random_coordinate(w_size)
    try:
        page.mouse.move(x, y)
        page.mouse.click(x, y)
        page.mouse.down()
        if monkey.indication:
            monkey.draw_and_clear_circle(page, x, y, duration * 1000)
        else:
            page.wait_for_timeout(duration * 1000)
        page.mouse.up()
    except Exception:
        LogAction.logger.exception("Error click and hold")
        exit()
    LogAction.logger.info(f"Click and hold the mouse for {duration} s at position: {x, y}")
