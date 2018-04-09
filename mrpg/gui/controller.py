from mrpg.core.game import Game
from mrpg.gui.renderer import Renderer
from mrpg.gui import wrapper


class Controller():
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        window = wrapper.init(self, width, height, caption="MRPG")
        self.game = Game()
        self.renderer = Renderer(self, window)

    def run(self):
        wrapper.run()

    def draw(self):
        self.renderer.render()

    def update(self, dt):
        pass

    def mouse_motion(self, x, y, dx, dy):
        pass

    def mouse_press(self, x, y, button, modifiers):
        pass

    def mouse_release(self, x, y, button, modifiers):
        pass

    def mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass
