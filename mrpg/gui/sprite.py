import pyglet


class Sprite(pyglet.sprite.Sprite):
    """Sprite which scales using nearest neighbor filter"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pyglet.gl.glTexParameteri(
            self._texture.target, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST
        )
        pyglet.gl.glTexParameteri(
            self._texture.target, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST
        )
