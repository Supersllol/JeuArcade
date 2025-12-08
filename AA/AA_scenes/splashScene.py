from __future__ import annotations

import os
import sys
import pygame
import math
from AA.AA_scenes import homeScene

# Ensure project root is in sys.path when running this file directly
if __name__ == "__main__":
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from AA.AA_scenes.sceneClass import Scene
from AA.AA_utils import inputManager, musicManager, settings, dbManager


class SplashScene(Scene):

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager,
                 musicManager: musicManager.MusicManager,
                 dbManager: dbManager.DatabaseManager):
        super().__init__(mainApp, inputManager, musicManager, dbManager)

        # Asset paths
        images_dir = os.path.join(settings.PARENT_PATH, "AA_images")

        # Load and scale background
        self.bg_image = pygame.image.load(
            os.path.join(images_dir, "splashscreen.png")).convert()
        self.bg_image = pygame.transform.scale(self.bg_image,
                                               settings.WINDOW_SIZE)
        self.display_duration = 3  # Duration to display splash screen in seconds

    def initScene(self):
        super().initScene()
        # Music can be played here if desired

    def loopScene(self, events: list[pygame.event.Event]):
        # Draw background
        self._mainApp.blit(self.bg_image, (0, 0))

        # Check elapsed time
        if self._stateTimer.elapsed(
        ) >= self.display_duration and not self.sceneFinished:
            self.sceneFinished = True

        # Call parent loop to handle input and quitting
        return super().loopScene(events)

    def getTransition(self) -> Scene | None:
        return homeScene.HomeScene(self._mainApp, self._inputManager,
                                   self._musicManager)


# Standalone test harness
if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(settings.WINDOW_SIZE)
    pygame.display.set_caption("Dance Dance to the Death - Home Screen Test")
    clock = pygame.time.Clock()

    # Create dummy managers for testing
    # InputManager needs a list of joysticks (empty list defaults to keyboard)
    input_mgr = inputManager.InputManager([])  # Empty list = keyboard mode
    music_mgr = musicManager.MusicManager()  # No arguments needed

    # Create home scene
    splash_scene = SplashScene(screen, input_mgr, music_mgr)
    splash_scene.initScene()

    # Main loop
    running = True
    print("Splash Screen Test Mode")

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Run scene loop
        if not splash_scene.loopScene(events):
            running = False

        # Update display
        pygame.display.flip()
        clock.tick(settings.FRAMERATE)

    pygame.quit()
    print("Splash screen test ended.")
