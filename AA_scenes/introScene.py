from __future__ import annotations

from AA_scenes import sceneClass, homeScene
import pygame
from typing import List


class IntroScene(sceneClass.Scene):

    def __init__(self, mainApp: pygame.Surface):
        super().__init__(mainApp)

    def initScene(self):
        super().initScene()

    def loopScene(self, events: List[pygame.event.Event],
                  joysticks: tuple[pygame.joystick.JoystickType,
                                   pygame.joystick.JoystickType | None]):
        self._mainApp.fill((255, 255, 255))

        if joysticks[0].get_button(1):
            self.finished = True
        return super().loopScene(events, joysticks)

    def getTransition(self):
        return homeScene.HomeScene(self._mainApp)
