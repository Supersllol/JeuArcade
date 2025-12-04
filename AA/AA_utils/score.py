from enum import Enum, auto


class HitType(Enum):
    Marvelous = auto()
    Perfect = auto()
    Great = auto()
    Good = auto()
    Miss = auto()


hitChiScore = {
    HitType.Marvelous: 500,
    HitType.Perfect: 400,
    HitType.Great: 200,
    HitType.Good: 100,
    HitType.Miss: -250
}

hitTimeOffsets = {
    0.02: HitType.Marvelous,
    0.04: HitType.Perfect,
    0.08: HitType.Great,
    0.15: HitType.Good,
    0.2: HitType.Miss
}


def getHitType(beatOffset: float, checkAbsoluteTiming: bool = True):
    if checkAbsoluteTiming: beatOffset = abs(beatOffset)
    for thresholdTime in sorted(list(hitTimeOffsets.keys())):
        if beatOffset < thresholdTime:
            return hitTimeOffsets[thresholdTime]

    return HitType.Miss
