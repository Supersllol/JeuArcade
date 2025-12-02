import json, math, os
from AA_utils import musicManager, settings, timer, inputManager
from enum import Enum
from typing import List


class GameTracks(Enum):
    I_JUST_DIED_IN_YOUR_ARMS_TONIGHT = "I Just Died In Your Arms Tonight"
    SEMI_CHARMED_LIFE = "Semi-Charmed Life"
    TAKE_ON_ME = "Take On Me"
    WHAT_IS_LOVE = "What Is Love"


class TrackNote:

    def __init__(self, timestamp: float):
        self._timestamp = timestamp
        self._active = False

    @property
    def timestamp(self):
        return self._timestamp

    def __str__(self):
        return f"Note: timestamp: {self.timestamp}"


class NoteLane:

    def __init__(self, notes: List[TrackNote], laneID: int):
        self._notes = notes
        self._laneID = laneID

    @property
    def notes(self):
        return self._notes

    @property
    def laneID(self):
        return self._laneID

    def addNote(self, note: TrackNote):
        self._notes.append(note)

    def __str__(self):
        notes = [str(note) + " " for note in self._notes]
        return f"Lane {self._laneID}: {''.join(notes)}"


class TrackSection:

    def __init__(self, lanes: tuple[NoteLane, ...], start: float, end: float):
        self._lanes = lanes
        self._musicStart = start
        self._musicEnd = end

    @property
    def lanes(self):
        return self._lanes

    @property
    def musicStart(self):
        return self._musicStart

    @property
    def musicEnd(self):
        return self._musicEnd

    def __str__(self):
        lanes = [str(lane) + "\n" for lane in self._lanes]
        return f"{''.join(lanes)}"


class TrackBeatMap:

    def __init__(self, chosenTrack: GameTracks):
        self._audioFile = os.path.join(settings.PARENT_PATH,
                                       f"AA_chansons/{chosenTrack.value}.wav")

        with open(os.path.join(settings.PARENT_PATH,
                               f"AA_chansons/beat-{chosenTrack.value}.json"),
                  "r",
                  encoding="utf8") as file:
            self._beatMap = json.load(file)

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
            sectionEnd = math.inf
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
            lanes[move].addNote(newNote)

        return TrackSection(lanes, sectionStart, sectionEnd)

    @property
    def audioFile(self):
        return self._audioFile
