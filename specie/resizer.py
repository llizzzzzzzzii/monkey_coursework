import random
import tkinter as tk


def resize_page(page):
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
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
