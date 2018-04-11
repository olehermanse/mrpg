import pyglet

FONT_SIZE = 32
SPACING = FONT_SIZE // 2
FRAME_SPACING = FONT_SIZE * 2


class Color:
    # Off black and white look a little more pleasant:
    BLACK = (16, 16, 16, 255)
    WHITE = (230, 230, 230, 255)

    def float(c):
        return (x / 255 for x in c)
