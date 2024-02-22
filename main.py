from fixtures.deco import LogMonkey
from playwright.sync_api import sync_playwright
from actions.click import one_click
from fixtures.constants import Links


class MonkeyRunner:
    def __init__(self, url, count=500, species=None, delay=0, indication=False,
                 indication_size=15, ignore_errors=False,
                 restricted_page=False):
        self.url = url
        self.count = count
        self.species = species
        self.delay = delay
        self.indication = indication
        self.indication_size = indication_size
        self.ignore_errors = ignore_errors
        self.restricted_page = restricted_page

    def draw_and_clear_circle(self, page, x, y, duration=500):
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

                    await new Promise(resolve => setTimeout(resolve, duration)
                    );

                    div.remove();
                }
            '''

        page.evaluate(script, [x, y, self.indication_size, duration])

    def run_monkey(self):
        LogMonkey.logger.info("Running monkey...")
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                page.set_viewport_size({"width": 1800, "height": 1200})
                page.goto(self.url)
                page.wait_for_selector('body')
                window_size = page.evaluate('''() => {
                        return {
                            width: window.innerWidth,
                            height: window.innerHeight
                        }
                    }''')
            except Exception:
                LogMonkey.logger.exception("Error opening a web page")
                exit()

            for _ in range(5):
                one_click(self, window_size, page)
            # click_and_hold(self, window_size, page)
            # hold_and_move_mouse(self, window_size, page)
            # multi_click(self, window_size, page)
            # hold(self, window_size, page)
            # double_click(self, window_size, page)
            # hover(self, window_size, page)

            browser.close()


if __name__ == "__main__":
    LogMonkey.logger.info("Configuring monkey...")
    url = Links.URL
    indicate = True
    monkey = MonkeyRunner(url, indicate)
    monkey.run_monkey()
