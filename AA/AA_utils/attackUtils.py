from __future__ import annotations

from enum import Enum, auto


class AttackType(Enum):
    PasChoisi = "Pas choisi"
    Rien = "Rien"
    CoupPoing = "COUP DE POING!"
    CoupPied = "COUP DE PIED!"
    DoubleCoupPoing = "DOUBLE COUP DE POING!"
    Hadoken = "HADOKEN !"


attackDamage = {
    AttackType.CoupPoing: 1,
    AttackType.CoupPied: 3,
    AttackType.DoubleCoupPoing: 6,
    AttackType.Hadoken: 10
}


def getAttackType(chiValue: int, attackThresholds: dict[AttackType, int]):
    if chiValue < attackThresholds[AttackType.CoupPoing]:
        return AttackType.Rien
    elif chiValue < attackThresholds[AttackType.CoupPied]:
        return AttackType.CoupPoing
    elif chiValue < attackThresholds[AttackType.DoubleCoupPoing]:
        return AttackType.CoupPied
    elif chiValue < attackThresholds[AttackType.Hadoken]:
        return AttackType.DoubleCoupPoing
    else:
        return AttackType.Hadoken
