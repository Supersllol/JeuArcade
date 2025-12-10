import pygame, os
from AA.AA_scenes import sceneClass, gameScene
from AA.AA_utils import inputManager, musicManager, dbManager, settings, fontManager, misc
from AA.AA_game import musicTrack, player


class TrackSelectionScene(sceneClass.Scene):

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager,
                 musicManager: musicManager.MusicManager,
                 dbManager: dbManager.DatabaseManager,
                 players: tuple[player.Player, player.Player]):
        super().__init__(mainApp, inputManager, musicManager, dbManager)

        self.players = players

        # Asset paths
        images_dir = os.path.join(settings.PARENT_PATH, "AA_images")

        icon_dir = os.path.join(images_dir, "AA_input_instruction")

        self._icons = {
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

        sounds_dir = os.path.join(os.path.dirname(settings.PARENT_PATH),
                                  "AA_sfx")

        self._sounds = {
            "option": pygame.mixer.Sound(os.path.join(sounds_dir,
                                                      "Option.wav")),
            "confirm":
            pygame.mixer.Sound(os.path.join(sounds_dir, "Confirm.wav")),
        }
        # Scale input icons uniformly
        for key, img in list(self._icons.items()):
            self._icons[key] = pygame.transform.scale(
                img, (150, 50)).convert_alpha()

        # Load and scale background
        self.bg_image = pygame.image.load(os.path.join(images_dir,
                                                       "dojo.jpg")).convert()
        self.bg_image = pygame.transform.scale(self.bg_image,
                                               settings.WINDOW_SIZE)

        self.selectionBg = misc.rescaleSurface(
            pygame.image.load(
                os.path.join(settings.PARENT_PATH, "AA_images",
                             "fond_rankings.png")), (None, 610))

        # keep an untouched base to restore every frame
        self._selectionBg_base = self.selectionBg.copy()

        self.trackChoices = [
            musicTrack.TrackBeatMap(track)
            for track in list(musicTrack.GameTracks)
        ]
        self.albumCovers = [
            misc.rescaleSurface(pygame.image.load(track.albumCoverFile),
                                (400, None)) for track in self.trackChoices
        ]
        self.currentChoice = 0

    def initScene(self):
        super().initScene()
        # Music can be played here if desired

    def loopScene(self, events: list[pygame.event.Event]):
        # Draw background
        self._mainApp.blit(self.bg_image, (0, 0))

        titre = fontManager.upheaval("Choix de la chanson", 75, (255, 204, 37))
        self._mainApp.blit(
            titre,
            titre.get_rect(center=(self._mainApp.get_rect().centerx, 60)))

        # restore a clean panel each frame then draw the dynamic content onto it
        panel = self._selectionBg_base.copy()

        currentAlbumCover = self.albumCovers[self.currentChoice]
        panel.blit(
            currentAlbumCover,
            currentAlbumCover.get_rect(center=(panel.get_rect().centerx, 260)))

        currentTrack = self.trackChoices[self.currentChoice]
        songTitle = fontManager.upheaval(
            f"{currentTrack.songName} ({currentTrack.songBPM} BPM)", 35,
            (255, 255, 255))
        panel.blit(songTitle,
                   songTitle.get_rect(center=(panel.get_rect().centerx, 500)))

        songArtist = fontManager.upheaval(currentTrack.songArtist, 25,
                                          (255, 255, 255))
        panel.blit(songArtist,
                   songArtist.get_rect(center=(panel.get_rect().centerx, 530)))

        # finally blit the composed panel
        self._mainApp.blit(
            panel,
            panel.get_rect(center=(self._mainApp.get_rect().centerx, 400)))

        for i in range(2):
            btns = self._inputManager.getBtnsPressed(i)
            axes = self._inputManager.getAxesActive(i)

            if inputManager.AxisInputs.X_LEFT in axes:
                self._sounds["option"].play()
                self.currentChoice = (self.currentChoice - 1) % len(
                    self.trackChoices)
            if inputManager.AxisInputs.X_RIGHT in axes:
                self._sounds["option"].play()
                self.currentChoice = (self.currentChoice + 1) % len(
                    self.trackChoices)

            if inputManager.ButtonInputs.START in btns:
                self._sounds["confirm"].play()
                self.sceneFinished = True

        self._mainApp.blit(self._icons["joystick"],
                           (20, settings.WINDOW_SIZE[1] - 60))

        self._mainApp.blit(self._icons["start"],
                           (220, settings.WINDOW_SIZE[1] - 60))

        self._mainApp.blit(self._icons["select"],
                           (420, settings.WINDOW_SIZE[1] - 60))

        # Call parent loop to handle input and quitting
        return super().loopScene(events)

    def getTransition(self) -> sceneClass.Scene | None:
        return gameScene.GameScene(self._mainApp, self._inputManager,
                                   self._musicManager, self._dbManager,
                                   self.trackChoices[self.currentChoice],
                                   self.players)
