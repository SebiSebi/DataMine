from enum import Enum, unique


@unique
class OBQAType(Enum):
    TRAIN = 1
    DEV = 2
    TEST = 3
