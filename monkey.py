from logi.loger import LogMonkey
from specie.Typer import send_keys
from specie.Typer import send_text
from specie.Typer import get_random_action
from specie import Clicker

class Monkey:
    def __init__(self, url, page, count=500, species=None, delay=0, indication=False, ignore_errors=False,
                 restricted_page=False):
        self.url = url
        self.page = page
        self.count = count
        self.species = species if species else ['clicker', 'typer']
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
        Clicker.click(self.page, self.indication)
        while current < count_species:
            actions = self.species
            for action in actions:
                if action == 'typer':
                    if get_random_action() == 'text':
                        send_text(self.page, self.indication, self.delay)
                        current += 1
                    else:
                        send_keys(self.page, self.indication, self.delay)
                        current += 1
                if action == 'clicker':
                    click_action = Clicker.random_action()
                    click_action(self.page, self.indication)
                    current += 1
                if count_species == current:
                    break

        LogMonkey.logger.info("Success")
