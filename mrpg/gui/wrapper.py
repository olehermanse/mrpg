"""Create a pyglet window and attach appropriate callbacks"""
import pyglet
from pyglet.window import mouse, key

key_map = {
    key.MOTION_UP: "up",
    key.MOTION_DOWN: "down",
    key.MOTION_LEFT: "left",
    key.MOTION_RIGHT: "right",
    key.W: "up",
    key.A: "left",
    key.S: "down",
    key.D: "right",
    key.ENTER: "enter",
    key.ESCAPE: "escape"
}

def run():
    pyglet.app.run()

class GameWindow(pyglet.window.Window):
    def __init__(self, w, h, controller):
        super().__init__(
            w, h, caption='MRPG', resizable=True)
        self.ratio = w / h
        self.controller = controller
        self.set_minimum_size(w // 2, h // 2)

        pyglet.clock.schedule_interval(self.update, 0.01)

    def update(self, dt):
        self.controller.update(dt)

    def on_resize(self, w, h):
        w = int(self.ratio * h)  # Locked aspect ratio
        self.width = w
        self.height = h

        # Don't use window dimensions for coordinate system, use viewport:
        width, height = self.get_viewport_size() # May be scaled (on mac)

        # Resize viewport (only necessary on windows):
        pyglet.gl.glViewport(0, 0, max(1, width), max(1, height))

        self.controller.resize(width, height)
        return pyglet.event.EVENT_HANDLED

    def on_draw(self):
        self.clear()

        # Use viewport size to set the coordinate system:
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        width, height = self.get_viewport_size()
        pyglet.gl.glOrtho(0, width, 0, height, -1, 1)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
        # The glOrtho call is necessary for high resolution mac font rendering

        self.controller.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.controller.mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        self.controller.mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.controller.mouse_release(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.controller.mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_key_press(self, symbol, modifiers):
        if symbol in key_map:
            self.controller.key_press(key_map[symbol])
            return pyglet.event.EVENT_HANDLED

    def on_key_release(self, symbol, modifiers):
        pass

    def on_text(self, text):
        pass

    def on_text_motion(self, text):
        pass


def init(controller, w, h, caption=None):
    window = GameWindow(w, h, controller)
    if caption:
        window.set_caption(caption)

    return window
