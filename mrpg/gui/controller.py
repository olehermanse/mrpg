import sys

import pyglet

from mrpg.core.game import Game
from mrpg.gui import wrapper
from mrpg.gui.commons import FRAME_SPACING, Color
from mrpg.gui.menu import Menu
from mrpg.gui.label import Label


class GUI():
    def __init__(self, window):
        self.window = window
        self.labels = []
        self.menu = Menu()

        self.init_content()

    def init_content(self):
        self.header = Label(
            "MRPG Prototype",
            x=FRAME_SPACING,
            y=self.window.height - FRAME_SPACING,
            anchor_x="left",
            anchor_y="top")
        self.labels.append(self.header)

    def draw(self):
        for label in self.labels:
            label.draw()
        self.menu.draw()

    def update(self, dt):
        self.menu.update(dt)
        self.header.update(dt)


class Controller():
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.window = wrapper.init(self, width, height, caption="MRPG")
        self.game = Game()
        self.gui = GUI(self.window)

        self.gui.menu.choices(*self.game.menu.choices)

        cursor = self.window.get_system_mouse_cursor("crosshair")
        self.window.set_mouse_cursor(cursor)

    def run(self):
        wrapper.run()

    def draw(self):
        self.window.clear()
        pyglet.gl.glClearColor(*Color.float(Color.BLACK))
        self.gui.draw()

    def update(self, dt):
        self.gui.update(dt)

    def mouse_motion(self, x, y, dx, dy):
        pass

    def mouse_press(self, x, y, button, modifiers):
        pass

    def mouse_release(self, x, y, button, modifiers):
        pass

    def mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def update_header(self):
        if self.game.menu:
            self.gui.header.text = self.game.menu.headline.replace(":", "")

    def enter(self):
        choice = self.gui.menu.pick()
        self.game.submit(choice)
        if self.game.menu:
            self.gui.menu.choices(*self.game.menu.choices)

        self.update_header()

    def key_press(self, inp):
        actions = {
            "up": self.gui.menu.up,
            "down": self.gui.menu.down,
            "escape": sys.exit,
            "enter": self.enter
        }
        if inp in actions:
            actions[inp]()
