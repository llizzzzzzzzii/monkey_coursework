import time
from conftest import get_random_coordinate
from fixtures.deco import LogClicker

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
        LogClicker.logger.exception("Error: Hold failed")
        exit()
    LogClicker.logger.info(f"Hold the mouse for {duration} s at position: {x, y}")


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
        LogClicker.logger.exception("Error: Click and hold failed")
        exit()
    LogClicker.logger.info(f"Clicked and held at position ({x, y})")
