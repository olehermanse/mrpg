"""Renders the state of a game and controller object using pyglet"""

import pyglet


class Color:
    # Off black and white look a little more pleasant
    BLACK = (16, 16, 16, 255)
    WHITE = (230, 230, 230, 255)

    def float(c):
        return (x / 255 for x in c)


class Renderer():
    def __init__(self, controller, window):
        self.controller = controller
        self.window = window
        cursor = window.get_system_mouse_cursor("crosshair")
        window.set_mouse_cursor(cursor)

        self.labels = []
        title = pyglet.text.Label(
            'MRPG - Prototype',
            font_name='Arial',
            font_size=36,
            x=0,
            y=self.window.height,
            anchor_x='left',
            anchor_y='top',
            color=Color.WHITE)
        self.labels.append(title)

    def render(self):
        self.window.clear()
        pyglet.gl.glClearColor(*Color.float(Color.BLACK))
        for label in self.labels:
            label.draw()
