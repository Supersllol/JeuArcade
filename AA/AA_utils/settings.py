from __future__ import annotations

import os

FRAMERATE = 60
WINDOW_SIZE = (1024, 768)

PARENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NOTE_SPEED = 300  # px/s
NOTE_HIT_HEIGHT = 600
NOTE_RADIUS = 25
DEAD_NOTE_FADEOUT = 0.15
TIME_NOTE_HITTABLE = -1.25

SONG_FADE_TIME_S = 0.5
GAME_START_DELAY = 1.5

NOTE_INDICATOR_TIME_ACTIVE = 0.15
