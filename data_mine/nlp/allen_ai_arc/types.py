from enum import Enum, unique


@unique
class ARCType(Enum):
    TRAIN_EASY = 1
    TRAIN_CHALLENGE = 2
    DEV_EASY = 3
    DEV_CHALLENGE = 4
    TEST_EASY = 5
    TEST_CHALLENGE = 6
