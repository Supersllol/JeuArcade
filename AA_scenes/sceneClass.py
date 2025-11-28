from __future__ import annotations

import pygame
from AA_utils import settings, timer, inputManager
from typing import List, Optional


# Base class representing a game scene/state.
# Subclasses implement initScene(), loopScene() and optionally getTransition().
class Scene:

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager):
        # Reference to the main drawing surface (window / screen)
        self._mainApp = mainApp

        # Flag indicating whether this scene has finished and should transition
        self._finished = False
        # Timer used to track time spent in the current scene / state
        self._stateTimer = timer.Timer()
        # Shared input manager instance (keyboard / joystick abstraction)
        self._inputManager = inputManager

    def initScene(self):
        # Called once when the scene becomes active — reset internal timer.
        self._stateTimer.restart()

    def loopScene(self, events: List[pygame.event.Event]):
        # Parent loop. Should be called after the child loop to update the button
        # states and check if user requested to exit program. Children loop should only
        # return whatever value this parent loop returns.
        for i in range(2):
            newPresses = self._inputManager.getBtnsPressed(i)
            # If the SELECT logical button was newly pressed, signal to stop loop
            if inputManager.ButtonInputs.SELECT in newPresses:
                return False
            # Debug: print any new button presses
            if newPresses: print(f"{i} : {newPresses}")

        for i in range(2):
            newAxes = self._inputManager.getAxesActive(i)
            # Debug: print any newly active axes
            if newAxes: print(f"{i} : {newAxes}")

        # Update input manager snapshot AFTER processing inputs so that
        # getBtnsPressed/getAxesActive detect rising edges relative to the
        # previously-stored state. Call once per frame.
        self._inputManager.update()
        return True

    def getTransition(self) -> Optional[Scene]:
        # Override in subclasses to return the next scene when finished.
        return None

    @property
    def finished(self):
        return self._finished

    @finished.setter
    def finished(self, newVal: bool):
        self._finished = newVal
