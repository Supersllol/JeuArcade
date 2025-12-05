from __future__ import annotations
from AA.AA_scenes import sceneClass
from AA.AA_utils import fontManager, inputManager, pygameText, musicManager, settings
from AA.AA_game import musicTrack, player, gameStates
from enum import Enum, auto
import pygame, os, math, copy


class GameScene(sceneClass.Scene):

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager,
                 musicManager: musicManager.MusicManager,
                 track: musicTrack.GameTracks, players: tuple[player.Player,
                                                              player.Player]):
        self._players = players
        self._bgImage = pygame.transform.scale(
            pygame.image.load(
                os.path.join(settings.PARENT_PATH, "AA_images/dojo.jpg")),
            (1100, 600))

        self._chosenTrack = musicTrack.TrackBeatMap(track)
        self._currentTrackSection: musicTrack.TrackSection
        self._targetStart = 0

        self._fadeOutStarted = False

        self._state = gameStates.GameState.PRE_COUNTDOWN_DELAY

        super().__init__(mainApp, inputManager, musicManager)

    def initScene(self):
        self._state = gameStates.GameState.PRE_COUNTDOWN_DELAY
        self._currentTrackSection = self._chosenTrack.getSection(0)

        for player in self._players:
            player.loadSection(copy.deepcopy(self._currentTrackSection))
        super().initScene()

    def _startNextSection(self):
        self._stateTimer.restart()
        if self._currentTrackSection.ID == 0:
            self._musicManager.prepareSection(0, 3)
            self._targetStart = 0
        else:
            self._targetStart = min([
                lane.queuedNotes[0].timingTimestamp
                for lane in self._currentTrackSection.lanes
            ])
            self._musicManager.play(self._chosenTrack.audioFile,
                                    self._targetStart - 3, 3000)
        for player in self._players:
            player.loadSection(copy.deepcopy(self._currentTrackSection))
        self._state = gameStates.GameState.MUSIC_COUNTDOWN

    def loopScene(self, events: list[pygame.event.Event]):
        currentMusicElapsed = self._musicManager.getMusicElapsedSeconds(
        ) if self._musicManager.isMusicRunning() else -math.inf
        self._mainApp.fill((0, 0, 0))
        self._mainApp.blit(
            self._bgImage,
            self._bgImage.get_rect(center=self._mainApp.get_rect().center))

        currentText: list[pygameText.PygameText] = []

        if self._state == gameStates.GameState.PRE_COUNTDOWN_DELAY:
            if self._stateTimer.elapsed() >= settings.PRE_COUNTDOWN_DELAY:
                self._startNextSection()

        elif self._state == gameStates.GameState.MUSIC_COUNTDOWN:
            if self._stateTimer.elapsed() >= 3:
                if self._currentTrackSection.ID == 0:
                    self._musicManager.play(self._chosenTrack.audioFile,
                                            self._targetStart)
                self._fadeOutStarted = False
                self._state = gameStates.GameState.PLAY_SECTION
            else:
                txt = fontManager.upheaval(
                    str(3 - int(self._stateTimer.elapsed())), 250,
                    (255, 255, 255))

                currentText.append(
                    pygameText.PygameText(
                        txt,
                        txt.get_rect(
                            center=(self._mainApp.get_rect().centerx,
                                    self._mainApp.get_rect().centery))))

        elif self._state == gameStates.GameState.PLAY_SECTION:
            if not self._fadeOutStarted and (
                    currentMusicElapsed >= self._currentTrackSection.musicEnd -
                    settings.SONG_FADE_TIME_S):
                self._fadeOutStarted = True
                self._musicManager.fadeout(
                    int(settings.SONG_FADE_TIME_S * 1000))

            if currentMusicElapsed >= self._currentTrackSection.musicEnd + settings.SECTION_SWITCH_BUFFER_TIME:
                self._musicManager.stop()
                self._fadeOutStarted = False
                self._stateTimer.restart()
                self._state = gameStates.GameState.WAIT_FOR_ATTACK

        elif self._state == gameStates.GameState.WAIT_FOR_ATTACK:
            if self._stateTimer.elapsed() >= 3:
                nextSectionID = self._currentTrackSection.ID + 1
                if (nextSectionID + 1) > self._chosenTrack.nbrSections:
                    self._state = gameStates.GameState.END
                    print("end")
                else:
                    self._currentTrackSection = self._chosenTrack.getSection(
                        nextSectionID)
                    self._stateTimer.restart()
                    self._state = gameStates.GameState.PRE_COUNTDOWN_DELAY
            else:
                txtCountdown = fontManager.upheaval(
                    str(3 - int(self._stateTimer.elapsed())), 80,
                    (255, 255, 255))

                txtInstructions = fontManager.upheaval("ATTAQUER? (D)", 80,
                                                       (255, 255, 255))

                currentText.append(
                    pygameText.PygameText(
                        txtCountdown,
                        txtCountdown.get_rect(
                            center=(self._mainApp.get_rect().centerx,
                                    self._mainApp.get_rect().centery + 40))))
                currentText.append(
                    pygameText.PygameText(
                        txtInstructions,
                        txtInstructions.get_rect(
                            center=(self._mainApp.get_rect().centerx,
                                    self._mainApp.get_rect().centery - 40))))

        for player in self._players:
            player.update(currentMusicElapsed, self._state, self._inputManager)

        for txt in currentText:
            self._mainApp.blit(txt.text, txt.position)

        return super().loopScene(events)

    def getTransition(self):
        return super().getTransition()
