from __future__ import annotations
import pygame, os
from enum import Enum
from AA.AA_utils import misc, settings, countries, fontManager
from AA.AA_game import healthBar


class Frame:

    def __init__(self, relativePos: tuple[int, int], imageName: str):
        self._relativePos = relativePos
        self._imageName = imageName


class PlayerAnimations(Enum):
    STAND_IDLE = [Frame((0, 0), "")]


class Sprite:

    def __init__(self, playerID: int, name: str,
                 country: countries.CountryOptions,
                 playerHalf: pygame.Surface):
        self._playerID = playerID
        self._playerHalf = playerHalf
        self._characterMidtop = (120, 275)

        self._character = pygame.transform.scale(
            pygame.image.load(
                os.path.join(settings.PARENT_PATH, "AA_images/P0-face.png")),
            settings.SPRITE_SIZE)

        self._spriteSurface = pygame.Surface(
            (settings.SPRITE_SIZE[0] + 100, settings.SPRITE_SIZE[1] + 100),
            pygame.SRCALPHA)

        self._country = countries.getCountryFlagSurface(country)
        self._name = fontManager.upheaval(name, 30, (255, 255, 255))

        self._healthBar = healthBar.HealthBar(playerID, self._spriteSurface)

    def update(self, health: int):
        self._spriteSurface.fill((0, 0, 0, 0))
        self._healthBar.update(health)
        self._spriteSurface.blit(
            self._character,
            self._character.get_rect(midtop=(self._spriteSurface.get_width() /
                                             2, 50)))
        self._spriteSurface.blit(
            self._country,
            self._country.get_rect(
                center=(self._spriteSurface.get_width() / 2 - 35,
                        self._spriteSurface.get_height() - 25)))
        self._spriteSurface.blit(
            self._name,
            self._name.get_rect(
                center=(self._spriteSurface.get_width() / 2 + 35,
                        self._spriteSurface.get_height() - 25)))

        misc.placeSurfaceInHalf(self._playerID, self._spriteSurface,
                                self._playerHalf, self._characterMidtop)
