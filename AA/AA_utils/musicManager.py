from __future__ import annotations

import pygame
from AA.AA_utils import timer


class MusicManager:

    def __init__(self):
        self._musicTimer = timer.Timer()

    def play(self, song: str, startSeconds: float):
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(0, startSeconds)
        self._musicTimer.restart()

    def fadeout(self, fadeoutMs: int):
        pygame.mixer.music.fadeout(fadeoutMs)

    def stop(self):
        pygame.mixer.music.stop()
        self._musicTimer.stop()

    def getMusicElapsedSeconds(self):
        return self._musicTimer.elapsed()

    def prepareSection(self, startSeconds: float, prepareTime: float):
        self._musicTimer.setAndStart(startSeconds - prepareTime)
