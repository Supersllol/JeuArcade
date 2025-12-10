from __future__ import annotations
import pygame, os
from AA.AA_utils import fontManager, misc, settings, attackUtils, fontManager

sectionWidth = 75


class ChiBar:

    def __init__(self, playerID: int, playerHalf: pygame.Surface):
        self._playerID = playerID
        self._playerHalf = playerHalf

        self._txtTitleChi = fontManager.upheaval("CHI", 26, (255, 255, 255))
        self._txtTitleTotalChi = fontManager.upheaval("CHI TOTAL", 26,
                                                      (255, 255, 255))
        self._barOutline = pygame.image.load(
            os.path.join(settings.PARENT_PATH, "AA_images",
                         f"chi_{playerID}.png")).convert_alpha()
        self._barSurface = pygame.Surface((350, 80))

        self._xPosThresholds = [100, 175, 250, 310]
        self._attackChiThresholds: list[int]

    def setChiThresholds(self, thresholds: dict[attackUtils.AttackType, int]):
        self._attackChiThresholds = list(thresholds.values())

    def calculateProgressBarX(self, currentChi: int):
        for id, threshold in enumerate(self._attackChiThresholds):
            if id == len(self._attackChiThresholds) - 1:
                if currentChi >= threshold:
                    return self._barOutline.get_width()

            if currentChi > threshold:
                continue

            if currentChi == threshold:
                return (id + 1) * sectionWidth

            if id == 0:
                previousThreshold = 0
            else:
                previousThreshold = self._attackChiThresholds[id - 1]
            relPos = (currentChi - previousThreshold) / (threshold -
                                                         previousThreshold)
            return int(id * sectionWidth + relPos * sectionWidth)
        return 0

    def update(self, currentChi: int, totalChi: int):
        self._barSurface.fill((0, 0, 0))

        pygame.draw.rect(self._barSurface, (255, 255, 255), [25, 0, 300, 50])

        progressX = self.calculateProgressBarX(currentChi)
        start = 25 if self._playerID == 0 else 325 - progressX
        pygame.draw.rect(self._barSurface, (22, 203, 235),
                         [start, 0, progressX, 50])

        self._barSurface.blit(
            self._barOutline,
            self._barOutline.get_rect(
                midtop=self._barSurface.get_rect().midtop))

        for i in range(4):
            threshold = self._attackChiThresholds[i]
            color = (255, 255, 255) if currentChi < threshold else (255, 204,
                                                                    37)
            txt = fontManager.upheaval(str(threshold), 13, color)
            misc.placeSurfaceInHalf(self._playerID, txt, self._barSurface,
                                    (self._xPosThresholds[i], 53))

        txtCurrentChi = fontManager.upheaval(str(currentChi), 26,
                                             (255, 255, 255))
        txtTotalChi = fontManager.upheaval(str(totalChi), 26, (255, 255, 255))

        misc.placeSurfaceInHalf(self._playerID, self._barSurface,
                                self._playerHalf, (335, 690))
        misc.placeSurfaceInHalf(self._playerID, self._txtTitleChi,
                                self._playerHalf, (100, 700))
        misc.placeSurfaceInHalf(self._playerID, txtCurrentChi,
                                self._playerHalf, (100, 725))
        misc.placeSurfaceInHalf(self._playerID, self._txtTitleTotalChi,
                                self._playerHalf, (100, 20))
        misc.placeSurfaceInHalf(self._playerID, txtTotalChi, self._playerHalf,
                                (100, 45))
