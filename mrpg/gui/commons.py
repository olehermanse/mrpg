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


def create_label(*args, **kwargs):
    defaults = dict(
        font_name=["Ubuntu Mono", "Consolas"],
        font_size=FONT_SIZE,
        anchor_x="left",
        anchor_y="bottom",
        color=Color.WHITE)
    for key in defaults:
        if key not in kwargs:
            kwargs[key] = defaults[key]
    return pyglet.text.Label(*args, **kwargs)
