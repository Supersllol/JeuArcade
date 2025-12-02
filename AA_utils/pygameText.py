import pygame


class PygameText:

    def __init__(self, text: pygame.Surface, position: pygame.Rect):
        self._text = text
        self._position = position

    @property
    def text(self):
        return self._text

    @property
    def position(self):
        return self._position
