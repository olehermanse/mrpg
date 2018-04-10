"""Renders the state of a game and controller object using pyglet"""

import pyglet

from mrpg.gui.commons import Color, FRAME_SPACING, create_label
from mrpg.gui.menu import Menu


class Renderer():
    def __init__(self, controller, window):
        self.controller = controller
        self.window = window
        cursor = window.get_system_mouse_cursor("crosshair")
        window.set_mouse_cursor(cursor)

        self.labels = []

        self.init_content()

    def init_content(self):
        title = create_label(
            "MRPG - Prototype",
            x=FRAME_SPACING,
            y=self.window.height - FRAME_SPACING,
            anchor_x="left",
            anchor_y="top")
        self.labels.append(title)
        self.menu = Menu()
        self.menu.choices("New", "Load", "Quit")

    def render(self):
        self.window.clear()
        pyglet.gl.glClearColor(*Color.float(Color.BLACK))
        for label in self.labels:
            label.draw()
        self.menu.draw()
