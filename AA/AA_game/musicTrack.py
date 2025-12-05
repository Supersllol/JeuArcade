from __future__ import annotations
import json, os, pygame, math
from AA.AA_utils import settings
from enum import Enum


class GameTracks(Enum):
    I_JUST_DIED_IN_YOUR_ARMS_TONIGHT = "I Just Died In Your Arms Tonight"
    SEMI_CHARMED_LIFE = "Semi-Charmed Life"
    TAKE_ON_ME = "Take On Me"
    WHAT_IS_LOVE = "What Is Love"


class TrackNote:

    def __init__(self, timestamp: float):
        self._timingTimestamp = timestamp
        self._appearTimestamp = -math.inf
        self._sheetPos = (0, 0)

    @property
    def timingTimestamp(self):
        return self._timingTimestamp

    @property
    def appearTimestamp(self):
        return self._appearTimestamp

    @property
    def sheetPos(self):
        return self._sheetPos

    @sheetPos.setter
    def sheetPos(self, newPos: tuple[float, float]):
        self._sheetPos = newPos

    def __str__(self):
        return f"Note: timing timestamp: {self.timingTimestamp}, appear timestamp: {self.appearTimestamp}"


class NoteLane:

    def __init__(self, notes: list[TrackNote], laneID: int):
        self._queuedNotes = notes
        self._activeNotes: list[TrackNote] = []
        self._laneID = laneID

    @property
    def queuedNotes(self):
        return self._queuedNotes

    @property
    def activeNotes(self):
        return self._activeNotes

    @property
    def laneID(self):
        return self._laneID

    def queueNote(self, note: TrackNote):
        self._queuedNotes.append(note)

    def activateNote(self, note: TrackNote):
        self._activeNotes.append(note)

    def queueAllNotes(self):
        self._queuedNotes.extend(self._activeNotes)
        self._queuedNotes.sort(key=lambda e: e.timingTimestamp)
        self._activeNotes = []

    def __str__(self):
        queuedNotes = [str(note) + " " for note in self._queuedNotes]
        activeNotes = [str(note) + " " for note in self._activeNotes]
        return f"Lane {self._laneID}: Queued notes: [{''.join(queuedNotes)}], Active notes: [{activeNotes}]"


class TrackSection:

    def __init__(self, ID: int, lanes: tuple[NoteLane, ...], start: float,
                 end: float):
        self._ID = ID
        self._lanes = lanes
        self._musicStart = start
        self._musicEnd = end

    @property
    def ID(self):
        return self._ID

    @property
    def lanes(self):
        return self._lanes

    @property
    def musicStart(self):
        return self._musicStart

    @property
    def musicEnd(self):
        return self._musicEnd

    def queueAllNotes(self):
        for lane in self._lanes:
            lane.queueAllNotes()

    def __str__(self):
        lanes = [str(lane) + "\n" for lane in self._lanes]
        return f"Section start: {self.musicStart}, end: {self.musicEnd}, lanes: {''.join(lanes)}"


class TrackBeatMap:

    def __init__(self, chosenTrack: GameTracks):
        self._audioFile = os.path.join(settings.PARENT_PATH,
                                       f"AA_chansons/{chosenTrack.value}.mp3")

        with open(os.path.join(settings.PARENT_PATH,
                               f"AA_chansons/beat-{chosenTrack.value}.json"),
                  "r",
                  encoding="utf8") as file:
            self._beatMap = json.load(file)
            self._nbrSections = len(self._beatMap["sections"])

    @property
    def nbrSections(self):
        return self._nbrSections

    def getSection(self, sectionID: int):
        lanes = tuple(NoteLane([], i) for i in range(4))
        sectionStart, sectionEnd = (self._beatMap["sections"].get(
            str(sectionID),
            -1), self._beatMap["sections"].get(str(sectionID + 1), -1))
        if sectionStart == -1:
            raise ValueError("Section not in beat map")
        else:
            sectionStart = sectionStart["start"]
        if sectionEnd == -1:
            sectionEnd = self._beatMap["songLength"]
        else:
            sectionEnd = sectionEnd["start"]

        allNotes = self._beatMap["notes"]
        for jsonNote in allNotes:
            time, move = jsonNote["time"], jsonNote["move"]
            if time < sectionStart:
                continue
            if time >= sectionEnd:
                break
            newNote = TrackNote(time)
            lanes[move].queueNote(newNote)

        return TrackSection(sectionID, lanes, sectionStart, sectionEnd)

    @property
    def audioFile(self):
        return self._audioFile
