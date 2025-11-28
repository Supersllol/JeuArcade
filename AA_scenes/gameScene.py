from __future__ import annotations

from AA_scenes.sceneClass import Scene
from AA_utils import settings, inputManager, fontManager
import pygame
from typing import List, Optional
from enum import Enum, auto
import os


class GameState(Enum):
    INITIAL_DELAY = auto(),
    START_COUNTDOWN = auto()


class GameScene(Scene):

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager):
        super().__init__(mainApp, inputManager)

        self._bgImage = pygame.image.load(
            os.path.join(settings.PARENT_PATH, "AA_images/dojo.jpg"))

    def initScene(self):
        super().initScene()

    def loopScene(self, events: List[pygame.event.Event]):
        self._mainApp.blit(
            self._bgImage,
            self._bgImage.get_rect(center=self._mainApp.get_rect().center))
        number3 = fontManager.upheaval("3", 60, "black")
        self._mainApp.blit(
            number3, number3.get_rect(center=self._mainApp.get_rect().center))

        return super().loopScene(events)

    def getTransition(self):
        return super().getTransition()
