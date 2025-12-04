from enum import Enum, auto


class HitType(Enum):
    Marvelous = auto()
    Perfect = auto()
    Great = auto()
    Good = auto()
    Miss = auto()


hitChiScore = {
    HitType.Marvelous: 0,
    HitType.Perfect: 0,
    HitType.Great: 0,
    HitType.Good: 0,
    HitType.Miss: -250
}
