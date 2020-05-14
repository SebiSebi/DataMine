from enum import Enum, unique


@unique
class HotpotQAType(Enum):
    TRAIN = 1
    DEV_DISTRACTOR = 2
    DEV_FULLWIKI = 3
    TEST_FULLWIKI = 4
