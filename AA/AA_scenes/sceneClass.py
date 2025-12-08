from __future__ import annotations

import pygame

from AA.AA_utils import timer, inputManager, musicManager, dbManager


# Base class representing a game scene/state.
# Subclasses implement initScene(), loopScene() and optionally getTransition().
class Scene:

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager,
                 musicManager: musicManager.MusicManager,
                 dbManager: dbManager.DatabaseManager):
        # Reference to the main drawing surface (window / screen)
        self._mainApp = mainApp

        # Flag indicating whether this scene has finished and should transition
        self._sceneFinished = False
        # Timer used to track time spent in the current scene / state
        self._stateTimer = timer.Timer()

        self._fadeTimer = timer.Timer()
        self._fadeInFinished = False
        self._blackMask = pygame.Surface(mainApp.get_size(), pygame.SRCALPHA)
        # Shared input manager instance (keyboard / joystick abstraction)
        self._inputManager = inputManager
        # Shared input manager instance (audio abstraction)
        self._musicManager = musicManager

        self._dbManager = dbManager

    def initScene(self):
        # Called once when the scene becomes active — reset internal timer.
        self._stateTimer.restart()
        self._fadeTimer.restart()
        self.fadeinScene()

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

        if not self._fadeInFinished:
            self.fadeinScene()

        # Update input manager snapshot AFTER processing inputs so that
        # getBtnsPressed/getAxesActive detect rising edges relative to the
        # previously-stored state. Call once per frame.
        self._inputManager.update()
        return True

    def getTransition(self) -> Scene | None:
        # Override in subclasses to return the next scene when finished.
        return None

    def fadeinScene(self):
        # Fade-in effect when scene starts
        if self._fadeTimer.elapsed() >= 1:
            self._fadeInFinished = True
            self._fadeTimer.stop()
            return
        self._fadeTimer.start()
        alpha = 255 - min(255, int((self._fadeTimer.elapsed()) * 255))
        self._blackMask.fill((0, 0, 0, alpha))
        self._mainApp.blit(self._blackMask, (0, 0))

    def fadeoutScene(self):
        """Returns true when fadeout is finished"""
        # Fade-out effect when scene ends
        self._fadeTimer.start()
        alpha = min(255, int((self._fadeTimer.elapsed()) * 255))
        self._blackMask.fill((0, 0, 0, alpha))
        self._mainApp.blit(self._blackMask, (0, 0))
        return self._fadeTimer.elapsed() >= 1

    @property
    def sceneFinished(self):
        return self._sceneFinished

    @sceneFinished.setter
    def sceneFinished(self, newVal: bool):
        self._sceneFinished = newVal
