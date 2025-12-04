from __future__ import annotations
import pygame
from AA.AA_utils import countries
from AA.AA_game import noteSheet, musicTrack, sprite, chiBar


class Player:

    def __init__(self,
                 name: str,
                 country: countries.CountryFlags,
                 playerID: int,
                 mainApp: pygame.Surface,
                 cpu: bool = False):
        self._name = name
        self._country = country
        self._chi = 70000
        self._health = 10
        self._playerID = playerID
        self._mainApp = mainApp
        self._cpu = cpu

        self._playerHalf = pygame.Surface(
            ((mainApp.get_width() / 2) + 50, mainApp.get_height()),
            pygame.SRCALPHA)

        self._trackSection: musicTrack.TrackSection

        self._noteSheet = noteSheet.NoteSheet(playerID, self._playerHalf)
        self._chiBar = chiBar.ChiBar(playerID, self._playerHalf)
        self._sprite = sprite.Sprite(playerID, self._playerHalf)

    def loadSection(self, newSection: musicTrack.TrackSection):
        self._trackSection = newSection

    def update(self, musicElapsedTime: float):
        self._playerHalf.fill((0, 0, 0, 0))

        self._noteSheet.update(self._trackSection, musicElapsedTime)
        self._chiBar.update(self._chi)
        self._sprite.update(self._health)

        self._mainApp.blit(
            self._playerHalf,
            self._playerHalf.get_rect(midleft=self._mainApp.get_rect().midleft)
            if self._playerID == 0 else self._playerHalf.get_rect(
                midright=self._mainApp.get_rect().midright))
