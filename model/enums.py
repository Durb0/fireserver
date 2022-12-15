from enum import Enum

class PositionCard(Enum):
    BASE = "BASE"
    MID = "MID"
    END = "END"
    BRIEF = "BRIEF"

class RelationLevel(Enum):
    CRITICAL_SUCCESS = 20
    SUCCESS = 10
    FAILURE = -10
    CRITICAL_FAILURE = -20
    REFUSAL = -15
    CRITICAL_REFUSAL = -30

    def get(str: str):
        if str == "CRITICAL_SUCCESS":
            return RelationLevel.CRITICAL_SUCCESS
        elif str == "SUCCESS":
            return RelationLevel.SUCCESS
        elif str == "FAILURE":
            return RelationLevel.FAILURE
        elif str == "CRITICAL_FAILURE":
            return RelationLevel.CRITICAL_FAILURE
        elif str == "REFUSAL":
            return RelationLevel.REFUSAL
        elif str == "CRITICAL_REFUSAL":
            return RelationLevel.CRITICAL_REFUSAL
        else:
            print("Error in RelationLevel.get()")
            return None

    def intToStr(int: int):
        if int == 20:
            return "CRITICAL_SUCCESS"
        elif int == 10:
            return "SUCCESS"
        elif int == -10:
            return "FAILURE"
        elif int == -20:
            return "CRITICAL_FAILURE"
        elif int == -15:
            return "REFUSAL"
        elif int == -30:
            return "CRITICAL_REFUSAL"
        else:
            print("Error in RelationLevel.intToStr()")
            return None
