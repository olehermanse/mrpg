"""Create a pyglet window and attach appropriate callbacks"""
import pyglet
from pyglet.window import mouse, key

controller = None
window = None

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


def update(dt):
    controller.update(dt)


def run():
    pyglet.app.run()


def init(ctrl, w, h, caption=None):
    global window
    global controller
    controller = ctrl
    window = pyglet.window.Window(w, h, resizable=True)
    if caption:
        window.set_caption(caption)
    pyglet.clock.schedule_interval(update, 0.01)

    # Event callbacks need to be registered here because of the window object:

    @window.event
    def on_draw():
        controller.draw()

    @window.event
    def on_resize(width, height):
        print('The window was resized to {}x{}'.format(width, height))

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        controller.mouse_motion(x, y, dx, dy)

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        controller.mouse_press(x, y, button, modifiers)

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        controller.mouse_release(x, y, button, modifiers)

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        controller.mouse_drag(x, y, dx, dy, buttons, modifiers)

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol in key_map:
            controller.key_press(key_map[symbol])
            return pyglet.event.EVENT_HANDLED

    @window.event
    def on_key_release(symbol, modifiers):
        pass

    @window.event
    def on_text(text):
        pass

    @window.event
    def on_text_motion(text):
        pass

    return window
