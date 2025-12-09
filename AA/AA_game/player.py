from __future__ import annotations
import pygame, os, random
from AA.AA_utils import countries, settings, score, inputManager, attackUtils, misc
from AA.AA_game import noteSheet, musicTrack, sprite, chiBar, gameStates, animations


class Player:

    def __init__(self, name: str, country: countries.CountryOptions,
                 playerID: int, mainApp: pygame.Surface):
        self._name = name
        self._country = country
        self._totalChi = 1000000
        self._currentChi = self._totalChi
        self._health = 10
        self._playerID = playerID
        self._mainApp = mainApp
        self._cpu = name == "CPU"
        self._cpuHits: list[list[float]] = [[] for i in range(4)]

        self._savedAttack = attackUtils.AttackType.PasChoisi

        self._checkMark = pygame.transform.scale(
            pygame.image.load(
                os.path.join(settings.PARENT_PATH, "AA_images/check.png")),
            (100, 100)).convert_alpha()
        self._xMark = pygame.transform.scale(
            pygame.image.load(
                os.path.join(settings.PARENT_PATH, "AA_images/x.png")),
            (100, 100)).convert_alpha()

        self._playerHalf = pygame.Surface(
            ((mainApp.get_width() / 2) + 250, mainApp.get_height()),
            pygame.SRCALPHA)

        self._trackSection: musicTrack.TrackSection

        self._noteSheet = noteSheet.NoteSheet(playerID, self._playerHalf)
        self._chiBar = chiBar.ChiBar(playerID, self._playerHalf)
        self._sprite = sprite.Sprite(playerID, name, country, self._playerHalf)

    @property
    def currentChi(self):
        return self._currentChi

    @currentChi.setter
    def currentChi(self, newVal: int):
        self._currentChi = max(newVal, 0)

    @property
    def totalChi(self):
        return self._totalChi

    def addChi(self, value: int):
        if (value + self._currentChi) < 0:
            self._totalChi -= self._currentChi
            self._currentChi = 0
        else:
            self._currentChi += value
            self._totalChi += value

    @property
    def savedAttack(self):
        return self._savedAttack

    @savedAttack.setter
    def savedAttack(self, newVal: attackUtils.AttackType):
        self._savedAttack = newVal

    def useAttack(self):
        self._currentChi -= attackUtils.attackChiThresholds[self._savedAttack]

    def registerEnemyAttack(self, enemyAttack: attackUtils.AttackType):
        self._health -= attackUtils.attackDamage[enemyAttack]

    def moveSprite(self, targetMidtop: tuple[int, int], travelTime: float):
        self._sprite.moveTo(targetMidtop, travelTime)

    def setAnimationManager(self, animManager: animations.AnimationManager):
        self._sprite.setAnimationManager(animManager)

    def changeAnimation(self,
                        newAnimation: animations.PlayerAnimations,
                        loop: bool = False,
                        changeSides: bool = False):
        self._sprite.setAnimation(newAnimation, changeSides, loop)

    def isAnimationFinished(self):
        return self._sprite.currentAnimation.isAnimationFinished()

    def _generateCpuHits(self):
        for lane in self._trackSection.lanes:
            for note in lane.queuedNotes:
                randomHitType = random.choices(
                    list(score.cpuHitTypeWeights.keys()),
                    list(score.cpuHitTypeWeights.values()))[0]
                if randomHitType == score.HitType.Manqué:
                    # skip note to allow it to miss
                    continue
                if randomHitType == score.HitType.Précoce:
                    # get between max hittable time and threshold for bon
                    generatedOffset = random.uniform(
                        settings.TIME_NOTE_HITTABLE,
                        -(score.hitTimeOffsets[score.HitType.Bon]))
                else:
                    if randomHitType == score.HitType.Merveilleux:
                        generatedOffset = 0
                    else:
                        offsetWindowStart = (
                            score.hitTimeOffsets[randomHitType])
                        previousHitType = list(score.hitTimeOffsets.keys()
                                               ).index(randomHitType) - 1
                        offsetWindowFinish = score.hitTimeOffsets[list(
                            score.hitTimeOffsets.keys())[previousHitType]]
                        generatedOffset = (
                            (offsetWindowStart - offsetWindowFinish) /
                            2) + offsetWindowFinish

                        # then randomly pick sign:
                        if random.choice([True, False]):
                            generatedOffset *= -1

                self._cpuHits[lane.laneID].append(note.timingTimestamp +
                                                  generatedOffset)

    def loadSection(self, newSection: musicTrack.TrackSection):
        newSection.queueAllNotes()
        for lane in newSection.lanes:
            for note in lane.queuedNotes:
                note.appearTimestamp = note.timingTimestamp - (
                    (settings.NOTE_HIT_HEIGHT + settings.NOTE_RADIUS) /
                    settings.NOTE_SPEED)
        self._trackSection = newSection
        if self._cpu:
            self._generateCpuHits()

    def _registerNoteHit(self, hitType: score.HitType):
        self.addChi(score.hitChiScore[hitType])

    def _userHitNote(self, btnPressed: inputManager.ButtonInputs,
                     musicElapsedTime: float):
        for lane in self._trackSection.lanes:
            if inputManager.moveBindings[lane.laneID] == btnPressed:
                # TODO: animate player
                self._noteSheet.laneBtnPressed(lane.laneID)
                if len(lane.activeNotes) == 0: return
                closestNote = lane.activeNotes[0]
                deltaTime = musicElapsedTime - closestNote.timingTimestamp
                if deltaTime >= settings.TIME_NOTE_HITTABLE:
                    hitType = score.getHitType(deltaTime)
                    self._registerNoteHit(hitType)
                    self._noteSheet.deactivateNote(lane.activeNotes.pop(0),
                                                   lane.laneID, hitType)

    def _updateNoteStatus(self, musicElapsedTime: float):
        for lane in self._trackSection.lanes:
            for note in lane.queuedNotes:
                if musicElapsedTime >= note.appearTimestamp:
                    lane.activateNote(lane.queuedNotes.pop(0))
                else:
                    break

            for note in lane.activeNotes:
                # negative to allow to check if missed
                if score.wasNoteMissed(musicElapsedTime -
                                       note.timingTimestamp):

                    self._registerNoteHit(score.HitType.Manqué)
                    self._noteSheet.deactivateNote(lane.activeNotes.pop(0),
                                                   lane.laneID,
                                                   score.HitType.Manqué)
                calculatedYPos = settings.NOTE_HIT_HEIGHT - (
                    (note.timingTimestamp - musicElapsedTime) *
                    settings.NOTE_SPEED)
                note.sheetPos = (self._noteSheet.getLaneCenterXPos(
                    lane.laneID), calculatedYPos)

    def update(self, musicElapsedTime: float, gameState: gameStates.GameState,
               input: inputManager.InputManager):
        self._playerHalf.fill((0, 0, 0, 0))

        if self._cpu:
            for id, lane in enumerate(self._cpuHits):
                if len(lane) != 0:
                    if lane[0] <= musicElapsedTime:
                        self._userHitNote(inputManager.moveBindings[id],
                                          musicElapsedTime)
                        lane.pop(0)

        else:
            btnsPressed = input.getBtnsPressed(self._playerID)
            for btn in btnsPressed:
                if gameState in gameStates.statesAllowMoves:
                    if btn in inputManager.moveBindings.values():
                        self._userHitNote(btn, musicElapsedTime)

                if gameState == gameStates.GameState.WAIT_FOR_ATTACK:
                    if btn == inputManager.attackBtn:
                        attackType = attackUtils.getAttackType(
                            self._currentChi)
                        self._savedAttack = attackType

        self._updateNoteStatus(musicElapsedTime)

        self._noteSheet.update(self._trackSection, gameState)
        self._chiBar.update(self._currentChi, self._totalChi)
        self._sprite.update(self._health)

        if gameState == gameStates.GameState.WAIT_FOR_ATTACK:
            if self._cpu and self._savedAttack == attackUtils.AttackType.PasChoisi:
                if random.choice([True, False]):
                    attackType = attackUtils.getAttackType(self._currentChi)
                    self._savedAttack = attackType
                else:
                    self._savedAttack = attackUtils.AttackType.Rien
            if self._savedAttack == attackUtils.AttackType.Rien or self._savedAttack == attackUtils.AttackType.PasChoisi:
                chosenMark = self._xMark
            else:
                chosenMark = self._checkMark
            misc.placeSurfaceInHalf(self._playerID, chosenMark,
                                    self._playerHalf, (365, 450))

        self._mainApp.blit(
            self._playerHalf,
            self._playerHalf.get_rect(midleft=self._mainApp.get_rect().midleft)
            if self._playerID == 0 else self._playerHalf.get_rect(
                midright=self._mainApp.get_rect().midright))
