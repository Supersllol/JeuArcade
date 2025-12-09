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

attackChiThresholds = {
    AttackType.CoupPoing: 5000,
    AttackType.CoupPied: 10000,
    AttackType.DoubleCoupPoing: 17500,
    AttackType.Hadoken: 30000
}


def getAttackType(chiValue: int):
    if chiValue < attackChiThresholds[AttackType.CoupPoing]:
        return AttackType.Rien
    elif chiValue < attackChiThresholds[AttackType.CoupPied]:
        return AttackType.CoupPoing
    elif chiValue < attackChiThresholds[AttackType.DoubleCoupPoing]:
        return AttackType.CoupPied
    elif chiValue < attackChiThresholds[AttackType.Hadoken]:
        return AttackType.DoubleCoupPoing
    else:
        return AttackType.Hadoken
