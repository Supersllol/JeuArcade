from __future__ import annotations

import pygame, os
from AA.AA_utils import settings


def upheaval(text: str, size: int, color: str | tuple[int, int, int]):
    return pygame.font.Font(
        os.path.join(settings.PARENT_PATH, "AA_fonts/upheavtt.ttf"),
        size).render(text, True, color)
