from mrpg.gui.menu import Menu
from mrpg.gui.label import MenuLabel, Label, Printer
from mrpg.gui.commons import frame_spacing, font_big, font_normal, font_spacing
from mrpg.core.game import Output


class GUI():
    def __init__(self, window):
        self.window = window
        self.labels = []
        width, height = self.window.get_viewport_size()
        spacing = frame_spacing(height)
        self.menu = Menu(spacing, spacing, font_normal(height))

        self.init_content()

    def init_content(self):
        width, height = self.window.get_viewport_size()

        self.header = Label(
            "MRPG Prototype",
            anchor_x="left",
            anchor_y="top")

        self.display = Label(
            "",
            anchor_x="left",
            anchor_y="top",
            multiline=True)
        self.outputter = Printer(
            "",
            anchor_x="left",
            anchor_y="top")

        self.labels.append(self.header)
        self.labels.append(self.outputter)
        self.labels.append(self.display)

        self.resize(width, height)

    def resize(self, width, height):
        self.header.x=frame_spacing(height)
        self.header.y=height - frame_spacing(height)
        self.header.font_size=font_big(height)

        self.display.x=frame_spacing(height)
        self.display.y=height - frame_spacing(height)
        self.display.font_size=font_normal(height)
        self.display.width=width // 2

        self.outputter.resize(width // 2, height - frame_spacing(height), font_normal(height))

        spacing = frame_spacing(height)
        self.menu.resize(spacing, spacing, font_normal(height))

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
