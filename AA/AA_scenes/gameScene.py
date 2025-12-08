from __future__ import annotations
from AA.AA_scenes import sceneClass
from AA.AA_utils import fontManager, inputManager, pygameText, musicManager, settings, attackUtils
from AA.AA_game import musicTrack, player, gameStates, animations
from enum import Enum, auto
import pygame, os, math, copy, random


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

        self._fightOrder: list[player.Player] = []

        self._fadeOutStarted = False

        self._gameState = gameStates.GameState.PRE_COUNTDOWN_DELAY
        self._fightState = gameStates.FightState.INITIAL_DELAY

        super().__init__(mainApp, inputManager, musicManager)

    def initScene(self):
        self._gameState = gameStates.GameState.WAIT_FOR_ATTACK
        self._currentTrackSection = self._chosenTrack.getSection(0)

        for player in self._players:
            player.loadSection(copy.deepcopy(self._currentTrackSection))
        super().initScene()

    def _chooseNextSection(self):
        nextSectionID = self._currentTrackSection.ID + 1
        if (nextSectionID + 1) > self._chosenTrack.nbrSections:
            self._gameState = gameStates.GameState.END
            print("end")
        else:
            self._currentTrackSection = self._chosenTrack.getSection(
                nextSectionID)
            self._stateTimer.restart()
            for player in self._players:
                player.moveSprite(settings.SPRITE_BASE_POS, 0)
            self._gameState = gameStates.GameState.PRE_COUNTDOWN_DELAY

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

            # already loaded if section 0
            for player in self._players:
                player.loadSection(copy.deepcopy(self._currentTrackSection))
        self._gameState = gameStates.GameState.MUSIC_COUNTDOWN

    def _chooseFightOrder(self, playersWithAttack: list[player.Player]):
        if len(playersWithAttack) == 1:
            return playersWithAttack
        player0, player1 = playersWithAttack[0], playersWithAttack[1]
        deltaScorePlayer0, deltaScorePlayer1 = player0.currentChi - attackUtils.attackChiThresholds[
            player0.
            attackPressed], player1.currentChi - attackUtils.attackChiThresholds[
                player1.attackPressed]
        if deltaScorePlayer0 == deltaScorePlayer1:
            random.shuffle(playersWithAttack)
            return playersWithAttack

        if deltaScorePlayer0 > deltaScorePlayer1:
            return [player0, player1]

        return [player1, player0]

    def loopScene(self, events: list[pygame.event.Event]):
        currentMusicElapsed = self._musicManager.getMusicElapsedSeconds(
        ) if self._musicManager.isMusicRunning() else -math.inf
        self._mainApp.fill((0, 0, 0))
        self._mainApp.blit(
            self._bgImage,
            self._bgImage.get_rect(center=self._mainApp.get_rect().center))

        currentText: list[pygameText.PygameText] = []

        if self._gameState == gameStates.GameState.PRE_COUNTDOWN_DELAY:
            if self._stateTimer.elapsed() >= settings.PRE_COUNTDOWN_DELAY:
                self._startNextSection()

        elif self._gameState == gameStates.GameState.MUSIC_COUNTDOWN:
            if self._stateTimer.elapsed() >= 3:
                if self._currentTrackSection.ID == 0:
                    self._musicManager.play(self._chosenTrack.audioFile,
                                            self._targetStart)
                self._fadeOutStarted = False
                self._gameState = gameStates.GameState.PLAY_SECTION
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

        elif self._gameState == gameStates.GameState.PLAY_SECTION:
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
                for player in self._players:
                    player.attackPressed = attackUtils.AttackType.PasChoisi
                self._gameState = gameStates.GameState.WAIT_FOR_ATTACK

        elif self._gameState == gameStates.GameState.WAIT_FOR_ATTACK:
            if self._stateTimer.elapsed() >= 3:
                playersWithAttack = [
                    player for player in self._players if
                    (player.attackPressed != attackUtils.AttackType.Rien and
                     player.attackPressed != attackUtils.AttackType.PasChoisi)
                ]
                if len(playersWithAttack) != 0:
                    self._fightOrder = self._chooseFightOrder(
                        playersWithAttack)
                    self._gameState = gameStates.GameState.FIGHT_SCENE
                    self._fightState = gameStates.FightState.INITIAL_DELAY
                    self._stateTimer.restart()
                else:
                    self._chooseNextSection()
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

        elif self._gameState == gameStates.GameState.FIGHT_SCENE:
            if self._fightState == gameStates.FightState.INITIAL_DELAY:
                if self._stateTimer.elapsed() >= settings.FIGHT_DELAY:
                    for player in self._players:
                        player.changeAnimation(
                            animations.PlayerAnimations.TURN_SIDE)

                    self._fightState = gameStates.FightState.TURN_TO_MIDDLE

            elif self._fightState == gameStates.FightState.TURN_TO_MIDDLE:
                if self._players[0].isAnimationFinished():
                    self._stateTimer.restart()
                    for player in self._players:
                        player.moveSprite(settings.SPRITE_FIGHT_POS,
                                          settings.FIGHT_TIME_TO_MIDDLE)
                        player.changeAnimation(
                            animations.PlayerAnimations.WALK)

                    self._fightState = gameStates.FightState.MOVE_TO_MIDDLE

            elif self._fightState == gameStates.FightState.MOVE_TO_MIDDLE:
                if self._stateTimer.elapsed() >= settings.FIGHT_TIME_TO_MIDDLE:
                    for player in self._players:
                        player.changeAnimation(
                            animations.PlayerAnimations.FIGHT)

                    self._stateTimer.restart()
                    self._fightState = gameStates.FightState.WAIT_BEFORE_ATTACK

            elif self._fightState == gameStates.FightState.WAIT_BEFORE_ATTACK:
                if self._stateTimer.elapsed() >= settings.FIGHT_DELAY:
                    self._players.index(self._fightOrder[0])

        for player in self._players:
            player.update(currentMusicElapsed, self._gameState,
                          self._inputManager)

        for txt in currentText:
            self._mainApp.blit(txt.text, txt.position)

        return super().loopScene(events)

    def getTransition(self):
        return super().getTransition()
