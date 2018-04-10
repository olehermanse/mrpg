from mrpg.gui.commons import create_label, SPACING, FRAME_SPACING, FONT_SIZE


class Menu:
    def __init__(self):
        self._strings = []
        self.background = None
        self._labels = []
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
            label = create_label(s, x=FRAME_SPACING, y=FRAME_SPACING + y)
            labels.append(label)

    def draw(self):
        for label in self._labels:
            label.draw()

    def selected(self):
        try:
            return self._strings[self.index]
        except IndexError:
            return None
