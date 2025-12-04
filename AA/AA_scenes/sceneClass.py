from __future__ import annotations

import pygame

from AA.AA_utils import timer, inputManager, musicManager


# Base class representing a game scene/state.
# Subclasses implement initScene(), loopScene() and optionally getTransition().
class Scene:

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager,
                 musicManager: musicManager.MusicManager):
        # Reference to the main drawing surface (window / screen)
        self._mainApp = mainApp

        # Flag indicating whether this scene has finished and should transition
        self._finished = False
        # Timer used to track time spent in the current scene / state
        self._stateTimer = timer.Timer()
        # Shared input manager instance (keyboard / joystick abstraction)
        self._inputManager = inputManager
        # Shared input manager instance (audio abstraction)
        self._musicManager = musicManager

    def initScene(self):
        # Called once when the scene becomes active — reset internal timer.
        self._stateTimer.restart()

    def loopScene(self, events: list[pygame.event.Event]):
        # Parent loop. Should be called after the child loop to update the button
        # states and check if user requested to exit program. Children loop should only
        # return whatever value this parent loop returns.
        for i in range(2):
            newPresses = self._inputManager.getBtnsPressed(i)
            # If the SELECT logical button was newly pressed, signal to stop loop
            if inputManager.ButtonInputs.SELECT in newPresses:
                return False
            # Debug: print any new button presses
            # if newPresses: print(f"{i} : {newPresses}")

        for i in range(2):
            newAxes = self._inputManager.getAxesActive(i)
            # Debug: print any newly active axes
            # if newAxes: print(f"{i} : {newAxes}")

        # Update input manager snapshot AFTER processing inputs so that
        # getBtnsPressed/getAxesActive detect rising edges relative to the
        # previously-stored state. Call once per frame.
        self._inputManager.update()
        return True

    def getTransition(self) -> Scene | None:
        # Override in subclasses to return the next scene when finished.
        return None

    def fadeinScene(self, startime: float = 0.0):
        # Fade-in effect when scene starts
        self._stateTimer.start()
        blackmask = pygame.Surface(self._mainApp.get_size())
        blackmask = blackmask.convert()
        alpha = 255 - min(255, int((self._stateTimer.elapsed()) * 255))
        blackmask.fill((0, 0, 0))
        blackmask.set_alpha(alpha)
        self._mainApp.blit(blackmask, (0, 0))

    def fadeoutScene(self):
        # Fade-out effect when scene ends
        self._stateTimer.start()
        blackmask = pygame.Surface(self._mainApp.get_size())
        blackmask = blackmask.convert()
        alpha = min(255, int((self._stateTimer.elapsed()) * 255))
        print(self._stateTimer.elapsed())
        blackmask.fill((0, 0, 0))
        blackmask.set_alpha(alpha)
        self._mainApp.blit(blackmask, (0, 0))

    @property
    def finished(self):
        return self._finished

    @finished.setter
    def finished(self, newVal: bool):
        self._finished = newVal
