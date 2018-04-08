"""Renders the state of a game and controller object using pyglet"""

import pyglet


class Renderer():
    def __init__(self, controller, window):
        self.controller = controller
        self.window = window
        cursor = window.get_system_mouse_cursor("crosshair")
        window.set_mouse_cursor(cursor)

    def render(self):
        self.window.clear()
        pyglet.gl.glClearColor(255, 255, 255, 255)
