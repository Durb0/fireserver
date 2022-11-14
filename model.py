from enum import Enum

class RelationLevel(Enum):
    BAD = 1
    GOOD = 2
    NONE = -1

class CardType(Enum):
    INTERVENTION = 1
    INFO = 2
    NONE = -1

class PositionCard(Enum):
    BASE = 0
    MID = 1
    END = 2

class BonusType(Enum):
    FIRE = 1
    SPEED = 2
    ROAD_SECURITY = 3
    CIVIL_SECURITY = 4
    CITERN = 5
    HIGH = 6
    DIVERS = 7
    POPULARITY = 8

class RessourceType(Enum):
    POPULARITY = 1
    FIREFIGHTER = 2
    CHEF = 3
    #trucks types
    GROSPIMPON = 4
    POMPON = 5
    PETITPIMPON = 6