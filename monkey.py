from monkey_logging.monkey_logger import LogMonkey
from monkey_logging.monkey_logger import LogError
from monkey_species.typer.typer import send_keys
from monkey_species.typer.typer import send_text
from monkey_species.typer.typer import get_random_action
from monkey_species.clicker import clicker
from monkey_species.resizer.resizer import resize_page
from monkey_species.scroller.scroller import scroll_to_random_position
from monkey_species.reloader.reloader import reload_page
from monkey_species.toucher.toucher import touch
import time


class Monkey:
    def __init__(self, url, page, count=500, species=None, delay=0, indication=False, ignore_errors=False,
                 restricted_page=False, color='red'):
        self.url = url
        self.page = page
        self.count = count
        self.species = species if species else ['clicker', 'typer', 'scroller', 'reloader', 'resizer', 'toucher']
        self.delay = delay
        self.indication = indication
        self.ignore_errors = ignore_errors
        self.restricted_page = restricted_page
        self.color = color


    def log_console_message(self, msg):
        if msg.type == 'error':
            LogError.logger.error(f"Console error: {msg.text}")
            if not self.ignore_errors:
                self.count = 0


    def run(self):
        try:
            species_str = ', '.join(specie for specie in self.species)
            LogMonkey.logger.info(f"Run monkey with {species_str}")
            self.page.goto(self.url)
            self.page.wait_for_load_state('domcontentloaded')
            current = 0
            self.page.on("console", lambda msg: self.log_console_message(msg))
            while current < self.count:
                actions = self.species
                for action in actions:
                    #тестовая строка для вызова ошибок в браузере
                    #self.page.evaluate('''console.error("Это тестовая ошибка в браузере");''')
                    if action == 'typer':
                        if get_random_action() == 'text':
                            result = send_text(self.page, self.indication, self.restricted_page, self.color)
                            current += 1
                            time.sleep(self.delay)
                        else:
                            result = send_keys(self.page, self.indication, self.restricted_page, self.color)
                            current += 1
                            time.sleep(self.delay)
                    if action == 'clicker':
                        click_action = clicker.random_action()
                        result = click_action(self.page, self.indication, self.restricted_page, self.ignore_errors, self.color)
                        current += 1
                        time.sleep(self.delay)
                    if action == 'scroller':
                        result = scroll_to_random_position(self.page, self.ignore_errors)
                        current += 1
                        time.sleep(self.delay)
                    if action == 'reloader':
                        result = reload_page(self.page, self.ignore_errors)
                        current += 1
                        time.sleep(self.delay)
                    if action == 'resizer':
                        result = resize_page(self.page, self.ignore_errors,self.color)
                        current += 1
                        time.sleep(self.delay)
                    if action == 'toucher':
                        result = touch(self.page, self.indication, self.restricted_page, self.ignore_errors,self.color)
                        current += 1
                        time.sleep(self.delay)
                    if not result or self.count == 0:
                        LogMonkey.logger.error("Fail")
                        return
                    if self.count == current:
                        break
        except Exception as e:
            LogMonkey.logger.error("Error: Monkey run")
            LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
            return

        LogMonkey.logger.info("Success")
