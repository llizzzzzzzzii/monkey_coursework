from monkey_logging.monkey_logger import LogReloader
from monkey_logging.monkey_logger import LogError


def reload_page(page):
    try:
        page.reload()
        LogReloader.logger.info("Reloaded page")
    except TimeoutError as e:
        LogReloader.logger.warning("Warning: The waiting time for the action has been exceeded")
    except Exception as e:
        LogReloader.logger.error("Error: Reload failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
