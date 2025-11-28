from __future__ import annotations

from AA_scenes import sceneClass, homeScene
from AA_utils import inputManager
import pygame
from typing import List, Optional


class IntroScene(sceneClass.Scene):

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager):
        super().__init__(mainApp, inputManager)

    def initScene(self):
        super().initScene()

    def loopScene(self, events: List[pygame.event.Event]):
        self._mainApp.fill((255, 255, 255))

        # if joysticks[0].get_button(1):
        #     self.finished = True
        return super().loopScene(events)

    def getTransition(self):
        return homeScene.HomeScene(self._mainApp, self._inputManager)
