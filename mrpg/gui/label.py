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
