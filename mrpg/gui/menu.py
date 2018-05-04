from mrpg.gui.commons import SPACING, FRAME_SPACING, FONT_SIZE
from mrpg.gui.label import MenuLabel


class Menu:
    def __init__(self, x=FRAME_SPACING, y=FRAME_SPACING):
        self._strings = []
        self.background = None
        self._labels = []
        self._length = 0
        self.index = 0
        self.x = x
        self.y = y

    def choices(self, *args):
        inv_index = len(self._labels) - self.index
        for arg in args:
            assert type(arg) is str
        strings = args
        labels = []

        ROW_SIZE = FONT_SIZE + SPACING
        y = len(strings) * (ROW_SIZE)
        for s in strings:
            y -= ROW_SIZE
            s = s[0].upper() + s[1:]
            label = MenuLabel(s, x=self.x, y=self.y + y)
            labels.append(label)

        length = len(labels)
        index = length - inv_index
        if index < 0:
            index = 0

        self._length = length
        self._strings = strings
        self._labels = labels
        self.index = index

    def draw(self):
        for label in self._labels:
            label.draw()

    def update(self, dt):
        if self.index is None and len(self._labels) > 0:
            self.index = 0
        if self.index >= len(self._labels):
            self.index = 0
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

    def pick(self):
        return self.selected()
