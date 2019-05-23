def font_big(window_height):
    return window_height // 24

def font_normal(window_height):
    return 3 * font_big(window_height) // 5

def font_spacing(font_size):
    return font_size // 2

def frame_spacing(window_height):
    return font_big(window_height) * 2

class Color:
    # Off black and white look a little more pleasant:
    BLACK = (16, 16, 16, 255)
    WHITE = (230, 230, 230, 255)

    def float(c):
        return (x / 255 for x in c)
