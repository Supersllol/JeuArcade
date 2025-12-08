from __future__ import annotations

import pygame, os
from AA.AA_utils import settings

upheavalMemory: dict[tuple[str, int, tuple[int, int, int]],
                     pygame.Surface] = {}


def upheaval(text: str, size: int, color: tuple[int, int, int]):
    if (text, size, color) not in upheavalMemory:
        upheavalMemory[(text, size, color)] = pygame.font.Font(
            os.path.join(settings.PARENT_PATH, "AA_fonts/upheavtt.ttf"),
            size).render(text, True, color)

    return upheavalMemory[(text, size, color)]
