from matplotlib.colors import to_rgba
import time


def draw_indicator(page, element, color):
    rgba_color = to_rgba(color, alpha=0.7)
    rgba_str = f"rgba({int(rgba_color[0] * 255)},{int(rgba_color[1] * 255)},{int(rgba_color[2] * 255)},{rgba_color[3]})"
    page.evaluate(
        f"""(element) => {{
                element.style.backgroundColor = '{rgba_str}';
                element.style.zIndex = '2147483647';
                element.style.position = 'relative';  // Ensures zIndex is respected
            }}""",
        element
    )
    time.sleep(0.5)
    page.evaluate(
        """(element) => {
            element.style.backgroundColor = '';
            element.style.zIndex = '';
            element.style.position = '';
        }""",
        element
    )
