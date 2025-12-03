from __future__ import annotations

import pygame
from AA.AA_scenes import gameScene
from AA.AA_utils import inputManager, musicManager, countries, settings
from AA.AA_game import musicTrack, player


def main():
    pygame.init()

    mainApp = pygame.display.set_mode(settings.WINDOW_SIZE,
                                      pygame.NOFRAME | pygame.SRCALPHA)
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
    music = musicManager.MusicManager()

    # currentScene = introScene.IntroScene(mainApp, input)
    player0 = player.Player("SIM", countries.CountryFlags.Québec, 0, mainApp)
    player1 = player.Player("MIS", countries.CountryFlags.Canada, 1, mainApp)
    currentScene = gameScene.GameScene(mainApp, input, music,
                                       musicTrack.GameTracks.SEMI_CHARMED_LIFE,
                                       (player0, player1))
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
