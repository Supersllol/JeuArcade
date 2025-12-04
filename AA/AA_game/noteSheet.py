from __future__ import annotations

import pygame

from AA.AA_utils import misc, settings, timer, fontManager, inputManager
from AA.AA_game import musicTrack

noteColors = {
    0: (213, 0, 0),
    1: (0, 28, 218),
    2: (0, 211, 43),
    3: (255, 240, 0)
}


def getLaneCenterXPos(sheetWidth: int, laneID: int):
    xGap = (sheetWidth - settings.NOTE_RADIUS * 8) / 5
    return (xGap + settings.NOTE_RADIUS +
            (xGap + settings.NOTE_RADIUS * 2) * laneID)


class NoteIndicator:

    def __init__(self, mainSheet: pygame.Surface, laneID: int):
        self._active = False
        self._mainSheet = mainSheet
        self._laneID = laneID
        self._coords = (getLaneCenterXPos(mainSheet.get_width(),
                                          laneID), settings.HIT_HEIGHT)
        self._activeTimer = timer.Timer()

    def setActive(self):
        self._active = True
        self._activeTimer.restart()

    def update(self):
        if self._active and self._activeTimer.elapsed(
        ) >= settings.TIME_ACTIVE_NOTE_INDICATOR:
            self._active = False
            self._activeTimer.stop()
        currentColor = (189, 0, 0) if self._active else (165, 164, 164)
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


class NoteSheet:

    def __init__(self, playerID: int, playerHalf: pygame.Surface):
        self._playerID = playerID
        self._playerHalf = playerHalf

        self._mainSheet = pygame.Surface((250, 684), pygame.SRCALPHA)

        self._noteIndicators = [
            NoteIndicator(self._mainSheet, i) for i in range(4)
        ]

    def _drawNotes(self, noteSection: musicTrack.TrackSection,
                   musicElapsedTime: float):
        for lane in noteSection.lanes:
            for note in lane.notes:
                calculatedYPos = settings.HIT_HEIGHT - (
                    (note.timestamp - musicElapsedTime) * settings.NOTE_SPEED)
                if calculatedYPos < (0 - settings.NOTE_RADIUS):
                    break
                misc.pixel_ring(
                    self._mainSheet,
                    noteColors[lane.laneID],
                    (getLaneCenterXPos(self._mainSheet.get_width(),
                                       lane.laneID), calculatedYPos),
                    settings.NOTE_RADIUS,
                    thickness=0)

    def update(self, noteSection: musicTrack.TrackSection,
               musicElapsedTime: float):
        self._mainSheet.fill((0, 0, 0, 100))

        self._drawNotes(noteSection, musicElapsedTime)

        for noteIndicator in self._noteIndicators:
            noteIndicator.update()

        misc.placeSurfaceInHalf(self._playerID, self._mainSheet,
                                self._playerHalf, (365, 0))
