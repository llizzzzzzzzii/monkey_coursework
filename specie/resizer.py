import random


def resize_page(page):
    window_size = page.viewport_size
    current_width = window_size["width"]
    current_height = window_size["height"]
    delta_width = random.randint(-100, 100)
    delta_height = random.randint(-100, 100)
    new_width = current_width + delta_width
    new_height = current_height + delta_height
    page.set_viewport_size({
        "width": new_width,
        "height": new_height
    })
    draw_rect = f"""
            const rect = document.createElement('div');
            rect.style.position = 'fixed';
            rect.style.top = '5px';
            rect.style.left = '5px';
            rect.style.width = '{new_width - 55}px';
            rect.style.height = '{new_height - 60}px';
            rect.style.border = '4px solid #ff0000';  // цвет рамки
            rect.style.opacity = '0.7';
            document.body.appendChild(rect);
                    setTimeout(() => {{
            rect.remove();
        }}, 1000); 
        """
    page.evaluate(draw_rect)
