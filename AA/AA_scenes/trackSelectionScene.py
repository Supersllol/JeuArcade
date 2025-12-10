import pygame, os
from AA.AA_scenes import sceneClass, homeScene
from AA.AA_utils import inputManager, musicManager, dbManager, settings


class SplashScene(sceneClass.Scene):

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

    def initScene(self):
        super().initScene()
        # Music can be played here if desired

    def loopScene(self, events: list[pygame.event.Event]):
        # Draw background
        self._mainApp.blit(self.bg_image, (0, 0))

        # Call parent loop to handle input and quitting
        return super().loopScene(events)

    def getTransition(self) -> sceneClass.Scene | None:
        return None
