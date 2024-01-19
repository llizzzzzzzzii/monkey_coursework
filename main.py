import random
import time
from playwright.sync_api import sync_playwright
import pyautogui


def draw_and_clear_circle(page, x, y, size):
    script = '''
        (args) => {
            const [x, y, size] = args;
            const div = document.createElement('div');
            div.style.position = 'absolute';
            div.style.left = `${x}px`;
            div.style.top = `${y}px`;
            div.style.width = `${size}px`;
            div.style.height = `${size}px`;
            div.style.opacity = '0.5';
            div.style.background = 'red';
            div.style.borderRadius = '50%';
            document.body.appendChild(div);

            setTimeout(() => {
                div.remove();  // Удаляем элемент после задержки (например, 1000 миллисекунд)
            }, 500);
        }
    '''
    page.evaluate(script, [x, y, size])


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.set_viewport_size({"width": 1800, "height": 1200})
    page.goto(
        'https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0')
    window_size = page.evaluate('''() => {
        return {
            width: window.innerWidth,
            height: window.innerHeight
        }
    }''')

    for _ in range(5):
        x = random.randint(0, window_size['width'])
        y = random.randint(0, window_size['height'])
        size = 15

        pyautogui.moveTo(x, y)
        draw_and_clear_circle(page, x, y, size)
        pyautogui.click(x, y)

        print('Click at position:', x, y)
        time.sleep(2)

    browser.close()
