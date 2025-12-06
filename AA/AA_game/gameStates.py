from __future__ import annotations

from enum import Enum, auto


class GameState(Enum):
    PRE_COUNTDOWN_DELAY = auto()
    MUSIC_COUNTDOWN = auto()
    PLAY_SECTION = auto()
    WAIT_FOR_ATTACK = auto()
    FIGHT_SCENE = auto()
    END = auto()


statesAllowMoves = [GameState.MUSIC_COUNTDOWN, GameState.PLAY_SECTION]
