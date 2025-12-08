from __future__ import annotations

import pygame
from AA.AA_scenes import gameScene, homeScene, splashScene, nameScene, countryScene
from AA.AA_utils import inputManager, musicManager, countries, settings, timer, dbManager
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
    db = dbManager.DatabaseManager()
    # currentScene = homeScene.HomeScene(mainApp, input, music, db)
    # currentScene = nameScene.NameScene(mainApp, input, music, db)
    # currentScene = countryScene.CountryScene(mainApp, input, music, db)
    # currentScene = splashScene.SplashScene(mainApp, input, music, db)
    player0 = player.Player("SIM", countries.CountryOptions.QBC, 0, mainApp)
    player1 = player.Player(
        "TST", countries.getRandomCPUCountry(countries.CountryOptions.QBC), 1,
        mainApp, False)
    currentScene = gameScene.GameScene(mainApp, input, music, db,
                                       musicTrack.GameTracks.SEMI_CHARMED_LIFE,
                                       (player0, player1))

    ACTIF = True
    clock = pygame.time.Clock()
    mainTimer = timer.Timer()

    currentScene.initScene()
    mainTimer.start()
    while ACTIF:
        if not currentScene.loopScene([event for event in pygame.event.get()]):
            ACTIF = False

        if currentScene.sceneFinished:
            if currentScene.fadeoutScene():
                newScene = currentScene.getTransition()
                if newScene:
                    newScene.initScene()
                    currentScene = newScene
                else:
                    ACTIF = False

        if mainTimer.elapsed() >= (1 / settings.FRAMERATE):
            clock.tick(settings.FRAMERATE)
            pygame.display.flip()
            mainTimer.restart()

    pygame.quit()
    db.closeConnection()


if __name__ == "__main__":
    main()
