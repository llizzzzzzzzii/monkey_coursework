from monkey_logging.monkey_logger import LogReloader
from monkey_logging.monkey_logger import LogError


def reload_page(page, ignore_errors):
    try:
        page.reload()
        LogReloader.logger.info("Reloaded page")
    except Exception as e:
        LogReloader.logger.error("Error: Reload failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
        if not ignore_errors:
            return False
    return True
