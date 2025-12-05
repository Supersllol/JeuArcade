from __future__ import annotations

import pygame

from AA.AA_utils import misc, settings, timer, fontManager, inputManager, score
from AA.AA_game import musicTrack, gameStates

noteColors = {
    0: (213, 0, 0, 255),
    1: (0, 28, 218, 255),
    2: (0, 211, 43, 255),
    3: (255, 240, 0, 255)
}

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
        baseColor = list(noteColors[self._laneID]) if self._missed else [
            255, 255, 255, 255
        ]

        transparency = max(
            0 + (255 * ((settings.DEAD_NOTE_FADEOUT - self._timer.elapsed()) /
                        settings.DEAD_NOTE_FADEOUT)), 0)
        baseColor[3] = int(transparency)
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
        misc.pixel_ring(self._mainSheet,
                        currentColor,
                        self._coords,
                        settings.NOTE_RADIUS,
                        thickness=2)


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
        time = self._activeTimer.elapsed()
        total_time = settings.HIT_TYPE_FADE_IN + settings.HIT_TYPE_ACTIVE + settings.HIT_TYPE_FADE_OUT

        if time >= total_time:
            # Animation complete
            transparency = 0
            self._activeTimer.stop()
        elif time >= (settings.HIT_TYPE_FADE_IN + settings.HIT_TYPE_ACTIVE):
            # Fade out phase: go from 255 → 0
            elapsed_fade = time - (settings.HIT_TYPE_FADE_IN +
                                   settings.HIT_TYPE_ACTIVE)
            transparency = int(255 *
                               (1 - elapsed_fade / settings.HIT_TYPE_FADE_OUT))
        elif time >= settings.HIT_TYPE_FADE_IN:
            # Active phase: full opacity
            transparency = 255
        else:
            # Fade in phase: go from 0 → 255
            transparency = int(255 * (time / settings.HIT_TYPE_FADE_IN))

        self._textSurface.set_alpha(transparency)
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
                (self.getLaneCenterXPos(i), settings.NOTE_HIT_HEIGHT))
            for i in range(4)
        ]

    def _drawNotes(self, noteSection: musicTrack.TrackSection):
        for lane in noteSection.lanes:
            for note in lane.activeNotes:
                misc.pixel_ring(self._mainSheet,
                                noteColors[lane.laneID],
                                note.sheetPos,
                                settings.NOTE_RADIUS,
                                thickness=0)

        for deactivatedNote in self._deactivatedNotes:
            misc.pixel_ring(self._mainSheet,
                            deactivatedNote.getNoteColor(),
                            deactivatedNote.baseNote.sheetPos,
                            settings.NOTE_RADIUS,
                            thickness=0)

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
        if gameState == gameStates.GameState.FIGHT_SCENE:
            self._mainSheet.fill((0, 0, 0, 0))
        else:
            self._mainSheet.fill((0, 0, 0, 100))

        for id, deactivatedNote in enumerate(self._deactivatedNotes):
            if not deactivatedNote.isNoteAlive():
                self._deactivatedNotes.pop(id)

        self._drawNotes(noteSection)

        for noteIndicator in self._noteIndicators:
            noteIndicator.update()

        self._hitTypeIndicator.update()

        pygame.draw.line(self._mainSheet, (255, 255, 255), (0, hittableYCoord),
                         (self._mainSheet.get_width(), hittableYCoord), 3)

        misc.placeSurfaceInHalf(self._playerID, self._mainSheet,
                                self._playerHalf, (365, 0))
