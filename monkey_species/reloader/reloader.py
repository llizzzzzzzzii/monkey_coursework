from monkey_logging.monkey_logger import LogReloader
from monkey_logging.monkey_logger import LogError


def reload_page(page, ignore_errors):
    try:
        page.reload()
        LogReloader.logger.info("Reloaded page")
    except Exception:
        LogError.logger.error("Reload failed")
        if not ignore_errors:
            return False
    return True
