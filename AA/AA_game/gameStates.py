from __future__ import annotations

from enum import Enum, auto


class GameState(Enum):
    PRE_COUNTDOWN_DELAY = auto()
    MUSIC_COUNTDOWN = auto()
    PLAY_SECTION = auto()
    WAIT_FOR_ATTACK = auto()
    FIGHT_SCENE = auto()
    END = auto()


class FightState(Enum):
    INITIAL_DELAY = auto()
    TURN_TO_MIDDLE = auto()
    MOVE_TO_MIDDLE = auto()
    WAIT_BEFORE_ATTACK = auto()


statesAllowMoves = [GameState.MUSIC_COUNTDOWN, GameState.PLAY_SECTION]
