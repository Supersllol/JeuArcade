from __future__ import annotations

import pygame, os
from AA.AA_scenes import homeScene

from AA.AA_scenes.sceneClass import Scene
from AA.AA_utils import inputManager, musicManager, settings
from AA.AA_utils.fontManager import upheaval


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

        x = 73
        y = 150
        lap = 0
        for n in range(2):
            for i in alphabet:
                text = upheaval(i, 75, (255, 255, 255))
                screen.blit(text, (x, y))
                x += 80
                lap += 1
                if lap%5 == 0:
                    y += 70
                    x = 73
                    if n == 1:
                        x = 585
            x = 585
            lap = 0
            y = 150

        # Call parent loop to handle input and quitting
        return super().loopScene(events)

    def getTransition(self) -> Scene | None:
        return None

#Truc random
alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

# Standalone test harness
if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(settings.WINDOW_SIZE)
    pygame.display.set_caption("Dance Dance to the Death - Name Screen Test")
    clock = pygame.time.Clock()

    # Create dummy managers for testing
    # InputManager needs a list of joysticks (empty list defaults to keyboard)
    input_mgr = inputManager.InputManager([])  # Empty list = keyboard mode
    music_mgr = musicManager.MusicManager()  # No arguments needed

    # Create home scene
    name_scene = NameScene(screen, input_mgr, music_mgr)
    name_scene.initScene()

    # Main loop
    running = True
    print("Name Screen Test Mode")
    print(
        "Controls: Arrow keys (UP/DOWN) to navigate, Q to select, ESC to quit")

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Run scene loop
        if not name_scene.loopScene(events):
            running = False

        # Update display
        pygame.display.flip()
        clock.tick(settings.FRAMERATE)

    pygame.quit()
    print("Name screen test ended.")