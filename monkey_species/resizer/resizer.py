from monkey_logging.monkey_logger import LogResizer
from monkey_logging.monkey_logger import LogError
import random
import pyautogui

def resize_page(page, ignore_errors):
    try:
        screen_width, screen_height = pyautogui.size()
        new_width = random.randint(800, screen_width)
        new_height = random.randint(600, screen_height)
        draw_rect = f"""
            const rect = document.createElement('div');
            rect.style.position = 'fixed';
            rect.style.top = '20px';
            rect.style.left = '20px';
            rect.style.width = '{new_width - 100}px';
            rect.style.height = '{new_height - 100}px';
            rect.style.border = '4px solid #ff0000'; // Цвет рамки красный
            rect.style.opacity = '0.7';
            document.body.appendChild(rect);
                    setTimeout(() => {{
                rect.remove();
            }}, 1000);
        """
        page.evaluate(draw_rect)
        page.set_viewport_size({"width": new_width, "height": new_height})
        LogResizer.logger.info(f"Resized to {new_width, new_height}")
    except Exception as e:
        LogResizer.logger.error("Error: Resize failed")
        LogError.logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
        if not ignore_errors:
            return False
    return True
