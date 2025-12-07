from __future__ import annotations

import pygame, os
from AA.AA_scenes import homeScene

from AA.AA_scenes.sceneClass import Scene
from AA.AA_utils import inputManager, musicManager, settings


class NameScene(Scene):

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager,
                 musicManager: musicManager.MusicManager):

        images_dir = os.path.join(settings.PARENT_PATH, "AA_images")

        self.bg_image = pygame.image.load(os.path.join(images_dir,
                                                       "dojo.jpg")).convert()
        self.bg_image = pygame.transform.scale(self.bg_image,
                                               settings.WINDOW_SIZE)

        super().__init__(mainApp, inputManager, musicManager)

    def initScene(self):
        super().initScene()

    def loopScene(self, events: list[pygame.event.Event]):

        self._mainApp.blit(
            self.bg_image,
            self.bg_image.get_rect(center=self._mainApp.get_rect().center))

        # Call parent loop to handle input and quitting
        return super().loopScene(events)

    def getTransition(self) -> Scene | None:
        return None
