import os

from .constants import CSQA_CACHE_DIR
from .types import CSQAType


def type_to_data_file(csqa_type):
    """
    Computes the path of the CSQA data file given the type.

    Each CSQA type has the corresponding data located in one file.
    """
    assert(isinstance(csqa_type, CSQAType))
    return {
            CSQAType.TRAIN: os.path.join(CSQA_CACHE_DIR, "train_rand_split.jsonl"),  # noqa: E501
            CSQAType.DEV: os.path.join(CSQA_CACHE_DIR, "dev_rand_split.jsonl"),
            CSQAType.TEST: os.path.join(CSQA_CACHE_DIR, "test_rand_split_no_answers.jsonl"),  # noqa: E501
    }[csqa_type]
