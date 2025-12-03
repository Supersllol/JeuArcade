import pygame
from enum import Enum
from AA.AA_utils import misc, settings
from AA.AA_game import healthBar
import os


class Frame:

    def __init__(self, relativePos: tuple[int, int], imageName: str):
        self._relativePos = relativePos
        self._imageName = imageName


class PlayerAnimations(Enum):
    STAND_IDLE = [Frame((0, 0), "")]


class Sprite:

    def __init__(self, playerID: int, playerHalf: pygame.Surface):
        self._playerID = playerID
        self._playerHalf = playerHalf
        self._midtop = (120, 350)

        self._healthBar = healthBar.HealthBar(playerID, self._playerHalf)

        self._sprite = pygame.transform.scale(
            pygame.image.load(
                os.path.join(settings.PARENT_PATH, "AA_images/P0-face.png")),
            (300, 300))

    def update(self, health: int):
        self._healthBar.update(health, self._midtop)

        misc.placeSurfaceInHalf(self._playerID, self._sprite, self._playerHalf,
                                self._midtop)
