from __future__ import annotations
import pygame, os
from AA.AA_utils import countries, settings, score, inputManager, attackUtils, misc
from AA.AA_game import noteSheet, musicTrack, sprite, chiBar, gameStates


class Player:

    def __init__(self,
                 name: str,
                 country: countries.CountryOptions,
                 playerID: int,
                 mainApp: pygame.Surface,
                 cpu: bool = False):
        self._name = name
        self._country = country
        if playerID == 0:
            self._totalChi = 5000
        else:
            self._totalChi = 5001
        self._currentChi = self._totalChi
        self._health = 10
        self._playerID = playerID
        self._mainApp = mainApp
        self._cpu = cpu
        self._registeredAttack = attackUtils.AttackType.Rien

        self._checkMark = pygame.transform.scale(
            pygame.image.load(
                os.path.join(settings.PARENT_PATH, "AA_images/check.png")),
            (100, 100))
        self._xMark = pygame.transform.scale(
            pygame.image.load(
                os.path.join(settings.PARENT_PATH, "AA_images/x.png")),
            (100, 100))

        self._playerHalf = pygame.Surface(
            ((mainApp.get_width() / 2) + 50, mainApp.get_height()),
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
    def registeredAttack(self):
        return self._registeredAttack

    @registeredAttack.setter
    def attackPressed(self, newVal: attackUtils.AttackType):
        self._registeredAttack = newVal

    @property
    def sprite(self):
        return self._sprite

    def loadSection(self, newSection: musicTrack.TrackSection):
        newSection.queueAllNotes()
        for lane in newSection.lanes:
            for note in lane.queuedNotes:
                note._appearTimestamp = note.timingTimestamp - (
                    (settings.NOTE_HIT_HEIGHT + settings.NOTE_RADIUS) /
                    settings.NOTE_SPEED)
        self._trackSection = newSection

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
                if score.wasNoteMissed(note.timingTimestamp -
                                       musicElapsedTime):

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

        btnsPressed = input.getBtnsPressed(self._playerID)
        for btn in btnsPressed:
            if gameState in gameStates.statesAllowMoves:
                if btn in inputManager.moveBindings.values():
                    self._userHitNote(btn, musicElapsedTime)

            if gameState == gameStates.GameState.WAIT_FOR_ATTACK:
                if btn == inputManager.attackBtn:
                    attackType = attackUtils.getAttackType(self._currentChi)
                    if attackType != attackUtils.AttackType.Rien:
                        self._registeredAttack = attackType

        self._updateNoteStatus(musicElapsedTime)

        self._noteSheet.update(self._trackSection, gameState)
        self._chiBar.update(self._currentChi, self._totalChi)
        self._sprite.update(self._health)

        if gameState == gameStates.GameState.WAIT_FOR_ATTACK:
            if self._registeredAttack == attackUtils.AttackType.Rien:
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
