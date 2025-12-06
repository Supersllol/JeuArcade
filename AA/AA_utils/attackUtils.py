from enum import Enum, auto


class AttackType(Enum):
    Rien = auto()
    CoupPoing = auto()
    CoupPied = auto()
    Projection = auto()
    Special = auto()


attackDamage = {
    AttackType.CoupPoing: 1,
    AttackType.CoupPied: 3,
    AttackType.Projection: 6,
    AttackType.Special: 10
}

attackChiThresholds = {
    AttackType.CoupPoing: 5000,
    AttackType.CoupPied: 10000,
    AttackType.Projection: 17500,
    AttackType.Special: 30000
}


def getAttackType(chiValue: int):
    if chiValue < attackChiThresholds[AttackType.CoupPoing]:
        return AttackType.Rien
    elif chiValue < attackChiThresholds[AttackType.CoupPied]:
        return AttackType.CoupPoing
    elif chiValue < attackChiThresholds[AttackType.Projection]:
        return AttackType.CoupPied
    elif chiValue < attackChiThresholds[AttackType.Special]:
        return AttackType.Projection
    else:
        return AttackType.Special
