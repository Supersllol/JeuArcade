from __future__ import annotations

from AA_scenes.sceneClass import Scene
from AA_utils import inputManager, musicManager
import pygame
from typing import List, Optional


class HomeScene(Scene):

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager,
                 musicManager: musicManager.MusicManager):
        super().__init__(mainApp, inputManager, musicManager)

    def initScene(self):
        super().initScene()

    def loopScene(self, events: List[pygame.event.Event]):
        # code appelé à chaque loop
        if inputManager.AxisInputs.X_LEFT in self._inputManager.getAxesActive(
                0):
            pass

        self._mainApp.fill((0, 0, 0))
        return super().loopScene(events)

    def getTransition(self):
        return super().getTransition()
