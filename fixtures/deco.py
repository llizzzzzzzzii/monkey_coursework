import logging

class LogAction:
    logger = logging.getLogger("Action")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s - %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

class LogMonkey:
    logger = logging.getLogger("Monkey")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s %(levelname)s - %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)