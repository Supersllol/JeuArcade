from __future__ import annotations

import pygame, os
from AA.AA_scenes import ruleScene, nameScene

from AA.AA_scenes.sceneClass import Scene
from AA.AA_utils import inputManager, musicManager, settings, dbManager, countries, fontManager, misc
from AA.AA_game import player

flagWidth = 65


class CountryChooser:

    def __init__(self, playerName: str, dbManager: dbManager.DatabaseManager,
                 bgNom: pygame.Surface):
        self.playerName = playerName
        self.validated = False
        self.askForExit = False

        self.allCountriesSurface = pygame.Surface(
            (settings.WINDOW_SIZE[0] // 2, settings.WINDOW_SIZE[1]),
            pygame.SRCALPHA)
        self.bgCountries = misc.rescaleSurface(
            pygame.image.load(
                os.path.join(settings.PARENT_PATH, "AA_images",
                             "fond_bleu.png")), (475, None))

        self.currentChoiceIndex = 0
        self.countryChoices = list(countries.CountryOptions)

        self.alreadyInDb = playerName in dbManager.getSavedPlayers()
        self.currentIndicator: pygame.Surface
        self.selectionIndicator: pygame.Surface
        self.validationIndicator: pygame.Surface
        self.countryNamesCenterPos: list[list[tuple[int, int]]]

        if self.alreadyInDb:
            self.selectionIndicator = misc.rescaleSurface(
                pygame.image.load(
                    os.path.join(settings.PARENT_PATH, "AA_images",
                                 "pays_selection.png")), (140, None))
            self.validationIndicator = misc.rescaleSurface(
                pygame.image.load(
                    os.path.join(settings.PARENT_PATH, "AA_images",
                                 "pays_choisi.png")), (140, None))
            center = self.bgCountries.get_rect().center
            self.countryNamesCenterPos = [[center]]
            playerCountry = countries.getCountryFromStr(
                dbManager.getSavedPlayers()[playerName].playerCountry)
            if playerCountry:
                self.countryChoices = [playerCountry]
                countryName = fontManager.upheaval(playerCountry.name, 60,
                                                   (255, 255, 255))
                self.bgCountries.blit(countryName,
                                      countryName.get_rect(center=center))
                flag = countries.getCountryFlagSurface(playerCountry, 200)
                self.bgCountries.blit(
                    flag, flag.get_rect(center=(center[0], center[1] - 140)))

                explications = fontManager.upheaval(f"JOUEUR DÉJÀ ENREGISTRÉ",
                                                    30, (255, 255, 255))
                self.bgCountries.blit(
                    explications,
                    explications.get_rect(center=(center[0], center[1] + 135)))
        else:
            self.selectionIndicator = misc.rescaleSurface(
                pygame.image.load(
                    os.path.join(settings.PARENT_PATH, "AA_images",
                                 "pays_selection.png")), (75, None))
            self.validationIndicator = misc.rescaleSurface(
                pygame.image.load(
                    os.path.join(settings.PARENT_PATH, "AA_images",
                                 "pays_choisi.png")), (75, None))

            colX = (self.bgCountries.get_width() // 2 - 135,
                    self.bgCountries.get_width() // 2 + 135)

            self.countryNamesCenterPos = [[(colX[i], 120 + j * 95)
                                           for j in range(5)]
                                          for i in range(2)]

            for i in range(2):
                for j in range(5):
                    country = self.countryChoices[5 * i + j]

                    countryName = fontManager.upheaval(country.name, 30,
                                                       (255, 255, 255))
                    txtCenterPos = self.countryNamesCenterPos[i][j]
                    self.bgCountries.blit(
                        countryName, countryName.get_rect(center=txtCenterPos))

                    flag = countries.getCountryFlagSurface(country, flagWidth)
                    flagXPos = txtCenterPos[
                        0] + 90 if i == 0 else txtCenterPos[0] - 90
                    self.bgCountries.blit(
                        flag,
                        flag.get_rect(center=(flagXPos, txtCenterPos[1])))

        self.allCountriesSurface.blit(
            bgNom,
            bgNom.get_rect(center=(self.allCountriesSurface.get_width() // 2,
                                   175)))
        nom = fontManager.upheaval(playerName, 80, (255, 204, 37))
        self.allCountriesSurface.blit(
            nom,
            nom.get_rect(center=(self.allCountriesSurface.get_width() // 2 + 2,
                                 168)))

        self.bgCountries = pygame.transform.scale_by(self.bgCountries, 0.8)
        for i in range(len(self.countryNamesCenterPos)):
            for j in range(len(self.countryNamesCenterPos[i])):
                self.countryNamesCenterPos[i][j] = (int(
                    self.countryNamesCenterPos[i][j][0] *
                    0.8), int(self.countryNamesCenterPos[i][j][1] * 0.8))

        # store immutable bases so we can reset before drawing
        self._bgCountries_base = self.bgCountries.copy()
        self._allCountries_base = self.allCountriesSurface.copy()

        self.currentIndicator = self.selectionIndicator
        self.drawIndicator()

    def drawIndicator(self):
        i, j = self.currentChoiceIndex // 5, self.currentChoiceIndex % 5
        txtPos = self.countryNamesCenterPos[i][j]

        # restore clean copies
        self.bgCountries = self._bgCountries_base.copy()
        self.allCountriesSurface = self._allCountries_base.copy()

        # draw only the current indicator
        self.bgCountries.blit(
            self.currentIndicator,
            self.currentIndicator.get_rect(center=(txtPos[0], txtPos[1] + 2)))

        # blit the updated countries panel into the full countries surface
        self.allCountriesSurface.blit(
            self.bgCountries,
            self.bgCountries.get_rect(
                center=(self.allCountriesSurface.get_rect().centerx, 480)))

    def getSelectedCountry(self):
        return self.countryChoices[self.currentChoiceIndex]

    def updateIndicator(self, btns: list[inputManager.ButtonInputs],
                        axes: list[inputManager.AxisInputs]):
        if inputManager.ButtonInputs.START in btns:
            self.validated = True
            self.currentIndicator = self.validationIndicator
        if inputManager.ButtonInputs.B in btns:
            if not self.validated:
                self.askForExit = True
            self.validated = False
            self.currentIndicator = self.selectionIndicator

        if not self.validated and not self.alreadyInDb:
            if inputManager.AxisInputs.X_LEFT in axes:
                self.currentChoiceIndex = (self.currentChoiceIndex - 5) % 10
            if inputManager.AxisInputs.X_RIGHT in axes:
                self.currentChoiceIndex = (self.currentChoiceIndex + 5) % 10
            if inputManager.AxisInputs.Y_DOWN in axes:
                currentColumn = 0 if self.currentChoiceIndex < 5 else 1
                self.currentChoiceIndex = 5 * currentColumn + (
                    (self.currentChoiceIndex - 5 * currentColumn) + 1) % 5
            if inputManager.AxisInputs.Y_UP in axes:
                currentColumn = 0 if self.currentChoiceIndex < 5 else 1
                self.currentChoiceIndex = 5 * currentColumn + (
                    (self.currentChoiceIndex - 5 * currentColumn) - 1) % 5

        self.drawIndicator()


class CountryScene(Scene):

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager,
                 musicManager: musicManager.MusicManager,
                 dbManager: dbManager.DatabaseManager, names: tuple[str, str]):

        images_dir = os.path.join(settings.PARENT_PATH, "AA_images")
        self.bg_image = pygame.image.load(os.path.join(images_dir, "dojo.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image,
                                               settings.WINDOW_SIZE).convert()
        self.bgNom = pygame.image.load(os.path.join(
            images_dir, "nom.png")).convert_alpha()

        icon_dir = os.path.join(images_dir, "AA_input_instruction")

        self._icons = {
            "b":
            pygame.image.load(os.path.join(icon_dir,
                                           "B - retour.png")).convert_alpha(),
            "start":
            pygame.image.load(os.path.join(
                icon_dir, "Start - Valider.png")).convert_alpha(),
            "select":
            pygame.image.load(os.path.join(
                icon_dir, "Quitter - Select.png")).convert_alpha(),
            "joystick":
            pygame.image.load(os.path.join(
                icon_dir, "Déplacer - Joystick.png")).convert_alpha(),
        }
        # Scale input icons uniformly
        for key, img in list(self._icons.items()):
            self._icons[key] = pygame.transform.scale(
                img, (150, 50)).convert_alpha()

        self.names = names
        self.singlePlayer = self.names[1] == "CPU"

        self.countryChoosers = [
            CountryChooser(self.names[i], dbManager, self.bgNom)
            for i in range(1 + int(not self.singlePlayer))
        ]

        self.transitionOption = 0

        super().__init__(mainApp, inputManager, musicManager, dbManager)

    def initScene(self):
        super().initScene()

    def returnToPreviousScreen(self):
        pass

    def loopScene(self, events: list[pygame.event.Event]):
        self._mainApp.blit(
            self.bg_image,
            self.bg_image.get_rect(center=self._mainApp.get_rect().center))

        # show player names and grids
        for i in range(1 + int(not self.singlePlayer)):
            self.countryChoosers[i].updateIndicator(
                self._inputManager.getBtnsPressed(i),
                self._inputManager.getAxesActive(i))
            if self.countryChoosers[i].askForExit:
                self.sceneFinished = True
                self.transitionOption = 1
            self._mainApp.blit(self.countryChoosers[i].allCountriesSurface,
                               (i * self._mainApp.get_width() // 2, 0))

        if all([chooser.validated for chooser in self.countryChoosers]):
            self._sceneFinished = True
            self.transitionOption = 0

        if self.singlePlayer:
            self._mainApp.blit(
                self.bgNom,
                self.bgNom.get_rect(center=(3 * self._mainApp.get_width() // 4,
                                            self._mainApp.get_height() // 2)))
            texteCpu = fontManager.upheaval("CPU", 80, (255, 204, 37))
            self._mainApp.blit(
                texteCpu,
                texteCpu.get_rect(
                    center=(3 * self._mainApp.get_width() // 4 + 2,
                            self._mainApp.get_height() // 2 - 5)))

        titre = fontManager.upheaval("Choix du pays", 75, (255, 204, 37))
        self._mainApp.blit(
            titre,
            titre.get_rect(center=(self._mainApp.get_rect().centerx, 60)))

        # Button input instructions at bottom

        self._mainApp.blit(self._icons["joystick"],
                           (20, settings.WINDOW_SIZE[1] - 60))

        self._mainApp.blit(self._icons["start"],
                           (220, settings.WINDOW_SIZE[1] - 60))

        self._mainApp.blit(self._icons["b"],
                           (420, settings.WINDOW_SIZE[1] - 60))

        self._mainApp.blit(self._icons["select"],
                           (620, settings.WINDOW_SIZE[1] - 60))

        # Call parent loop to handle input and quitting
        return super().loopScene(events)

    def getTransition(self) -> Scene | None:
        if self.transitionOption == 0:
            player0 = player.Player(
                self.names[0], self.countryChoosers[0].getSelectedCountry(), 0,
                self._mainApp)
            if not self.singlePlayer:
                player1 = player.Player(
                    self.names[1],
                    self.countryChoosers[1].getSelectedCountry(), 1,
                    self._mainApp)
            else:
                player1 = player.Player(
                    self.names[1],
                    countries.getRandomCPUCountry(player0._country), 1,
                    self._mainApp)
            return ruleScene.RuleScene(self._mainApp, self._inputManager,
                                       self._musicManager, self._dbManager,
                                       (player0, player1))
        if self.transitionOption == 1:
            return nameScene.NameScene(self._mainApp, self._inputManager,
                                       self._musicManager, self._dbManager,
                                       self.names)
        return None
