from __future__ import annotations
from AA_scenes import sceneClass
from AA_utils import settings, inputManager, fontManager, musicManager, pygameText
from AA_game import player, musicTrack
from typing import List, Optional
from enum import Enum, auto
import pygame, os


class GameState(Enum):
    INITIAL_DELAY = auto()
    START_COUNTDOWN = auto()
    PLAY_SECTION = auto()
    WAIT_FOR_ATTACK = auto()
    FIGHT_SCENE = auto()
    RESTART_COUNTDOWN = auto()
    END = auto()


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
        self._currentTrackSection = 0

        self._fadeOutStarted = False

        self._state = GameState.INITIAL_DELAY

        super().__init__(mainApp, inputManager, musicManager)

    def initScene(self):
        self._state = GameState.INITIAL_DELAY
        super().initScene()

    def loopScene(self, events: List[pygame.event.Event]):
        print(self._musicManager.getMusicElapsedSeconds())
        self._mainApp.fill((0, 0, 0))
        self._mainApp.blit(
            self._bgImage,
            self._bgImage.get_rect(center=self._mainApp.get_rect().center))

        currentText: List[pygameText.PygameText] = []

        if self._state == GameState.INITIAL_DELAY:
            if self._stateTimer.elapsed() >= settings.START_DELAY:
                self._stateTimer.restart()
                self._currentTrackSection = 0
                self._musicManager.prepareSection(0, 3)
                for player in self._players:
                    player.loadSection(self._chosenTrack.getSection(0))
                self._state = GameState.START_COUNTDOWN

        elif self._state == GameState.START_COUNTDOWN:
            if self._stateTimer.elapsed() >= 3:
                self._musicManager.play(self._chosenTrack.audioFile, 0)
                self._fadeOutStarted = False
                self._state = GameState.PLAY_SECTION
            else:
                txt = "3"
                if self._stateTimer.elapsed() >= 1:
                    txt = "2"
                if self._stateTimer.elapsed() >= 2:
                    txt = "1"
                txt = fontManager.upheaval(txt, 250, "white")

                currentText.append(
                    pygameText.PygameText(
                        txt,
                        txt.get_rect(
                            center=(self._mainApp.get_rect().centerx,
                                    self._mainApp.get_rect().centery))))

        elif self._state == GameState.PLAY_SECTION:

            if not self._fadeOutStarted and (
                    self._musicManager.getMusicElapsedSeconds()
                    >= (self._chosenTrack.getSection(
                        self._currentTrackSection).musicEnd -
                        settings.FADE_TIME_S)):
                self._fadeOutStarted = True
                self._musicManager.fadeout(settings.FADE_TIME_S * 1000)

            if self._musicManager.isSongOver(
            ) or self._musicManager.getMusicElapsedSeconds(
            ) >= self._chosenTrack.getSection(
                    self._currentTrackSection).musicEnd:
                self._musicManager.stop()
                self._fadeOutStarted = False
                self._state = GameState.WAIT_FOR_ATTACK

        for player in self._players:
            player.update(self._musicManager.getMusicElapsedSeconds())

        for txt in currentText:
            self._mainApp.blit(txt.text, txt.position)

        return super().loopScene(events)

    def getTransition(self):
        return super().getTransition()
