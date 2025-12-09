from __future__ import annotations
from AA.AA_scenes import sceneClass, rankingsScene
from AA.AA_utils import fontManager, inputManager, pygameText, musicManager, settings, attackUtils, dbManager
from AA.AA_game import musicTrack, player, gameStates, animations
from enum import Enum, auto
import pygame, os, math, copy, random


class GameScene(sceneClass.Scene):

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager,
                 musicManager: musicManager.MusicManager,
                 dbManager: dbManager.DatabaseManager,
                 track: musicTrack.GameTracks, players: tuple[player.Player,
                                                              player.Player]):
        self._players = players
        animManager = animations.AnimationManager()
        for player in self._players:
            player.setAnimationManager(animManager)
        self._playerAttacking = players[0]
        self._bgImage = pygame.transform.scale(
            pygame.image.load(
                os.path.join(settings.PARENT_PATH, "AA_images/dojo.jpg")),
            (1100, 600)).convert()

        self._chosenTrack = musicTrack.TrackBeatMap(track)
        self._currentTrackSectionID = 0
        self._targetStart = 0

        self._fightOrder: list[player.Player] = []

        self._fadeOutStarted = False

        self._gameState = gameStates.GameState.PRE_COUNTDOWN_DELAY
        self._fightState = gameStates.FightState.INITIAL_DELAY
        self._fightText: list[pygameText.PygameText] = []

        self._winner: player.Player
        self._winReason = ""

        self._playerSections = [[
            self._chosenTrack.getSection(j) for i in range(2)
        ] for j in range(self._chosenTrack.nbrSections)]

        super().__init__(mainApp, inputManager, musicManager, dbManager)

    def initScene(self):
        self._gameState = gameStates.GameState.PRE_COUNTDOWN_DELAY

        self._currentTrackSectionID = 0

        for player in self._players:
            player.loadSection(self._playerSections[
                self._currentTrackSectionID][player._playerID])
        super().initScene()

    def _chooseNextSection(self):
        nextSectionID = self._currentTrackSectionID + 1
        if (nextSectionID + 1) > self._chosenTrack.nbrSections:
            player0, player1 = self._players
            if player0._health == player1._health:
                if player0._totalChi == player1.totalChi:
                    self._winner = random.choice(self._players)
                    self._winReason = "CHOIX ALÉATOIRE"
                else:
                    if player0._totalChi > player1.totalChi:
                        self._winner = player0
                    else:
                        self._winner = player1
                    self._winReason = "PAR CHI TOTAL"
            else:
                if player0._health > player1._health:
                    self._winner = player0
                else:
                    self._winner = player1
                self._winReason = "PAR PV"

            self._stateTimer.restart()
            self._gameState = gameStates.GameState.TIEBREAKER_DELAY
        else:
            self._currentTrackSectionID = nextSectionID
            self._stateTimer.restart()
            for player in self._players:
                player.moveSprite(settings.SPRITE_BASE_POS, 0)
                player.changeAnimation(animations.PlayerAnimations.STAND)
            self._gameState = gameStates.GameState.PRE_COUNTDOWN_DELAY

    def _startNextSection(self):
        self._stateTimer.restart()
        if self._currentTrackSectionID == 0:
            self._musicManager.prepareSection(0, 3)
            self._targetStart = 0
        else:
            self._targetStart = min([
                lane.queuedNotes[0].timingTimestamp for lane in
                self._playerSections[self._currentTrackSectionID][0].lanes
            ])
            self._musicManager.play(self._chosenTrack.audioFile,
                                    self._targetStart - 3, 3000)

            # already loaded if section 0
            for player in self._players:
                player.loadSection(self._playerSections[
                    self._currentTrackSectionID][player._playerID])
        self._gameState = gameStates.GameState.MUSIC_COUNTDOWN

    def _chooseFightOrder(self, playersWithAttack: list[player.Player]):
        if len(playersWithAttack) == 1:
            return playersWithAttack
        player0, player1 = playersWithAttack[0], playersWithAttack[1]
        deltaScorePlayer0, deltaScorePlayer1 = player0.currentChi - attackUtils.attackChiThresholds[
            player0.
            savedAttack], player1.currentChi - attackUtils.attackChiThresholds[
                player1.savedAttack]
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
                if self._currentTrackSectionID == 0:
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
                    currentMusicElapsed
                    >= self._playerSections[self._currentTrackSectionID]
                [0].musicEnd - settings.SONG_FADE_TIME_S):
                self._fadeOutStarted = True
                self._musicManager.fadeout(
                    int(settings.SONG_FADE_TIME_S * 1000))

            if currentMusicElapsed >= self._playerSections[
                    self._currentTrackSectionID][
                        0].musicEnd + settings.SECTION_SWITCH_BUFFER_TIME:
                self._musicManager.stop()
                self._fadeOutStarted = False
                self._stateTimer.restart()
                for player in self._players:
                    player.savedAttack = attackUtils.AttackType.PasChoisi
                self._gameState = gameStates.GameState.WAIT_FOR_ATTACK

        elif self._gameState == gameStates.GameState.WAIT_FOR_ATTACK:
            if self._stateTimer.elapsed() >= 3:
                playersWithAttack = [
                    player for player in self._players
                    if (player.savedAttack != attackUtils.AttackType.Rien and
                        player.savedAttack != attackUtils.AttackType.PasChoisi)
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
                                    self._mainApp.get_rect().centery - 70))))
                currentText.append(
                    pygameText.PygameText(
                        txtInstructions,
                        txtInstructions.get_rect(
                            center=(self._mainApp.get_rect().centerx,
                                    self._mainApp.get_rect().centery - 150))))

        elif self._gameState == gameStates.GameState.FIGHT_SCENE:
            if self._fightState == gameStates.FightState.INITIAL_DELAY:
                if self._stateTimer.elapsed() >= settings.FIGHT_DELAY:
                    for player in self._players:
                        player.changeAnimation(
                            animations.PlayerAnimations.TURN_SIDE)

                    self._fightState = gameStates.FightState.TURN_SIDE

            elif self._fightState == gameStates.FightState.TURN_SIDE:
                if self._players[0].isAnimationFinished():
                    self._stateTimer.restart()
                    for player in self._players:
                        player.moveSprite(settings.SPRITE_FIGHT_POS,
                                          settings.FIGHT_TIME_TO_MIDDLE)
                        player.changeAnimation(
                            animations.PlayerAnimations.WALK, True)

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
                    self._playerAttacking = self._fightOrder[0]
                    attackedPlayer = self._players[
                        1 - self._playerAttacking._playerID]
                    if self._playerAttacking.savedAttack == attackUtils.AttackType.Hadoken:
                        # TODO: change to fireball
                        self._playerAttacking.changeAnimation(
                            animations.PlayerAnimations.HADOKEN)
                        self._playerAttacking.moveSprite(
                            settings.HADOKEN_POS, 0)
                        attackedPlayer.changeAnimation(
                            animations.PlayerAnimations.EMPTY)

                    else:
                        if self._playerAttacking.savedAttack == attackUtils.AttackType.CoupPoing:
                            self._playerAttacking.changeAnimation(
                                animations.PlayerAnimations.PUNCH)
                        elif self._playerAttacking.savedAttack == attackUtils.AttackType.CoupPied:
                            self._playerAttacking.changeAnimation(
                                animations.PlayerAnimations.KICK)
                        elif self._playerAttacking.savedAttack == attackUtils.AttackType.DoubleCoupPoing:
                            self._playerAttacking.changeAnimation(
                                animations.PlayerAnimations.DOUBLE_PUNCH)
                        attackedPlayer.changeAnimation(
                            animations.PlayerAnimations.DAMAGE)

                    attackName = fontManager.upheaval(
                        self._playerAttacking.savedAttack.value, 60,
                        (255, 255, 255))

                    self._fightText.append(
                        pygameText.PygameText(
                            attackName,
                            attackName.get_rect(
                                center=(self._mainApp.get_rect().centerx,
                                        175))))

                    self._playerAttacking.useAttack()
                    self._fightState = gameStates.FightState.ATTACK

            elif self._fightState == gameStates.FightState.ATTACK:
                if all(
                    [player.isAnimationFinished()
                     for player in self._players]):

                    attackedPlayer = self._players[
                        1 - self._playerAttacking._playerID]
                    attackedPlayer.registerEnemyAttack(
                        self._playerAttacking.savedAttack)

                    attackDamage = fontManager.upheaval(
                        f"-{attackUtils.attackDamage[self._playerAttacking.savedAttack]} PV",
                        60, (255, 255, 255))
                    self._fightText.append(
                        pygameText.PygameText(
                            attackDamage,
                            attackDamage.get_rect(
                                center=(self._mainApp.get_rect().centerx,
                                        225))))
                    if self._playerAttacking.savedAttack != attackUtils.AttackType.Hadoken:
                        for player in self._players:
                            player.changeAnimation(
                                animations.PlayerAnimations.FIGHT)

                    self._stateTimer.restart()
                    self._fightState = gameStates.FightState.WAIT_REGISTER_ATTACK

            elif self._fightState == gameStates.FightState.WAIT_REGISTER_ATTACK:
                if self._stateTimer.elapsed() >= settings.TIME_ATTACK_REGISTER:
                    self._fightText.clear()

                    self._fightOrder.pop(0)

                    attackedPlayer = self._players[
                        1 - self._playerAttacking._playerID]
                    if attackedPlayer._health <= 0:
                        self._stateTimer.restart()
                        if self._playerAttacking.savedAttack != attackUtils.AttackType.Hadoken:
                            attackedPlayer.changeAnimation(
                                animations.PlayerAnimations.DEAD)
                        self._gameState = gameStates.GameState.END
                        self._winReason = "PAR K.O."
                        self._winner = self._playerAttacking
                    elif len(self._fightOrder) == 0:
                        for player in self._players:
                            player.changeAnimation(
                                animations.PlayerAnimations.TURN_AROUND)
                        self._fightState = gameStates.FightState.TURN_AROUND
                    else:
                        self._stateTimer.restart()
                        self._fightState = gameStates.FightState.WAIT_BEFORE_ATTACK

            elif self._fightState == gameStates.FightState.TURN_AROUND:
                if self._players[0].isAnimationFinished():
                    self._stateTimer.restart()
                    for player in self._players:
                        player.moveSprite(settings.SPRITE_BASE_POS,
                                          settings.FIGHT_TIME_TO_MIDDLE)
                        player.changeAnimation(
                            animations.PlayerAnimations.WALK, True, True)

                    self._fightState = gameStates.FightState.MOVE_TO_START

            elif self._fightState == gameStates.FightState.MOVE_TO_START:
                if self._stateTimer.elapsed() >= settings.FIGHT_TIME_TO_MIDDLE:
                    for player in self._players:
                        player.changeAnimation(
                            animations.PlayerAnimations.TURN_FRONT)

                    self._stateTimer.restart()
                    self._fightState = gameStates.FightState.WAIT_BEFORE_RESTART

            elif self._fightState == gameStates.FightState.WAIT_BEFORE_RESTART:
                if self._players[0].isAnimationFinished():
                    self._chooseNextSection()

            currentText = self._fightText

        elif self._gameState == gameStates.GameState.TIEBREAKER_DELAY:
            if self._stateTimer.elapsed() >= settings.TIEBREAKER_DELAY:
                self._players[1 - self._winner._playerID].changeAnimation(
                    animations.PlayerAnimations.DEAD)
                self._stateTimer.restart()
                self._gameState = gameStates.GameState.END

        elif self._gameState == gameStates.GameState.END:
            gameOver = fontManager.upheaval(f"PARTIE TERMINÉE", 100,
                                            (255, 255, 255))
            gagnant = fontManager.upheaval(f"GAGNANT: {self._winner._name}",
                                           70, (255, 255, 255))
            raison = fontManager.upheaval(f"{self._winReason}", 70,
                                          (255, 255, 255))
            currentText.append(
                pygameText.PygameText(
                    gameOver,
                    gameOver.get_rect(center=(self._mainApp.get_rect().centerx,
                                              110))))
            currentText.append(
                pygameText.PygameText(
                    gagnant,
                    gagnant.get_rect(center=(self._mainApp.get_rect().centerx,
                                             190))))
            currentText.append(
                pygameText.PygameText(
                    raison,
                    raison.get_rect(center=(self._mainApp.get_rect().centerx,
                                            240))))
            if self._stateTimer.elapsed() >= settings.TIMER_END:

                self._sceneFinished = True

        if self._playerAttacking.savedAttack == attackUtils.AttackType.Hadoken:
            attackedPlayer = self._players[1 - self._playerAttacking._playerID]
            attackedPlayer.update(currentMusicElapsed, self._gameState,
                                  self._inputManager)
            self._playerAttacking.update(currentMusicElapsed, self._gameState,
                                         self._inputManager)
        else:
            for player in self._players:
                player.update(currentMusicElapsed, self._gameState,
                              self._inputManager)

        for txt in currentText:
            self._mainApp.blit(txt.text, txt.position)

        return super().loopScene(events)

    def getTransition(self):
        if not self._winner._name == "CPU":
            self._dbManager.addPlayerResult(self._winner, True)
        loser = self._players[1 - self._winner._playerID]
        if not loser._name == "CPU":
            self._dbManager.addPlayerResult(loser, False)

        return rankingsScene.RankingsScene(self._mainApp, self._inputManager,
                                           self._musicManager, self._dbManager,
                                           (self._winner._name, loser._name))
