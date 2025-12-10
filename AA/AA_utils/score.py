from __future__ import annotations

from enum import Enum, auto
from AA.AA_utils import settings


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
    HitType.Merveilleux: 0.02,
    HitType.Parfait: 0.04,
    HitType.Bien: 0.08,
    HitType.Bon: 0.15,
}

cpuHitTypeWeights = {
    HitType.Manqué: 0.1,
    HitType.Merveilleux: 0.075,
    HitType.Parfait: 0.175,
    HitType.Bien: 0.4,
    HitType.Bon: 0.15,
    HitType.Précoce: 0.1
}

sortedHitTimeOffsets = sorted(list(hitTimeOffsets.keys()),
                              key=lambda e: hitTimeOffsets[e])


def wasNoteMissed(beatOffset: float):
    return beatOffset > hitTimeOffsets[HitType.Bon]


def getHitType(beatOffset: float):

    for hitType in sortedHitTimeOffsets:
        if abs(beatOffset) < hitTimeOffsets[hitType]:
            return hitType

    return HitType.Précoce
