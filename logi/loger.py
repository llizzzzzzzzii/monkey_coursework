import logging
from colorlog import ColoredFormatter


def set_logger(logger):
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s%(name)s: %(message)s%(reset)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)


class LogError:
    logger = logging.getLogger("Error")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class LogClicker:
    logger = logging.getLogger("Clicker")
    set_logger(logger)


class LogTyper:
    logger = logging.getLogger("Typer")
    set_logger(logger)


class LogMonkey:
    logger = logging.getLogger("Monkey")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s%(message)s%(reset)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'red',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
