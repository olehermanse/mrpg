import sys

import pyglet

from mrpg.core.game import Game, State
from mrpg.gui import wrapper
from mrpg.gui.commons import Color
from mrpg.gui.gui import GUI


class Controller():
    def __init__(self, width=1280, height=720):
        self.window = wrapper.init(self, width, height, caption="MRPG")
        self.game = Game()
        self.gui = GUI(self.window)
        self.width, self.height = self.window.get_viewport_size()

        self.gui.menu.choices(*self.game.menu.choices)

        cursor = self.window.get_system_mouse_cursor("crosshair")
        self.window.set_mouse_cursor(cursor)

    def resize(self, w, h):
        width, height = self.window.get_viewport_size()
        self.gui.resize(width, height)

    def run(self):
        wrapper.run()

    def draw(self):
        self.window.clear()

        pyglet.gl.glClearColor(*Color.float(Color.BLACK))
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()

        width, height = self.window.get_viewport_size()

        pyglet.gl.glOrtho(0, width, 0, height, -1, 1)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)

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
        self.gui.header.text = ""
        # if self.game.menu:
        #     self.gui.header.text = self.game.menu.headline.replace(":", "")

    def update_text_display(self):
        state = self.game.state
        if state == State.MAIN_MENU:
            self.gui.display.text = ""
        elif state == State.GAME_MENU:
            self.gui.display.text = self.game.player.string_long()
        elif state == State.BATTLE_MENU:
            self.gui.display.text = self.game.battle.stats()

    def enter(self):
        choice = self.gui.menu.pick()
        self.game.submit(choice)
        if self.game.menu:
            self.gui.menu.choices(*self.game.menu.choices)
        self.gui.set_output(self.game.get_output())
        self.update_header()
        self.update_text_display()

    def key_press(self, inp):
        actions = {
            "up": self.gui.menu.up,
            "down": self.gui.menu.down,
            "escape": sys.exit,
            "enter": self.enter
        }
        if inp in actions:
            actions[inp]()
