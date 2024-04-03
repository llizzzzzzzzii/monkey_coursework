from monkey_logging.monkey_logger import LogMonkey
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
                 restricted_page=False):
        self.url = url
        self.page = page
        self.count = count
        self.species = species if species else ['clicker', 'typer', 'scroller', 'reloader', 'resizer', 'toucher']
        self.delay = delay
        self.indication = indication
        self.ignore_errors = ignore_errors
        self.restricted_page = restricted_page

    def run(self):
        species_str = ', '.join(specie for specie in self.species)
        LogMonkey.logger.info(f"Run monkey with {species_str}")
        self.page.goto(self.url)
        self.page.wait_for_load_state('domcontentloaded')
        count_species = self.count
        current = 0
        while current < count_species:
            actions = self.species
            for action in actions:
                if action == 'typer':
                    if get_random_action() == 'text':
                        send_text(self.page, self.indication, self.restricted_page)
                        current += 1
                        time.sleep(self.delay)
                    else:
                        send_keys(self.page, self.indication, self.restricted_page)
                        current += 1
                        time.sleep(self.delay)
                if action == 'clicker':
                    click_action = clicker.random_action()
                    result = click_action(self.page, self.indication, self.restricted_page, self.ignore_errors)
                    current += 1
                    time.sleep(self.delay)
                if action == 'scroller':
                    scroll_to_random_position(self.page)
                    current += 1
                    time.sleep(self.delay)
                if action == 'reloader':
                    reload_page(self.page)
                    current += 1
                    time.sleep(self.delay)
                if action == 'resizer':
                    resize_page(self.page)
                    current += 1
                    time.sleep(self.delay)
                if action == 'toucher':
                    touch(self.page, self.indication, self.restricted_page)
                    current += 1
                    time.sleep(self.delay)
                if count_species == current:
                    if not result:
                        LogMonkey.logger.error("Fail")
                        return
                    break

        LogMonkey.logger.info("Success")
