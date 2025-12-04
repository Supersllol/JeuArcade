from enum import Enum, auto


class GameState(Enum):
    INITIAL_DELAY = auto()
    START_COUNTDOWN = auto()
    PLAY_SECTION = auto()
    WAIT_FOR_ATTACK = auto()
    FIGHT_SCENE = auto()
    RESTART_COUNTDOWN = auto()
    END = auto()


statesAllowMoves = [
    GameState.START_COUNTDOWN, GameState.RESTART_COUNTDOWN,
    GameState.PLAY_SECTION
]
