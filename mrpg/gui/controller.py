import sys

from mrpg.core.game import Game, State
from mrpg.gui import wrapper
from mrpg.gui.commons import Color
from mrpg.gui.gui import GUI


class Controller:
    def __init__(self, width=960, height=540):
        self.window = wrapper.init(self, width, height, caption="MRPG")
        self.game = Game()
        self.gui = GUI(self.window)

        cursor = self.window.get_system_mouse_cursor("crosshair")
        self.window.set_mouse_cursor(cursor)
        self.update_choices()
        self.gui.refresh(self.game)

    def resize(self, w, h):
        self.gui.resize(w, h)

    def run(self):
        wrapper.run()

    def draw(self):
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

    def resolve_to_output(self):
        while self.game.events:
            outputs = self.game.get_event().resolve()
            outputs = [s.strip() for s in outputs if s.strip()]
            if outputs:
                return outputs
        return None

    def progress_to_output(self):
        output = self.resolve_to_output()
        if output:
            return output
        while self.game.battle and self.game.battle.turn:
            self.game.progress()
            output = self.resolve_to_output()
            if output:
                return output
        if self.game.adventure and not self.game.battle:
            self.game.progress()
            output = self.resolve_to_output()
            if output:
                return output
        return None

    def update_choices(self):
        if self.game.menu:
            self.gui.menu.choices(*self.game.menu.choices)

    def enter(self):
        output = self.progress_to_output()
        if output:
            self.gui.set_output(output)
        elif self.gui.has_output():
            self.gui.set_output("")
        else:
            choice = self.gui.menu.pick()
            self.game.submit(choice)

            output = self.progress_to_output()
            if output:
                self.gui.set_output(output)
        self.update_choices()

    def key_press(self, inp):
        actions = {
            "up": self.gui.menu.up,
            "down": self.gui.menu.down,
            "escape": sys.exit,
            "enter": self.enter,
        }
        if inp in actions:
            actions[inp]()
        self.gui.refresh(self.game)
