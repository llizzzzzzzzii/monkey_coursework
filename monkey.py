from logi.loger import LogMonkey
from specie.input_keys import send_keys
from specie.input_keys import send_text
from specie.input_keys import get_random_action


class Monkey:
    def __init__(self, url, page, count=500, species=None, delay=0, indication=False, ignore_errors=False,
                 restricted_page=False):
        self.url = url
        self.page = page
        self.count = count
        self.species = species if species else ['click', 'input']
        self.delay = delay
        self.indication = indication
        self.ignore_errors = ignore_errors
        self.restricted_page = restricted_page

    def run(self):
        LogMonkey.logger.info(f"Run monkey with {self.species}")
        self.page.goto(self.url)
        self.page.wait_for_load_state('domcontentloaded')
        count_species = self.count
        current = 0
        while current < count_species:
            actions = self.species
            for action in actions:
                if action == 'input':
                    if get_random_action() == 'text':
                        send_text(self.page, self.indication, self.delay)
                        current += 1
                    else:
                        send_keys(self.page, self.indication, self.delay)
                        current += 1
                if count_species == current:
                    break

        LogMonkey.logger.info("Success")
