import time
from matplotlib.colors import to_rgba

def draw_indicator(page, x, y, color):
    rgba_color = to_rgba(color, alpha=0.7)
    rgba_str = f"rgba({int(rgba_color[0] * 255)},{int(rgba_color[1] * 255)},{int(rgba_color[2] * 255)},{rgba_color[3]})"
    radius = 15
    page.evaluate(f"""
        const indicator = document.createElement('div');
        indicator.style.cssText = `
            position: fixed !important;
            background-color: {rgba_str} !important;
            width: {radius}px !important;
            height: {radius}px !important;
            border: 2px solid red !important;
            border-radius: 50% !important;
            left: {x}px !important;
            top: {y}px !important;
            transform: translate(-50%, -50%) !important;
            z-index: 2147483647 !important;
        `;
        document.body.appendChild(indicator);
        setTimeout(() => indicator.remove(), 700);
    """)
    time.sleep(0.7)
