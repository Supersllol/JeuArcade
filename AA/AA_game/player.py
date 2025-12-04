from __future__ import annotations
import pygame
from AA.AA_utils import countries, settings, score
from AA.AA_game import noteSheet, musicTrack, sprite, chiBar


class Player:

    def __init__(self,
                 name: str,
                 country: countries.CountryFlags,
                 playerID: int,
                 mainApp: pygame.Surface,
                 cpu: bool = False):
        self._name = name
        self._country = country
        self._chi = 70000
        self._health = 10
        self._playerID = playerID
        self._mainApp = mainApp
        self._cpu = cpu

        self._playerHalf = pygame.Surface(
            ((mainApp.get_width() / 2) + 50, mainApp.get_height()),
            pygame.SRCALPHA)

        self._trackSection: musicTrack.TrackSection

        self._noteSheet = noteSheet.NoteSheet(playerID, self._playerHalf)
        self._chiBar = chiBar.ChiBar(playerID, self._playerHalf)
        self._sprite = sprite.Sprite(playerID, self._playerHalf)

    def loadSection(self, newSection: musicTrack.TrackSection):
        newSection.queueAllNotes()
        for lane in newSection.lanes:
            for note in lane.queuedNotes:
                note._appearTimestamp = note.timingTimestamp - (
                    (settings.NOTE_HIT_HEIGHT + settings.NOTE_RADIUS) /
                    settings.NOTE_SPEED)
        self._trackSection = newSection

    def _registerNoteHit(self, hitType: score.HitType):
        self._chi += score.hitChiScore[hitType]

    def _updateNoteStatus(self, musicElapsedTime: float):
        for lane in self._trackSection.lanes:
            for note in lane.queuedNotes:
                if musicElapsedTime >= note.appearTimestamp:
                    lane.activateNote(lane.queuedNotes.pop(0))
                else:
                    break

            for note in lane.activeNotes:
                if musicElapsedTime - note.timingTimestamp >= settings.MISSED_NOTE_TIME:
                    self._registerNoteHit(score.HitType.Miss)
                    self._noteSheet.deactivateNote(True,
                                                   lane.activeNotes.pop(0),
                                                   lane.laneID)
                calculatedYPos = settings.NOTE_HIT_HEIGHT - (
                    (note.timingTimestamp - musicElapsedTime) *
                    settings.NOTE_SPEED)
                note.sheetPos = (self._noteSheet.getLaneCenterXPos(
                    lane.laneID), calculatedYPos)

    def update(self, musicElapsedTime: float):
        self._playerHalf.fill((0, 0, 0, 0))

        self._updateNoteStatus(musicElapsedTime)

        self._noteSheet.update(self._trackSection)
        self._chiBar.update(self._chi)
        self._sprite.update(self._health)

        self._mainApp.blit(
            self._playerHalf,
            self._playerHalf.get_rect(midleft=self._mainApp.get_rect().midleft)
            if self._playerID == 0 else self._playerHalf.get_rect(
                midright=self._mainApp.get_rect().midright))
