from __future__ import annotations

import pygame
from AA_utils.timer import Timer
from typing import List


class Scene:

    def __init__(self, mainApp: pygame.Surface):
        self._finished = False
        self._mainTimer = Timer()
        self._mainApp = mainApp

    def initScene(self):
        self._mainTimer.restart()

    def loopScene(self, events: List[pygame.event.Event],
                  joysticks: tuple[pygame.joystick.JoystickType,
                                   pygame.joystick.JoystickType | None]):
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if joysticks[0].get_button(4):
                    return False
        return True

    def getTransition(self):
        return Scene(pygame.Surface((0, 0)))

    @property
    def finished(self):
        return self._finished

    @finished.setter
    def finished(self, newVal: bool):
        self._finished = newVal
