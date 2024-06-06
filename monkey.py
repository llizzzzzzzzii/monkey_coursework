from monkey_logging.monkey_logger import LogMonkey
from monkey_logging.monkey_logger import LogError
from monkey_species.typer.typer import get_random_action
from monkey_species.clicker import clicker
from monkey_species.resizer.resizer import resize_page
from monkey_species.scroller.scroller import scroll_to_random_position
from monkey_species.reloader.reloader import reload_page
from monkey_species.toucher.toucher import touch
from playwright._impl._errors import TimeoutError as PlaywrightTimeoutError
from playwright._impl._errors import TargetClosedError as PlaywrightTargetClosedError
from playwright._impl._errors import Error as PlaywrightError
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

    def on_page_popup(self, popup):
        popup.close()

    def run(self):
        try:
            species_str = ', '.join(specie for specie in self.species)
            LogMonkey.logger.info(f"Run monkey with {species_str}")
            self.page.goto(self.url)
            if self.restricted_page:
                self.page.on("popup", self.on_page_popup)
            current = 0
            self.page.on("console", lambda msg: self.log_console_message(msg))
            while current < self.count:
                actions = self.species
                for action in actions:
                    if action == 'typer':
                        typer_action = get_random_action()
                        typer_action(self.page, self.indication, self.restricted_page, self.color)
                    elif action == 'clicker':
                        click_action = clicker.random_action()
                        self.page = click_action(self.page, self.indication, self.restricted_page, self.color)
                    elif action == 'scroller':
                        scroll_to_random_position(self.page)
                    elif action == 'reloader':
                        reload_page(self.page)
                    elif action == 'resizer':
                        resize_page(self.page, self.color)
                    elif action == 'toucher':
                        self.page = touch(self.page, self.indication, self.restricted_page, self.color)
                    else:
                        LogMonkey.logger.error("Error: Unknown action")
                        LogMonkey.logger.error("Fail")
                        return
                    current += 1
                    if self.count == 0:
                        LogMonkey.logger.error("Fail")
                        return
                    if self.count == current:
                        break
                    time.sleep(self.delay)
        except PlaywrightTimeoutError:
            LogMonkey.logger.error("Error: The page is not responding")
            LogMonkey.logger.error("Fail")
            return
        except PlaywrightTargetClosedError:
            LogMonkey.logger.error("Error: Target page, context or browser has been closed")
            LogMonkey.logger.error("Fail")
            return
        except PlaywrightError:
            LogMonkey.logger.error("Error: The execution of the request was interrupted. Maybe frame was detached")
            LogMonkey.logger.error("Fail")
            return
        except Exception as e:
            LogMonkey.logger.error("Error: Monkey run")
            LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
            return

        LogMonkey.logger.info("Success")
