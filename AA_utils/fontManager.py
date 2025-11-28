import pygame
from AA_utils import settings
import os


def upheaval(text: str, size: int, color: str | tuple[int, int, int]):
    return pygame.font.Font(
        os.path.join(settings.PARENT_PATH, "AA_fonts/upheavtt.ttf"),
        size).render(text, True, color)
