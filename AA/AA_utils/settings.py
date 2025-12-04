from __future__ import annotations

import os

FRAMERATE = 60
WINDOW_SIZE = (1024, 768)

PARENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NOTE_SPEED = 300  # px/s
NOTE_HIT_HEIGHT = 600
SONG_FADE_TIME_S = 1
GAME_START_DELAY = 0
NOTE_RADIUS = 25
TIME_ACTIVE_NOTE_INDICATOR = 0.25
MISSED_NOTE_TIME = 0.2
DEAD_NOTE_FADEOUT = 0.25
