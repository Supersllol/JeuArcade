from __future__ import annotations

import pygame, os
from AA.AA_scenes import homeScene

from AA.AA_scenes.sceneClass import Scene
from AA.AA_utils import inputManager, musicManager, settings
from AA.AA_utils.fontManager import upheaval

#Test de single VS multiplayer
singleplayer = False

class NameScene(Scene):

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager,
                 musicManager: musicManager.MusicManager):

        # Asset base path
        images_dir = os.path.join(settings.PARENT_PATH, "AA_images")
        icon_dir = os.path.join(images_dir, "AA_input_instruction")

        self.bg_image = pygame.image.load(os.path.join(images_dir,
                                                       "dojo.jpg")).convert()
        self.bg_image = pygame.transform.scale(self.bg_image,
                                               settings.WINDOW_SIZE)

        super().__init__(mainApp, inputManager, musicManager)

        self._icons = {
            "a":
                pygame.image.load(os.path.join(icon_dir,
                                               "Valider - A.png")).convert_alpha(),
            "b":
                pygame.image.load(os.path.join(icon_dir,
                                               "Effacer - B.png")).convert_alpha(),
            "select":
                pygame.image.load(os.path.join(
                    icon_dir, "Quitter - Select.png")).convert_alpha(),
            "joystick":
                pygame.image.load(os.path.join(
                    icon_dir, "Déplacer - Joystick.png")).convert_alpha(),
        }
        # Scale input icons uniformly
        for key, img in list(self._icons.items()):
            self._icons[key] = pygame.transform.scale(img, (150, 50))

        self.img_ver = {
            "check":
        pygame.image.load(os.path.join(
            images_dir, "check.png")).convert_alpha(),
            "x":
        pygame.image.load(os.path.join(
            images_dir, "x.png")).convert_alpha()}

        self.lettres = pygame.Surface((settings.WINDOW_SIZE[0]//2,settings.WINDOW_SIZE[1]), pygame.SRCALPHA)
        x = 73
        y = 150
        lap = 0
        for i in alpha:
            text = upheaval(i, 75, (255, 255, 255))
            if i == "M" or i == "W":
                self.lettres.blit(text, (x-4, y))
            elif i == "Q":
                self.lettres.blit(text, (x, y-3))
            elif i == "Y":
                self.lettres.blit(text, (x-2, y))
            else:
                self.lettres.blit(text, (x, y))
            x += 80
            lap += 1
            if lap%5 == 0:
                y += 70
                x = 73

        self.selection = pygame.image.load(os.path.join(images_dir, "selection.png")).convert_alpha()
        self.selection_pos1 = [56,150]
        self.selection_pos2 = [567,150]

        self.alphabet = [
            ["A","B","C","D","E"],
            ["F","G","H","I","J"],
            ["K","L","M","N","O"],
            ["P","Q","R","S","T"],
            ["U","V","W","X","Y"],
            ["Z"]
        ]
        self.y = 0
        self.x = 0
        self.nom = []
        self.ready = False

        #2nd player
        self.y2 = 0
        self.x2 = 0
        self.nom2 = []
        self.ready2 = False

    def initScene(self):
        super().initScene()

    def loopScene(self, events: list[pygame.event.Event]):

        # Input: navigate with up/down, confirm with A/Start
        for i in range(2):  # Check both players
            new_axes = self._inputManager.getAxesActive(i,
                                                        onlyCheckForNew=True)
            if inputManager.AxisInputs.Y_UP in new_axes:
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
                print("UP")
            elif inputManager.AxisInputs.Y_DOWN in new_axes:
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
                            self.selection_pos2[0] = 56
                        self.selection_pos2[1] += 70
                print("DOWN")
            elif inputManager.AxisInputs.X_LEFT in new_axes:
                if i == 0:
                    if self.x > 0:
                        if not self.y == 5:
                            self.x -= 1
                            self.selection_pos1[0] -= 80
                    else:
                        if self.x2 > 0:
                            if not self.y2 == 5:
                                self.x2 -= 1
                                self.selection_pos2[0] -= 80
                print("LEFT")
            elif inputManager.AxisInputs.X_RIGHT in new_axes:
                if i == 0:
                    if self.x <= 3:
                        if not self.y == 5:
                            self.x += 1
                            self.selection_pos1[0] += 80
                    else:
                        if self.x2 <= 3:
                            if not self.y2 == 5:
                                self.x2 += 1
                                self.selection_pos2[0] += 80
                print("RIGHT")

            new_btns = self._inputManager.getBtnsPressed(i,
                                                         onlyCheckForNew=True)
            if inputManager.ButtonInputs.A in new_btns:
                # Trigger action
                if i == 0:
                    if len(self.nom) < 3:
                        self.nom.append(self.alphabet[self.y][self.x])
                    else:
                        if len(self.nom2) < 3:
                            self.nom2.append(self.alphabet[self.y][self.x])
                print(f"A, {self.nom}")

            elif inputManager.ButtonInputs.B in new_btns:
                # Trigger action
                if i == 0:
                    if len(self.nom) > 0:
                        self.nom.pop()
                    self.ready = False
                else:
                    if len(self.nom2) > 0:
                        self.nom2.pop()
                    self.ready2 = False
                print(f"B, {self.nom}")

            elif inputManager.ButtonInputs.START in new_btns:
                if i == 0:
                    if not self.nom == ["C","P","U"] and len(self.nom) == 3:
                        print(f"{self.nom[0]} {self.nom[1]} {self.nom[2]}")
                        self.ready = True
                    else:
                        print("ERREUR")
                else:
                    if not self.nom == ["C","P","U"] and len(self.nom) == 3:
                        print(f"{self.nom[0]} {self.nom[1]} {self.nom[2]}")
                        self.ready = True
                    else:
                        print("ERREUR")

        self._mainApp.blit(
            self.bg_image,
            self.bg_image.get_rect(center=self._mainApp.get_rect().center))

        screen.blit(self.selection, (self.selection_pos1[0],self.selection_pos1[1]))
        screen.blit(self.lettres, (0,0))

        if not singleplayer:
            screen.blit(self.selection, (self.selection_pos2[0],self.selection_pos2[1]))
            screen.blit(self.lettres, (settings.WINDOW_SIZE[0]//2, 0))

        # Button input instructions at bottom
        # B input
        self._mainApp.blit(self._icons["joystick"],
                           (20, settings.WINDOW_SIZE[1] - 180))
        self._mainApp.blit(self._icons["a"],
                           (20, settings.WINDOW_SIZE[1] - 140))
        # Select input
        self._mainApp.blit(self._icons["b"],
                           (20, settings.WINDOW_SIZE[1] - 100))
        # Joystick input
        self._mainApp.blit(self._icons["select"],
                           (15, settings.WINDOW_SIZE[1] - 60))

        if self.ready:
            self._mainApp.blit(self.img_ver["check"],
                               (15, 60))
            self._mainApp.blit(self.img_ver["x"],
                               (600, 60))

        # Call parent loop to handle input and quitting
        return super().loopScene(events)

    def getTransition(self) -> Scene | None:
        return None

#Truc random
alpha = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

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