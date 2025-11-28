from __future__ import annotations

from AA_scenes.sceneClass import Scene
from AA_utils import inputManager
import pygame
from typing import List, Optional


class HomeScene(Scene):

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager):
        super().__init__(mainApp, inputManager)

    def initScene(self):
        super().initScene()

    def loopScene(self, events: List[pygame.event.Event]):
        self._mainApp.fill((0, 0, 0))
        return super().loopScene(events)

    def getTransition(self):
        return super().getTransition()
