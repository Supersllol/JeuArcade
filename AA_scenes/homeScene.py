from __future__ import annotations

from AA_scenes.sceneClass import Scene
import pygame
from typing import List


class HomeScene(Scene):

    def __init__(self, mainApp: pygame.Surface):
        super().__init__(mainApp)

    def initScene(self):
        super().initScene()

    def loopScene(self, events: List[pygame.event.Event],
                  joysticks: tuple[pygame.joystick.JoystickType,
                                   pygame.joystick.JoystickType | None]):
        self._mainApp.fill((0, 0, 0))
        return super().loopScene(events, joysticks)

    def getTransition(self):
        return super().getTransition()
