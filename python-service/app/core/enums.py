from enum import Enum 

class PlayerFilterSet(str, Enum):
    ALL = "all"
    ACTIVE = "active"
    INACTIVE = "inactive"

class PlayerStatSet(str, Enum):
    REGULAR = "regular"
    CAREER = "career"
