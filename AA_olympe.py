import pygame
from AA_scenes import introScene

FRAMERATE = 60


def main():
    pygame.init()

    mainApp = pygame.display.set_mode((1024, 768), pygame.NOFRAME)
    currentScene = introScene.IntroScene(mainApp)
    ACTIF = True
    clock = pygame.time.Clock()

    # setup joysticks
    joysticks = ()
    joystickCount = pygame.joystick.get_count()
    if not joystickCount:
        print("Aucun joystick connecté, veuillez réessayer.")
        return
    else:
        joystick0 = pygame.joystick.Joystick(0)
        if joystickCount > 1:
            joystick1 = pygame.joystick.Joystick(1)
        else:
            joystick1 = None
        joysticks = (joystick0, joystick1)

    currentScene.initScene()

    while ACTIF:
        if not currentScene.loopScene([event for event in pygame.event.get()],
                                      joysticks):
            ACTIF = False

        if currentScene.finished:
            currentScene = currentScene.getTransition()
            currentScene.initScene()

        clock.tick(FRAMERATE)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
