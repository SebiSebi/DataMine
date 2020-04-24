import os

from .constants import DROP_CACHE_DIR
from .types import DROPType


def type_to_data_file(drop_type):
    """
    Computes the path of the DROP data file given the type.

    Each DROP type has the corresponding data located in one file.
    """
    assert(isinstance(drop_type, DROPType))
    data_dir = os.path.join(DROP_CACHE_DIR, "drop_dataset")
    return {
            DROPType.TRAIN: os.path.join(data_dir, "drop_dataset_train.json"),
            DROPType.DEV: os.path.join(data_dir, "drop_dataset_dev.json"),
    }[drop_type]
