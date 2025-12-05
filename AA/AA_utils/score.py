from enum import Enum, auto


class HitType(Enum):
    Merveilleux = auto()
    Parfait = auto()
    Bien = auto()
    Bon = auto()
    Manqué = auto()
    Précoce = auto()


hitChiScore = {
    HitType.Merveilleux: 500,
    HitType.Parfait: 400,
    HitType.Bien: 150,
    HitType.Bon: 0,
    HitType.Manqué: -250,
    HitType.Précoce: -250
}

hitTimeOffsets = {
    -0.2: HitType.Manqué,
    0.015: HitType.Merveilleux,
    0.04: HitType.Parfait,
    0.08: HitType.Bien,
    0.15: HitType.Bon,
    0.2: HitType.Précoce
}

sortedHitTimeOffsets = sorted(list(hitTimeOffsets.keys()))


def wasNoteMissed(beatOffset: float):
    missedOffset = sortedHitTimeOffsets[0]
    return beatOffset <= missedOffset


def getHitType(beatOffset: float):
    # print(beatOffset)
    if abs(beatOffset) >= sortedHitTimeOffsets[-1]:
        return HitType.Précoce

    for thresholdTime in sortedHitTimeOffsets[1:-1]:
        if abs(beatOffset) < thresholdTime:
            return hitTimeOffsets[thresholdTime]

    return HitType.Manqué
