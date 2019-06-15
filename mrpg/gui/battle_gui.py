import pyglet

from mrpg.gui.label import Label


class ResourceBar:
    def __init__(self, color):
        self.label = Label("", anchor_x="left", anchor_y="center")
        self.background = None
        self.color = color
        self.fraction = 1.0

    def resize(self, x, y, w, h, font_size):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label.x = x + w // 32
        self.label.y = y - h // 2
        self.label.w = w
        self.label.h = h
        self.label.font_size = font_size
        r, g, b = self.color
        color = r, g, b
        f = self.fraction
        self.foreground = pyglet.graphics.vertex_list(
            4, ('v2f', (x, y, x + w * f, y, x + w * f, y - h, x, y - h)),
            ('c3B', (*color, *color, *color, *color)))
        self.border = pyglet.graphics.vertex_list(
            4, ('v2f', (x, y, x + w, y, x + w, y - h, x, y - h)),
            ('c3B', (*color, *color, *color, *color)))
        r, g, b = r // 3, g // 3, b // 3
        color = r, g, b
        self.background = pyglet.graphics.vertex_list(
            4, ('v2f', (x, y, x + w, y, x + w, y - h, x, y - h)),
            ('c3B', (*color, *color, *color, *color)))

    def refresh(self, current, max):
        self.label.text = f"{current}/{max}"
        self.fraction = current / max
        color = self.color
        f = self.fraction
        x, y, w, h = self.x, self.y, self.w, self.h
        self.foreground = pyglet.graphics.vertex_list(
            4, ('v2f', (x, y, x + w * f, y, x + w * f, y - h, x, y - h)),
            ('c3B', (*color, *color, *color, *color)))

    def draw(self):
        if self.background:
            self.background.draw(pyglet.gl.GL_QUADS)
        if self.foreground:
            self.foreground.draw(pyglet.gl.GL_QUADS)
        if self.border:
            self.border.draw(pyglet.gl.GL_LINE_LOOP)
        if self.label:
            self.label.draw()


class CreatureGUI:
    def __init__(self):
        self.name = Label("", anchor_x="left", anchor_y="top")
        self.level = Label("", anchor_x="right", anchor_y="top")
        self.str = Label("", anchor_x="left", anchor_y="top")
        self.dex = Label("", anchor_x="center", anchor_y="top")
        self.int = Label("", anchor_x="right", anchor_y="top")
        self.hp = ResourceBar((0, 128, 0))
        self.mp = ResourceBar((0, 0, 128))

    def resize(self, x, y, w, h, font_size):
        self.name.x = x
        self.name.y = y
        self.name.font_size = font_size
        self.level.x = x + w
        self.level.y = y
        self.level.font_size = font_size
        small_font = int(font_size * 0.7)
        self.str.font_size = small_font
        self.dex.font_size = small_font
        self.int.font_size = small_font
        row_size = 1.5 * font_size
        self.hp.resize(x, y - row_size, w, font_size, small_font)
        self.mp.resize(x, y - 2 * row_size, w, font_size, small_font)
        self.str.x = x + w // 32
        self.dex.x = x + w // 2
        self.int.x = x + w - w // 32
        self.str.y = self.dex.y = self.int.y = y - 3 * row_size

    def draw(self):
        self.name.draw()
        self.level.draw()
        self.hp.draw()
        self.mp.draw()
        self.str.draw()
        self.dex.draw()
        self.int.draw()

    def refresh(self, creature):
        self.name.text = creature.name
        self.level.text = f"Lv. {creature.level}"
        current = creature.current
        base = creature.base
        self.hp.refresh(current["hp"], base["hp"])
        self.mp.refresh(current["mp"], base["mp"])
        self.str.text = f"str: {current['str']}/{base['str']}"
        self.dex.text = f"dex: {current['dex']}/{base['dex']}"
        self.int.text = f"int: {current['int']}/{base['int']}"


class BattleGUI:
    def __init__(self):
        self.enabled = False
        self.a = CreatureGUI()
        self.b = CreatureGUI()

    def resize(self, x, y, w, h, font_size):
        s = w // 20
        self.a.resize(x, y, w // 2 - s, h, font_size)
        self.b.resize(x + w // 2 + s, y, w // 2 - s, h, font_size)

    def draw(self):
        if self.enabled:
            self.a.draw()
            self.b.draw()

    def refresh(self, battle):
        self.enabled = True
        self.a.refresh(battle.a)
        self.b.refresh(battle.b)

    def hide(self):
        self.enabled = False
