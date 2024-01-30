import random
import time
from playwright.sync_api import sync_playwright

def get_random_coordinate(w_size):
    x = random.randint(0, w_size['width'])
    y = random.randint(0, w_size['height'])
    return x, y

class MonkeyRunner:
    def __init__(self, url, count=500, species=None, delay=0, indication=None, ignore_errors=False, restricted_page=False):
        self.url = url
        self.count = count
        self.species = species
        self.delay = delay
        self.indication = indication
        self.ignore_errors = ignore_errors
        self.restricted_page = restricted_page

    def draw_and_clear_circle(self, page, x, y, size, duration=500):
        script = '''
                async (params) => {
                    const [x, y, size, duration] = params;
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

                    await new Promise(resolve => setTimeout(resolve, duration));

                    div.remove();
                }
            '''
        page.evaluate(script, [x, y, size, duration])

    def run_monkey(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.set_viewport_size({"width": 1800, "height": 1200})
            page.goto(self.url)
            window_size = page.evaluate('''() => {
                    return {
                        width: window.innerWidth,
                        height: window.innerHeight
                    }
                }''')

            size = 15
            for _ in range(5):
                x,y=get_random_coordinate(window_size)
                self.draw_and_clear_circle(page,x,y,size,duration=100)
                page.mouse.click(x,y)
                time.sleep(pause)

            browser.close()

if __name__ == "__main__":
    url = 'https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'
    count = 500
    species = None
    delay = 0
    indication = None
    ignore_errors = False
    restricted_page = False

    pause = 1

    monkey = MonkeyRunner(url, count, species, delay, indication, ignore_errors, restricted_page)
    monkey.run_monkey()