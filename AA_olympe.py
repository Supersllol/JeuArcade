import pygame
from AA_scenes import introScene, gameScene
from AA_utils import settings, inputManager


def main():
    pygame.init()

    mainApp = pygame.display.set_mode(settings.WINDOW_SIZE, pygame.NOFRAME)
    pygame.mouse.set_visible(False)

    # setup joysticks
    joysticks = []
    joystickCount = pygame.joystick.get_count()
    if not joystickCount:
        print("Aucun joystick connecté")
    else:
        for i in range(joystickCount):
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            joysticks.append(joystick)
    input = inputManager.InputManager(joysticks)

    # currentScene = introScene.IntroScene(mainApp, input)
    currentScene = gameScene.GameScene(mainApp, input)
    ACTIF = True
    clock = pygame.time.Clock()

    currentScene.initScene()

    while ACTIF:
        if not currentScene.loopScene([event for event in pygame.event.get()]):
            ACTIF = False

        if currentScene.finished:
            newScene = currentScene.getTransition()
            if newScene:
                newScene.initScene()
                currentScene = newScene

        clock.tick(settings.FRAMERATE)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
