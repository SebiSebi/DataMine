import os

from .constants import OBQA_CACHE_DIR
from .types import OBQAType


def type_to_data_file(obqa_type):
    """
    Computes the path of the OBQA data file given the type.

    Each OBQA type has the corresponding data located in one file.
    """
    assert(isinstance(obqa_type, OBQAType))
    data_dir = os.path.join(
            OBQA_CACHE_DIR,
            "OpenBookQA-V1-Sep2018",
            "Data", "Main"
    )
    return {
            OBQAType.TRAIN: os.path.join(data_dir, "train.jsonl"),
            OBQAType.DEV: os.path.join(data_dir, "dev.jsonl"),
            OBQAType.TEST: os.path.join(data_dir, "test.jsonl")
    }[obqa_type]
