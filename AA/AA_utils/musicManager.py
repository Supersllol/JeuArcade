from __future__ import annotations

import pygame
from AA.AA_utils import timer


class MusicManager:

    def __init__(self):
        self._musicTimer = timer.Timer()
        self._musicTimer.stop()

    def play(self, song: str, startSeconds: float, fadeinMs: int = 0):
        pygame.mixer.music.load(song)
        # pygame.mixer.music.play(0, startSeconds, fadeinMs)
        pygame.mixer.music.play(0, startSeconds)
        self._musicTimer.setAndStart(startSeconds)

    def fadeout(self, fadeoutMs: int):
        pygame.mixer.music.fadeout(fadeoutMs)

    def stop(self):
        pygame.mixer.music.stop()
        self._musicTimer.stop()

    def getMusicElapsedSeconds(self):
        return self._musicTimer.elapsed()

    def prepareSection(self, startSeconds: float, prepareTime: float):
        self._musicTimer.setAndStart(startSeconds - prepareTime)

    def isMusicRunning(self):
        return self._musicTimer.isRunning()
