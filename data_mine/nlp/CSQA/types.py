from enum import Enum, unique


@unique
class CSQAType(Enum):
    TRAIN = 1
    DEV = 2
    TEST = 3
