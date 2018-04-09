"""Create a pyglet window and attach appropriate callbacks"""
import pyglet
from pyglet.window import mouse

controller = None
window = None


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

    def get_button(button):
        if type(button) is list:
            buttons = []
            for btn in button:
                buttons.append(get_button(btn))
            return btn
        if button == mouse.LEFT:
            return 1
        if button == mouse.RIGHT:
            return 2
        if button == mouse.MIDDLE:
            return 3

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        controller.mouse_press(x, y, get_button(button), modifiers)

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        controller.mouse_release(x, y, get_button(button), modifiers)

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        controller.mouse_drag(x, y, dx, dy, get_button(buttons), modifiers)

    return window
