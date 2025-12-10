from __future__ import annotations

import pygame
from AA.AA_utils import timer


class MusicManager:

    def __init__(self):
        self._musicTimer = timer.Timer()
        self._musicTimer.stop()
        self._currentTrack = None
        self._isLooping = False

    def play(self, song: str, startSeconds: float, fadeinMs: int = 0):
        pygame.mixer.music.load(song)
        # pygame.mixer.music.play(0, startSeconds, fadeinMs)
        pygame.mixer.music.play(0, startSeconds)
        self._musicTimer.setAndStart(startSeconds)
        self._currentTrack = song
        self._isLooping = False

    def playLooping(self, song: str, startSeconds: float = 0.0, volume: float = 0.5):
        """Play a track that loops indefinitely (for menu music)"""
        pygame.mixer.music.load(song)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1, startSeconds)  # -1 means loop indefinitely
        self._musicTimer.setAndStart(startSeconds)
        self._currentTrack = song
        self._isLooping = True

    def fadeout(self, fadeoutMs: int):
        pygame.mixer.music.fadeout(fadeoutMs)

    def stop(self):
        pygame.mixer.music.stop()
        self._musicTimer.stop()
        self._currentTrack = None
        self._isLooping = False

    def getMusicElapsedSeconds(self):
        return self._musicTimer.elapsed()

    def prepareSection(self, startSeconds: float, prepareTime: float):
        self._musicTimer.setAndStart(startSeconds - prepareTime)

    def isMusicRunning(self):
        return self._musicTimer.isRunning()

    def getCurrentTrack(self):
        """Returns the currently playing track path or None"""
        return self._currentTrack

    def isLooping(self):
        """Returns True if the current track is looping"""
        return self._isLooping

    def setVolume(self, volume: float):
        """Set music volume (0.0 to 1.0)"""
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
