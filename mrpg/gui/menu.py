from mrpg.gui.commons import font_spacing, frame_spacing
from mrpg.gui.label import MenuLabel


class Menu:
    def __init__(self, x, y, font_size):
        self._strings = []
        self.background = None
        self.font_size = font_size
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

        row_size = self.font_size + font_spacing(self.font_size)
        y = len(strings) * (row_size)
        for s in strings:
            y -= row_size
            s = s[0].upper() + s[1:]
            label = MenuLabel(
                8 * self.font_size,
                s,
                x=self.x,
                y=self.y + y,
                font_size=self.font_size)
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
