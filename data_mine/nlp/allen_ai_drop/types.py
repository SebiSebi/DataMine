from enum import Enum, unique


@unique
class DROPType(Enum):
    TRAIN = 1
    DEV = 2
