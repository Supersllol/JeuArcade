from __future__ import annotations

import pygame

from AA.AA_utils import misc, settings, timer, fontManager, inputManager, score
from AA.AA_game import musicTrack, gameStates

noteColors = {
    0: (213, 0, 0),
    1: (0, 28, 218),
    2: (0, 211, 43),
    3: (255, 240, 0)
}

noteSurfaces: dict[tuple[int, int, int], pygame.Surface] = {}

deactivatedNoteSurfaces: dict[tuple[int, int, int, int], pygame.Surface] = {}

noteIndicatorRings: dict[tuple[int, int, int], pygame.Surface] = {}

hittableYCoord = settings.NOTE_HIT_HEIGHT - settings.NOTE_RADIUS + settings.TIME_NOTE_HITTABLE * settings.NOTE_SPEED


class DeactivatedNote:

    def __init__(self, missed: bool, note: musicTrack.TrackNote, laneID: int):
        self._baseNote = note
        self._missed = missed
        self._laneID = laneID
        self._timer = timer.Timer()
        self._timer.restart()

    def isNoteAlive(self):
        return self._timer.elapsed() < settings.DEAD_NOTE_FADEOUT

    def getNoteColor(self):
        baseColor = (255, 255, 255)

        transparency = max(
            0 + (255 * ((settings.DEAD_NOTE_FADEOUT - self._timer.elapsed()) /
                        settings.DEAD_NOTE_FADEOUT)), 0)
        baseColor = (baseColor[0], baseColor[1], baseColor[2],
                     int(transparency))
        return baseColor

    @property
    def baseNote(self):
        return self._baseNote


class NoteIndicator:

    def __init__(self, mainSheet: pygame.Surface, laneID: int,
                 coords: tuple[int, int]):
        self._active = False
        self._mainSheet = mainSheet
        self._laneID = laneID
        self._coords = coords
        self._activeTimer = timer.Timer()

    def setActive(self):
        self._active = True
        self._activeTimer.restart()

    def update(self):
        if self._active and self._activeTimer.elapsed(
        ) >= settings.NOTE_INDICATOR_TIME_ACTIVE:
            self._active = False
            self._activeTimer.stop()
        currentColor = (255, 255, 255) if self._active else (165, 164, 164)
        buttonIndicator = fontManager.upheaval(
            inputManager.moveBindings[self._laneID].name, 25, currentColor)
        self._mainSheet.blit(
            buttonIndicator,
            buttonIndicator.get_rect(center=(self._coords[0],
                                             self._coords[1] - 3)))
        if currentColor not in noteIndicatorRings:
            noteIndicatorRings[currentColor] = misc.pixel_ring(
                currentColor, settings.NOTE_RADIUS, thickness=5)
        self._mainSheet.blit(
            noteIndicatorRings[currentColor],
            noteIndicatorRings[currentColor].get_rect(center=self._coords))


class HitTypeIndicator:

    def __init__(self, mainSheet: pygame.Surface):
        self._mainSheet = mainSheet

        self._textSurface = pygame.Surface((200, 60), pygame.SRCALPHA)
        self._activeTimer = timer.Timer()

    def registerHitType(self, hitType: score.HitType):
        self._textSurface.fill((0, 0, 0, 0))
        txtType = fontManager.upheaval(hitType.name.upper(), 28,
                                       (255, 255, 255))
        self._textSurface.blit(
            txtType,
            txtType.get_rect(center=(self._textSurface.get_width() / 2, 20)))

        txtChiScore = fontManager.upheaval(str(score.hitChiScore[hitType]), 30,
                                           (255, 255, 255))
        self._textSurface.blit(
            txtChiScore,
            txtChiScore.get_rect(center=(self._textSurface.get_width() / 2,
                                         42)))
        self._activeTimer.restart()

    def update(self):
        """Show the hit-type text while its timer is within the total display time,
        otherwise stop the timer and do nothing (no fading)."""
        time = self._activeTimer.elapsed()
        # If the timer expired, stop and don't draw
        if time >= settings.HIT_TYPE_TIME_ACTIVE:
            self._activeTimer.stop()
            self._textSurface.fill((0, 0, 0, 0))
            return

        # Otherwise just blit the pre-rendered surface (full opacity)
        self._mainSheet.blit(
            self._textSurface,
            self._textSurface.get_rect(midtop=(self._mainSheet.get_width() / 2,
                                               625)))


