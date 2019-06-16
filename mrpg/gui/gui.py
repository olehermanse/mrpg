from mrpg.gui.menu import Menu
from mrpg.gui.label import MenuLabel, Label, Printer
from mrpg.gui.battle_gui import BattleGUI
from mrpg.gui.commons import frame_spacing, font_big, font_normal, font_spacing


class GUI():
    def __init__(self, window):
        self.window = window
        self.draw_list = []
        width, height = self.window.get_viewport_size()
        spacing = frame_spacing(height)
        self.menu = Menu(spacing, spacing, font_normal(height))

        self.init_content()

    def init_content(self):
        width, height = self.window.get_viewport_size()

        self.header = Label("", anchor_x="left", anchor_y="top")

        self.display = Label(
            "", anchor_x="left", anchor_y="top", multiline=True)
        self.printer = Printer("", anchor_x="left", anchor_y="bottom")

        self.battle_gui = BattleGUI()

        self.draw_list.append(self.header)
        self.draw_list.append(self.printer)
        self.draw_list.append(self.display)
        self.draw_list.append(self.battle_gui)

        self.resize(width, height)

    def resize(self, width, height):
        self.header.x = frame_spacing(height)
        self.header.y = height - frame_spacing(height)
        self.header.font_size = font_big(height)

        self.display.x = frame_spacing(height)
        self.display.y = height - frame_spacing(height)
        self.display.font_size = font_normal(height)
        self.display.width = width // 2

        x = y = frame_spacing(height)
        font_size = font_normal(height)
        row_size = font_size + font_spacing(font_size)
        self.menu.resize(x, y, font_size)
        self.printer.resize(x, y + 3 * row_size, font_size)

        x = frame_spacing(height)
        y = height - frame_spacing(height)
        w = width - 2 * frame_spacing(height)
        h = height // 2 - frame_spacing(height)
        self.battle_gui.resize(x, y, w, h, font_size)

    def draw(self):
        for label in self.draw_list:
            label.draw()
        self.menu.draw()

    def set_output(self, outputs):
        if type(outputs) is str:
            self.printer.set_text(outputs)
        strings = []
        for message in outputs:
            if type(message) is str:
                strings.append(message)
                continue
            if type(message) is list:
                message = "\n".join(message)
            strings.append(message)
        self.printer.set_text("\n".join(strings))

    def has_output(self):
        return len("\n".join(self.printer.strings)) > 0

    def update(self, dt):
        """Called at a regular interval to animate labels etc."""
        self.menu.update(dt)
        self.printer.update(dt)

    def refresh(self):
        """After an enter click, we need to show/hide some elements"""
        if self.has_output():
            self.menu.display = False
        else:
            self.menu.display = True

    def reset_labels(self):
        self.header.text = ""
        self.display.text = ""

    def main_menu(self):
        self.reset_labels()
        self.battle_gui.hide()
        if not self.has_output():
            self.header.text = "MRPG Prototype"

    def game_menu(self, player):
        self.reset_labels()
        self.battle_gui.hide()
        if not self.has_output():
            self.display.text = player.string_long()

    def battle(self, battle):
        self.reset_labels()
        if battle:
            self.battle_gui.refresh(battle)
        else:
            self.battle_gui.hide()
