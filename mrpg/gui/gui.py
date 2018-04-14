from mrpg.gui.menu import Menu
from mrpg.gui.label import Label
from mrpg.gui.commons import FRAME_SPACING


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
