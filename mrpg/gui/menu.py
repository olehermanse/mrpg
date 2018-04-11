from mrpg.gui.commons import SPACING, FRAME_SPACING, FONT_SIZE
from mrpg.gui.label import Label

class Menu:
    def __init__(self):
        self._strings = []
        self.background = None
        self._labels = []
        self._length = 0
        self.index = 0

    def choices(self, *args):
        for arg in args:
            assert type(arg) is str
        strings = args
        self._strings = strings
        self._labels = []
        if not strings:
            return

        labels = self._labels
        ROW_SIZE = FONT_SIZE + SPACING
        y = len(strings) * (ROW_SIZE)
        for s in strings:
            y -= ROW_SIZE
            label = Label(s, x=FRAME_SPACING, y=FRAME_SPACING + y)
            labels.append(label)
        self._length = len(labels)

    def draw(self):
        for label in self._labels:
            label.draw()

    def update(self, dt):
        for index, label in enumerate(self._labels):
            if index == self.index:
                label.selected = True
            else:
                label.selected = False
            label.update(dt)

    def selected(self):
        try:
            return self._strings[self.index]
        except IndexError:
            return None

    def down(self):
        if self.index < self._length - 1:
            self.index += 1

    def up(self):
        if self.index > 0:
            self.index -= 1
