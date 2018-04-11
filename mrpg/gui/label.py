import pyglet

from mrpg.gui.commons import FONT_SIZE, Color


class Label(pyglet.text.Label):
    def __init__(self, *args, **kwargs):
        defaults = dict(
            font_name=["Ubuntu Mono", "Consolas"],
            font_size=FONT_SIZE,
            anchor_x="left",
            anchor_y="bottom",
            color=Color.WHITE)
        for key in defaults:
            if key not in kwargs:
                kwargs[key] = defaults[key]
        self.label = pyglet.text.Label(*args, **kwargs)

        self.animation_speed = 200
        self.start_x = self.label.x
        self.travel_distance = 20
        self.offset_x = 0
        self.selected = False

    def draw(self):
        self.label.draw()

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
        self.x = self.start_x + self.offset_x
        self.label.x = int(self.x)
