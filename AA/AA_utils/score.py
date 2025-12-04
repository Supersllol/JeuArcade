from enum import Enum, auto


class HitType(Enum):
    Merveilleux = auto()
    Parfait = auto()
    Bien = auto()
    Bon = auto()
    Manqué = auto()


hitChiScore = {
    HitType.Merveilleux: 500,
    HitType.Parfait: 400,
    HitType.Bien: 200,
    HitType.Bon: 0,
    HitType.Manqué: -250
}

hitTimeOffsets = {
    0.02: HitType.Merveilleux,
    0.04: HitType.Parfait,
    0.08: HitType.Bien,
    0.15: HitType.Bon,
    0.2: HitType.Manqué
}


def getHitType(beatOffset: float, checkAbsoluteTiming: bool = True):
    if checkAbsoluteTiming: beatOffset = abs(beatOffset)
    for thresholdTime in sorted(list(hitTimeOffsets.keys())):
        if beatOffset < thresholdTime:
            return hitTimeOffsets[thresholdTime]

    return HitType.Manqué
