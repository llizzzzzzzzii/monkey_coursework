from logi.loger import LogMonkey
from specie.input_keys import send_keys_to_random_element


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
        for _ in range(self.count):
            action = self.species
            if action == 'input':
                send_keys_to_random_element(self.page, self.indication)

        LogMonkey.logger.info("Success")
