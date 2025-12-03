from __future__ import annotations
import pygame
from AA.AA_utils import fontManager, misc


class ChiBar:

    def __init__(self, playerID: int, playerHalf: pygame.Surface):
        self._playerID = playerID
        self._playerHalf = playerHalf

        self._txtChi = fontManager.upheaval("CHI", 26, "white")
        self._bar = pygame.Surface((300, 50), pygame.SRCALPHA)

    def update(self, currentChi: int):
        self._bar.fill("#FFFFFF")

        txtCurrentChi = fontManager.upheaval(str(currentChi), 26, "white")

        misc.placeSurfaceInHalf(self._playerID, self._bar, self._playerHalf,
                                (300, 702))
        misc.placeSurfaceInHalf(self._playerID, self._txtChi, self._playerHalf,
                                (65, 700))
        misc.placeSurfaceInHalf(self._playerID, txtCurrentChi,
                                self._playerHalf, (65, 725))
