from __future__ import annotations
import pygame
from AA.AA_utils import misc


class HealthBar:

    def __init__(self, playerID: int, playerHalf: pygame.Surface):
        self._playerID = playerID
        self._playerHalf = playerHalf

        self._bar = pygame.Surface((150, 30), pygame.SRCALPHA)

    def _drawHealthBars(self, health: int):
        """Draw green rectangles on self._bar to represent health (0-10 scale).
        Each rectangle represents 1 health point, centered on the surface.
        health: integer from 0 to 10
        """
        # Clear the surface first
        self._bar.fill((0, 0, 0))

        bar_width = self._bar.get_width()
        bar_height = self._bar.get_height()

        # Calculate dimensions for rectangles and gaps
        rect_width = 11
        rect_height = 18
        gap = 3
        total_width = (rect_width * 10) + (gap * 9
                                           )  # 10 rects + 9 gaps between them

        # Calculate starting X to center the entire bar
        start_x = (bar_width - total_width) // 2

        # Draw green rectangles (one per health point)
        for i in range(health):
            x = start_x + (i * (rect_width + gap))
            rect = pygame.Rect(
                x,
                (bar_height - rect_height) // 2,  # Center vertically too
                rect_width,
                rect_height)
            pygame.draw.rect(self._bar, (0, 255, 64), rect)

        # Optional: draw a border around the entire bar
        pygame.draw.rect(self._bar, (0, 0, 0), (0, 0, bar_width, bar_height),
                         2)

    def update(self, health: int, spriteMidTop: tuple[int, int]):
        self._drawHealthBars(health)

        misc.placeSurfaceInHalf(self._playerID, self._bar, self._playerHalf,
                                (spriteMidTop[0], spriteMidTop[1] - 40))
