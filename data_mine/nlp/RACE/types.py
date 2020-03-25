from enum import Enum, unique


@unique
class RACEType(Enum):
    TRAIN_MIDDLE = 1
    TRAIN_HIGH = 2
    DEV_MIDDLE = 3
    DEV_HIGH = 4
    TEST_MIDDLE = 5
    TEST_HIGH = 6
