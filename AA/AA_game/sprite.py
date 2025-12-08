from __future__ import annotations
import pygame, os
from enum import Enum
from AA.AA_utils import misc, settings, countries, fontManager, timer
from AA.AA_game import healthBar, animations


class Sprite:

    def __init__(self, playerID: int, name: str,
                 country: countries.CountryOptions,
                 playerHalf: pygame.Surface):
        self._playerID = playerID
        self._playerHalf = playerHalf
        self._characterMidtop = settings.SPRITE_BASE_POS

        self._targetPos = self._characterMidtop
        self._travelInitialPos = (0, 0)
        self._travelTimeLength = 0.0
        self._travelStep = (0, 0)
        self._travelTimer = timer.Timer()

        self._animationManager = animations.AnimationManager()
        self._currentAnimation = self._animationManager.getAnimation(
            animations.PlayerAnimations.STAND, playerID)

        self._spriteSurface = pygame.Surface(
            (settings.SPRITE_SIZE[0] + 100, settings.SPRITE_SIZE[1] + 100),
            pygame.SRCALPHA)

        self._country = countries.getCountryFlagSurface(country)
        self._name = fontManager.upheaval(name, 30, (255, 255, 255))

        self._healthBar = healthBar.HealthBar(playerID, self._spriteSurface)

    @property
    def currentAnimation(self):
        return self._currentAnimation

    def setAnimation(self, newAnimation: animations.PlayerAnimations,
                     changeSides: bool):
        playerID = self._playerID
        if changeSides:
            if playerID == 0:
                playerID = 1
            else:
                playerID = 0

        self._currentAnimation = self._animationManager.getAnimation(
            newAnimation, playerID)
        self._currentAnimation.startAnimation(True)

    def moveTo(self, targetMidtop: tuple[int, int], travelTime: float):
        if travelTime == 0:
            self._characterMidtop = targetMidtop
            self._travelTimer.stop()
            return
        self._targetPos = targetMidtop
        self._travelTimeLength = travelTime
        xStep = (targetMidtop[0] - self._characterMidtop[0]) / travelTime
        yStep = (targetMidtop[1] - self._characterMidtop[1]) / travelTime
        self._travelStep = (xStep, yStep)
        self._travelInitialPos = self._characterMidtop
        self._travelTimer.restart()

    def _updateTravel(self):
        elapsed = self._travelTimer.elapsed()
        if elapsed >= self._travelTimeLength:
            self._travelTimer.stop()
            self._characterMidtop = self._targetPos
        else:
            newX = self._travelInitialPos[0] + int(
                self._travelStep[0] * elapsed)
            newY = self._travelInitialPos[1] + int(
                self._travelStep[1] * elapsed)
            self._characterMidtop = (newX, newY)

    def update(self, health: int):
        if self._travelTimer.isRunning():
            self._updateTravel()

        self._spriteSurface.fill((0, 0, 0, 0))
        self._healthBar.update(health)

        self._currentAnimation.update()
        character = self._currentAnimation.getCurrentFrame()
        self._spriteSurface.blit(
            character,
            character.get_rect(midtop=(self._spriteSurface.get_width() / 2,
                                       50)))
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
