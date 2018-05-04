import pyglet

from mrpg.gui.commons import FONT_SIZE, Color


class Label(pyglet.text.Label):
    def __init__(self, *args, **kwargs):
        defaults = dict(
            font_name=["Ubuntu Mono", "Consolas", "Menlo", "Monaco"],
            font_size=FONT_SIZE,
            anchor_x="left",
            anchor_y="bottom",
            color=Color.WHITE)
        for key in defaults:
            if key not in kwargs:
                kwargs[key] = defaults[key]
        super().__init__(*args, **kwargs)

    def draw(self):
        super().draw()

    def update(self, dt):
        pass


class TypingLabel(Label):
    def __init__(self, text, **kwargs):
        super().__init__("", **kwargs)
        self.y_float = float(self.y)
        self.set_text(text)
        self.delay = 0.02
        self.counter = 0.0
        self.done = False
        self.enabled = True

    def complete(self):
        self.text = self.final_text

    def is_done(self):
        return self.done

    def draw(self):
        super().draw()

    def set_text(self, text):
        self.final_text = text
        self.text = ""
        self.done = False

    def add_letter(self):
        if len(self.final_text) > len(self.text):
            self.text += self.final_text[len(self.text)]
        else:
            self.done = True

    def update(self, dt):
        if self.target_y is not None:
            if self.y < self.target_y:
                self.y_float += dt * 300
                if self.y_float > self.target_y:
                    self.y_float = self.target_y
                    self.target_y = None
            elif self.y > self.target_y:
                self.y_float -= dt * 300
                if self.y_float < self.target_y:
                    self.y_float = self.target_y
                    self.target_y = None
            else:
                self.y_float = self.y
                self.target_y = None
        self.y = int(self.y_float)
        if not self.enabled:
            return
        self.counter += dt
        if self.counter > self.delay:
            self.counter -= self.delay
            self.add_letter()


class Printer:
    def __init__(self, text, **kwargs):
        self.kwargs = kwargs
        self.spacing = 40
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.set_text(text)
        self.index = 0

    def set_text(self, text):
        self.strings = text.split("\n")
        self.labels = []
        y = self.y
        for string in self.strings:
            label = TypingLabel(string, **self.kwargs)
            label.y = y
            y -= self.spacing
            label.enabled = False
            self.labels.append(label)

    def draw(self):
        for label in self.labels:
            label.draw()

    def update(self, dt):
        enable = True
        self.index = None
        for index, label in enumerate(self.labels):
            label.enabled = enable
            if not label.is_done():
                enable = False
                if self.index is None:
                    self.index = index
        if self.index is not None and self.index > 6:
            self.index = None
            self.labels = self.labels[1:]
            self.strings = self.strings[1:]

        if len(self.strings) > 0 and self.strings[0].strip() == "":
            self.labels = self.labels[1:]
            self.strings = self.strings[1:]

        y = self.y
        for label in self.labels:
            label.target_y = y
            y -= self.spacing

        for label in self.labels:
            label.update(dt)


class MenuLabel(Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.animation_speed = 200
        self.start_x = self.x
        self.travel_distance = self.content_width / len(self.text)

        self.offset_x = 0
        self.selected = False

    def update(self, dt):
        if self.selected:
            if self.offset_x < self.travel_distance:
                self.offset_x += dt * self.animation_speed
            elif self.offset_x > self.travel_distance:
                self.offset_x = self.travel_distance
        else:
            if self.offset_x > 0:
                self.offset_x -= dt * self.animation_speed
            elif self.offset_x < 0:
                self.offset_x = 0
        new_x = self.start_x + self.offset_x
        self.x = int(new_x)
