from __future__ import annotations

import pygame, math


class Timer:

    def __init__(self):
        self.running = False
        self.startTime = 0

    def start(self):
        # si ne roule pas déjà commencer le timer en changeant le temps de départ
        if self.running: return
        # get_ticks() retourne le temps actuel en ms
        self.startTime = pygame.time.get_ticks() / 1000.0
        self.running = True

    def stop(self):
        self.running = False

    def isRunning(self):
        return self.running

    def elapsed(self):
        if not self.running: return 0
        # temps écoulé vaut  temps actuel - temps départ
        return (pygame.time.get_ticks() / 1000.0) - self.startTime

    def setAndStart(self, newTime: float):
        self.startTime = (pygame.time.get_ticks() / 1000.0) - newTime
        self.running = True

    def restart(self):
        # recommencer le timer même s'il roulait déjà
        self.running = False
        self.start()
