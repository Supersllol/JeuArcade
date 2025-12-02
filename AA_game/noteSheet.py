import pygame
from typing import List
from AA_utils import misc, settings, timer, inputManager
from AA_game import musicTrack

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
        misc.pixel_ring(self._mainSheet,
                        "red" if self._active else "white",
                        self._coords,
                        settings.NOTE_RADIUS,
                        thickness=3)


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
        # for lane in noteSection.lanes:
        #     for note in lane.notes:
        note = noteSection.lanes[3].notes[0]
        calculatedYPos = settings.HIT_HEIGHT - (
            (note.timestamp - musicElapsedTime) * settings.NOTE_SPEED)
        pygame.draw.circle(self._mainSheet, "blue", (getLaneCenterXPos(
            self._mainSheet.get_width(), 3), calculatedYPos), 10)

    def update(self, noteSection: musicTrack.TrackSection,
               musicElapsedTime: float):
        self._mainSheet.fill("#0000006E")

        self._drawNotes(noteSection, musicElapsedTime)

        for noteIndicator in self._noteIndicators:
            noteIndicator.update()

        misc.placeSurfaceInHalf(self._playerID, self._mainSheet,
                                self._playerHalf, (365, 0))
