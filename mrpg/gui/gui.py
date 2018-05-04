from mrpg.gui.menu import Menu
from mrpg.gui.label import MenuLabel, Label, Printer
from mrpg.gui.commons import FRAME_SPACING, FONT_SIZE_SMALL
from mrpg.core.game import Output


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

        self.display = Label(
            "",
            x=FRAME_SPACING,
            y=self.window.height - FRAME_SPACING,
            anchor_x="left",
            anchor_y="top",
            font_size=FONT_SIZE_SMALL,
            multiline=True,
            width=600)
        self.outputter = Printer(
            "",
            x=self.window.width - FRAME_SPACING - 600,
            y=self.window.height - FRAME_SPACING,
            anchor_x="left",
            anchor_y="top",
            font_size=FONT_SIZE_SMALL)
        self.labels.append(self.header)
        self.labels.append(self.outputter)
        self.labels.append(self.display)

    def draw(self):
        for label in self.labels:
            label.draw()
        self.menu.draw()

    def set_output(self, outputs):
        if type(outputs) is str:
            self.outputter.set_text(outputs)
        strings = []
        for message in outputs:
            if type(message) is str:
                strings.append(message)
                continue
            data = message.data
            if type(message) is Output.Display:
                self.display.text = data
                continue
            if type(data) is list:
                data = "\n".join(data)
            strings.append(data)
        self.outputter.set_text("\n".join(strings))

    def update(self, dt):
        self.menu.update(dt)
        self.outputter.update(dt)
