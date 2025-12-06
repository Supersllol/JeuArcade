from __future__ import annotations
import pygame
from AA.AA_utils import fontManager, misc


class ChiBar:

    def __init__(self, playerID: int, playerHalf: pygame.Surface):
        self._playerID = playerID
        self._playerHalf = playerHalf

        self._txtTitleChi = fontManager.upheaval("CHI", 26, (255, 255, 255))
        self._txtTitleTotalChi = fontManager.upheaval("TOTAL CHI", 26,
                                                      (255, 255, 255))
        self._bar = pygame.Surface((300, 50), pygame.SRCALPHA)

    def update(self, currentChi: int, totalChi: int):
        self._bar.fill((255, 255, 255))

        txtCurrentChi = fontManager.upheaval(str(currentChi), 26,
                                             (255, 255, 255))
        txtTotalChi = fontManager.upheaval(str(totalChi), 26, (255, 255, 255))

        misc.placeSurfaceInHalf(self._playerID, self._bar, self._playerHalf,
                                (300, 702))
        misc.placeSurfaceInHalf(self._playerID, self._txtTitleChi,
                                self._playerHalf, (65, 700))
        misc.placeSurfaceInHalf(self._playerID, txtCurrentChi,
                                self._playerHalf, (65, 725))
        misc.placeSurfaceInHalf(self._playerID, self._txtTitleTotalChi,
                                self._playerHalf, (100, 20))
        misc.placeSurfaceInHalf(self._playerID, txtTotalChi, self._playerHalf,
                                (100, 45))