class NoteSheet:

    def __init__(self, playerID: int, playerHalf: pygame.Surface):
        self._playerID = playerID
        self._playerHalf = playerHalf

        self._mainSheet = pygame.Surface((250, 684), pygame.SRCALPHA)
        self._deactivatedNotes: list[DeactivatedNote] = []
        self._hitTypeIndicator = HitTypeIndicator(self._mainSheet)

        self._noteIndicators = [
            NoteIndicator(
                self._mainSheet, i,
                (self.getLaneCenterXPos(i), settings.NOTE_HIT_HEIGHT - 33))
            for i in range(4)
        ]

    def _drawNotes(self, noteSection: musicTrack.TrackSection):
        for lane in noteSection.lanes:
            for note in lane.activeNotes:
                noteColor = noteColors[lane.laneID]
                if noteColor not in noteSurfaces:
                    noteSurfaces[noteColor] = misc.pixel_ring(
                        noteColor, settings.NOTE_RADIUS, thickness=0)
                self._mainSheet.blit(
                    noteSurfaces[noteColor],
                    noteSurfaces[noteColor].get_rect(center=note.sheetPos))

        for deactivatedNote in self._deactivatedNotes:
            noteColor = deactivatedNote.getNoteColor()
            if noteColor not in deactivatedNoteSurfaces:
                deactivatedNoteSurfaces[noteColor] = misc.pixel_ring(
                    noteColor, settings.NOTE_RADIUS, thickness=0)
            self._mainSheet.blit(
                deactivatedNoteSurfaces[noteColor],
                deactivatedNoteSurfaces[noteColor].get_rect(
                    center=deactivatedNote.baseNote.sheetPos))

    def getLaneCenterXPos(self, laneID: int):
        xGap = (self._mainSheet.get_width() - settings.NOTE_RADIUS * 8) / 5
        return int((xGap + settings.NOTE_RADIUS +
                    (xGap + settings.NOTE_RADIUS * 2) * laneID))

    def deactivateNote(self, note: musicTrack.TrackNote, laneID: int,
                       hitType: score.HitType):
        self._hitTypeIndicator.registerHitType(hitType)
        self._deactivatedNotes.append(
            DeactivatedNote(hitType == score.HitType.Manqué, note, laneID))

    def laneBtnPressed(self, laneID: int):
        self._noteIndicators[laneID].setActive()

    def update(self, noteSection: musicTrack.TrackSection,
               gameState: gameStates.GameState):
        if gameState == gameStates.GameState.FIGHT_SCENE or gameState == gameStates.GameState.TIEBREAKER_DELAY or gameState == gameStates.GameState.END:
            self._mainSheet.fill((0, 0, 0, 0))
        else:
            self._mainSheet.fill((0, 0, 0, 100))
            pygame.draw.line(self._mainSheet, (255, 255, 255),
                             (0, hittableYCoord),
                             (self._mainSheet.get_width(), hittableYCoord), 3)
            for noteIndicator in self._noteIndicators:
                noteIndicator.update()

        for id, deactivatedNote in enumerate(self._deactivatedNotes):
            if not deactivatedNote.isNoteAlive():
                self._deactivatedNotes.pop(id)

        self._drawNotes(noteSection)

        self._hitTypeIndicator.update()

        misc.placeSurfaceInHalf(self._playerID, self._mainSheet,
                                self._playerHalf, (365, 0))
