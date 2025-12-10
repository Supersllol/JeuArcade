from __future__ import annotations

import pygame, os
from AA.AA_scenes import homeScene

from AA.AA_scenes import sceneClass, countryScene, homeScene
from AA.AA_utils import inputManager, musicManager, settings, dbManager, timer
from AA.AA_utils.fontManager import upheaval

#Truc random
alpha = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]


class NameScene(sceneClass.Scene):

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager,
                 musicManager: musicManager.MusicManager,
                 dbManager: dbManager.DatabaseManager, names: tuple[str, str]):

        # Asset base path
        images_dir = os.path.join(settings.PARENT_PATH, "AA_images")
        icon_dir = os.path.join(images_dir, "AA_input_instruction")

        self.bg_image = pygame.image.load(os.path.join(images_dir,
                                                       "dojo.jpg")).convert()
        self.bg_image = pygame.transform.scale(self.bg_image,
                                               settings.WINDOW_SIZE)
        # SFX live one level above AA (e.g., JeuArcade/AA_sfx), so hop up a directory
        sounds_dir = os.path.join(os.path.dirname(settings.PARENT_PATH),
                      "AA_sfx")
        
        self._sounds = {
            "select": pygame.mixer.Sound(os.path.join(sounds_dir, "Select.wav")),
            "option" : pygame.mixer.Sound(os.path.join(sounds_dir, "Option.wav")),
            "back": pygame.mixer.Sound(os.path.join(sounds_dir, "Back.wav")),
            "confirm": pygame.mixer.Sound(os.path.join(sounds_dir, "Confirm.wav")),
        }

        super().__init__(mainApp, inputManager, musicManager, dbManager)

        self._icons = {
            "a":
            pygame.image.load(os.path.join(icon_dir,
                                           "Valider - A.png")).convert_alpha(),
            "b":
            pygame.image.load(os.path.join(icon_dir,
                                           "B - Retour.png")).convert_alpha(),
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

        self.img_ver = {
            "check":
            pygame.image.load(os.path.join(images_dir,
                                           "check.png")).convert_alpha(),
            "x":
            pygame.image.load(os.path.join(images_dir,
                                           "x.png")).convert_alpha()
        }
        # Scale input icons uniformly
        for key, img in list(self.img_ver.items()):
            self.img_ver[key] = pygame.transform.scale(img, (80, 80))

        self.lettres = pygame.Surface(
            (settings.WINDOW_SIZE[0] // 2, settings.WINDOW_SIZE[1]),
            pygame.SRCALPHA)
        x = 73
        y = 250
        lap = 0
        for i in alpha:
            text = upheaval(i, 75, (255, 255, 255))
            if i == "M" or i == "W":
                self.lettres.blit(text, (x - 4, y))
            elif i == "Q":
                self.lettres.blit(text, (x, y - 3))
            elif i == "Y":
                self.lettres.blit(text, (x - 2, y))
            else:
                self.lettres.blit(text, (x, y))
            x += 80
            lap += 1
            if lap % 5 == 0:
                y += 70
                x = 73

        self.info = upheaval("Choix du nom", 80, (255, 204, 37))

        self.selection = pygame.image.load(
            os.path.join(images_dir, "selection.png")).convert_alpha()
        self.selection_o = pygame.image.load(
            os.path.join(images_dir, "selection_o.png")).convert_alpha()
        self.selection_pos1 = [56, 250]
        self.selection_pos2 = [568, 250]

        self.nom_place = pygame.image.load(os.path.join(
            images_dir, "nom.png")).convert_alpha()

        self.alphabet = [["A", "B", "C", "D", "E"], ["F", "G", "H", "I", "J"],
                         ["K", "L", "M", "N", "O"], ["P", "Q", "R", "S", "T"],
                         ["U", "V", "W", "X", "Y"], ["Z"]]
        self.y = 0
        self.x = 0
        self.timer = timer.Timer()
        self.nom = names[0]  # store name as a string
        self.ready = False
        self.erreur = False
        self.click = False
        self.prio = False
        self.text = upheaval(self.nom, 75, (255, 204, 37))

        # 2nd player
        self.y2 = 0
        self.x2 = 0
        self.timer2 = timer.Timer()
        self.nom2 = names[1]  # store second player's name as a string
        self.ready2 = False
        self.erreur2 = False
        self.click2 = False
        self.prio2 = False
        self.text2 = upheaval(self.nom2, 75, (255, 204, 37))

        self._singlePlayer = self.nom2 == "CPU"
        self.transitionOption = None

    def initScene(self):
        super().initScene()
        
        # Start loop menu music if not already playing
        menu_music_path = os.path.join(os.path.dirname(settings.PARENT_PATH),
                                       "AA", "AA_chansons", "loop_menu.mp3")
        if not self._musicManager.isLooping() or self._musicManager.getCurrentTrack() != menu_music_path:
            self._musicManager.playLooping(menu_music_path)

    def loopScene(self, events: list[pygame.event.Event]):

        # Input: navigate with up/down, confirm with A/Start
        for i in range(1 + int(not self._singlePlayer)):  # Check both players
            new_axes = self._inputManager.getAxesActive(i,
                                                        onlyCheckForNew=True)
            if inputManager.AxisInputs.Y_UP in new_axes:
                self._sounds["option"].play()
                if i == 0:
                    if self.y > 0:
                        if self.y == 5:
                            self.x = 0
                        self.y -= 1
                        self.selection_pos1[1] -= 70
                else:
                    if self.y2 > 0:
                        if self.y2 == 5:
                            self.x2 = 0
                        self.y2 -= 1
                        self.selection_pos2[1] -= 70
            elif inputManager.AxisInputs.Y_DOWN in new_axes:
                self._sounds["option"].play()
                if i == 0:
                    if self.y <= 4:
                        self.y += 1
                        if self.y == 5:
                            self.x = 0
                            self.selection_pos1[0] = 56
                        self.selection_pos1[1] += 70
                else:
                    if self.y2 <= 4:
                        self.y2 += 1
                        if self.y2 == 5:
                            self.x2 = 0
                            self.selection_pos2[0] = 568
                        self.selection_pos2[1] += 70
            elif inputManager.AxisInputs.X_LEFT in new_axes:
                self._sounds["option"].play()
                if i == 0:  # PLAYER 1
                    if self.x > 0 and self.y != 5:
                        self.x -= 1
                        self.selection_pos1[0] -= 80
                else:  # PLAYER 2
                    if self.x2 > 0 and self.y2 != 5:
                        self.x2 -= 1
                        self.selection_pos2[0] -= 80

            elif inputManager.AxisInputs.X_RIGHT in new_axes:
                self._sounds["option"].play()
                if i == 0:  # PLAYER 1
                    if self.x < 4 and self.y != 5:
                        self.x += 1
                        self.selection_pos1[0] += 80
                else:  # PLAYER 2
                    if self.x2 < 4 and self.y2 != 5:
                        self.x2 += 1
                        self.selection_pos2[0] += 80

######################################################################### Axes ^^^^

            new_btns = self._inputManager.getBtnsPressed(i,
                                                         onlyCheckForNew=True)
            if inputManager.ButtonInputs.A in new_btns:
                # Trigger action
                self._sounds["select"].play()
                if i == 0:
                    if len(self.nom) < 3:
                        self.nom += self.alphabet[self.y][self.x]
                        self.erreur = False
                        self.click = True
                        self.text = upheaval(self.nom, 75, (255, 204, 37))
                else:
                    if len(self.nom2) < 3:
                        self.nom2 += self.alphabet[self.y2][self.x2]
                        self.erreur2 = False
                        self.click2 = True
                        self.text2 = upheaval(self.nom2, 75, (255, 204, 37))

            elif inputManager.ButtonInputs.B in new_btns:
                self._sounds["back"].play()
                # Trigger action
                requestedExit = False
                if i == 0:
                    if len(self.nom) == 0:
                        requestedExit = True
                    if len(self.nom) > 0:
                        self.nom = self.nom[:-1]
                    self.ready = False
                    self.erreur = False
                    self.text = upheaval(self.nom, 80, (255, 204, 37))
                    if self.prio:
                        self.ready2 = True
                        self.prio = False
                        self.prio2 = True
                        self.erreur2 = False
                else:
                    if len(self.nom2) == 0:
                        requestedExit = True
                    if len(self.nom2) > 0:
                        self.nom2 = self.nom2[:-1]
                    self.ready2 = False
                    self.erreur2 = False
                    self.text2 = upheaval(self.nom2, 80, (255, 204, 37))
                    if self.prio2:
                        self.ready = True
                        self.prio2 = False
                        self.prio = True
                        self.erreur = False

                if requestedExit:
                    self.transitionOption = 1
                    self.sceneFinished = True

            elif inputManager.ButtonInputs.START in new_btns:
                # Trigger action
                if i == 0:
                    self.erreur = False
                    if not self.nom == "CPU" and len(self.nom) == 3:
                        if not self.ready2:
                            self._sounds["confirm"].play()
                            self.ready = True
                        else:
                            if self.nom != self.nom2:
                                self._sounds["confirm"].play()
                                self.ready = True
                            else:
                                self.prio2 = True
                                self.erreur = True
                    else:
                        self.erreur = True
                else:
                    self.erreur2 = False
                    if not self.nom2 == "CPU" and len(self.nom2) == 3:
                        if not self.ready:
                            self._sounds["confirm"].play()
                            self.ready2 = True
                        else:
                            if self.nom != self.nom2:
                                self._sounds["confirm"].play()
                                self.ready2 = True
                            else:
                                self.prio = True
                                self.erreur2 = True
                    else:
                        self.erreur2 = True


################################################################################################INPUTS ^^^^^^

        self._mainApp.blit(
            self.bg_image,
            self.bg_image.get_rect(center=self._mainApp.get_rect().center))

        if self.click:
            self._mainApp.blit(
                self.selection_o,
                (self.selection_pos1[0], self.selection_pos1[1]))
            self.timer.start()
            if self.timer.elapsed() >= settings.NAME_INDICATOR_TIME:
                self.click = False
                self.timer.stop()
        else:
            self._mainApp.blit(
                self.selection,
                (self.selection_pos1[0], self.selection_pos1[1]))
        self._mainApp.blit(self.lettres, (0, 0))

        if not self._singlePlayer:
            if self.click2:
                self._mainApp.blit(
                    self.selection_o,
                    (self.selection_pos2[0], self.selection_pos2[1]))
                self.timer2.start()
                if self.timer2.elapsed() >= settings.NAME_INDICATOR_TIME:
                    self.click2 = False
                    self.timer2.stop()
            else:
                self._mainApp.blit(
                    self.selection,
                    (self.selection_pos2[0], self.selection_pos2[1]))
            self._mainApp.blit(self.lettres, (settings.WINDOW_SIZE[0] // 2, 0))

        # Button input instructions at bottom
        # B input
        self._mainApp.blit(self._icons["joystick"],
                           (20, settings.WINDOW_SIZE[1] - 60))
        self._mainApp.blit(self._icons["a"],
                           (220, settings.WINDOW_SIZE[1] - 60))
        self._mainApp.blit(self._icons["start"],
                           (420, settings.WINDOW_SIZE[1] - 60))
        # Select input
        self._mainApp.blit(self._icons["b"],
                           (620, settings.WINDOW_SIZE[1] - 60))
        # Joystick input
        self._mainApp.blit(self._icons["select"],
                           (820, settings.WINDOW_SIZE[1] - 60))

        # 1. Grid position
        lettres_rect = self.lettres.get_rect(topleft=(0, 0))

        # Center name box horizontally over the letter grid
        nom_place_rect = self.nom_place.get_rect()
        nom_place_rect.centerx = lettres_rect.centerx
        nom_place_rect.y = 110  # fixed position that’s on-screen

        # Center text inside the name box
        text_rect = self.text.get_rect(center=nom_place_rect.center)

        self._mainApp.blit(self.nom_place, nom_place_rect)
        self._mainApp.blit(self.text, (text_rect[0] + 1, text_rect[1] - 4))

        ########################################################
        if self._singlePlayer:
            self._mainApp.blit(
                self.nom_place,
                self.nom_place.get_rect(
                    center=(3 * self._mainApp.get_width() // 4,
                            self._mainApp.get_height() // 2)))
            texteCpu = upheaval("CPU", 80, (255, 204, 37))
            self._mainApp.blit(
                texteCpu,
                texteCpu.get_rect(
                    center=(3 * self._mainApp.get_width() // 4 + 2,
                            self._mainApp.get_height() // 2 - 5)))
        else:

            # 1. Grid position
            lettres_rect = self.lettres.get_rect(
                topleft=(settings.WINDOW_SIZE[0] // 2, 0))

            # Center name box horizontally over the letter grid
            nom_place_rect2 = self.nom_place.get_rect()
            nom_place_rect2.centerx = lettres_rect.centerx
            nom_place_rect2.y = 110  # fixed position that’s on-screen

            # Center text inside the name box
            text_rect2 = self.text2.get_rect(center=nom_place_rect2.center)

            self._mainApp.blit(self.nom_place, nom_place_rect2)
            self._mainApp.blit(self.text2,
                               (text_rect2[0] + 1, text_rect2[1] - 4))

        if self.ready:
            self._mainApp.blit(self.img_ver["check"], (350, 142))
        if self.erreur:
            self._mainApp.blit(self.img_ver["x"], (350, 142))
        if not self._singlePlayer:
            if self.ready2:
                self._mainApp.blit(self.img_ver["check"], (863, 142))
            if self.erreur2:
                self._mainApp.blit(self.img_ver["x"], (863, 142))

        self._mainApp.blit(
            self.info,
            self.info.get_rect(center=(self._mainApp.get_rect().centerx, 60)))

        if self.ready:
            if self._singlePlayer or (not self._singlePlayer and self.ready2):
                self._sceneFinished = True
                self.transitionOption = 0

        # Call parent loop to handle input and quitting
        return super().loopScene(events)

    def getTransition(self) -> sceneClass.Scene | None:
        if self.transitionOption == 0:
            return countryScene.CountryScene(self._mainApp, self._inputManager,
                                             self._musicManager,
                                             self._dbManager,
                                             (self.nom, self.nom2))
        if self.transitionOption == 1:
            return homeScene.HomeScene(self._mainApp, self._inputManager,
                                       self._musicManager, self._dbManager)
        return None
