import pygame
from enum import Enum, auto
from AA_utils import timer


class MusicManager:

    def __init__(self):
        self._musicTimer = timer.Timer()
        self._songLength = 0

    def play(self, song: str, startSeconds: float):
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(0, startSeconds)
        self._musicTimer.restart()
        self._songLength = pygame.mixer.Sound(song).get_length()

    def fadeout(self, fadeoutMs: int):
        pygame.mixer.music.fadeout(fadeoutMs)

    def stop(self):
        pygame.mixer.music.stop()
        self._musicTimer.stop()

    def getMusicElapsedSeconds(self):
        return self._musicTimer.elapsed()

    def prepareSection(self, startSeconds: float, prepareTime: float):
        self._musicTimer.setAndStart(startSeconds - prepareTime)

    def isSongOver(self):
        return self._musicTimer.elapsed() >= self._songLength
