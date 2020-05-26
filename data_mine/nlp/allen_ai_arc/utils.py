import os

from .constants import ARC_CACHE_DIR
from .types import ARCType


def type_to_data_file(arc_type):
    """
    Computes the path of the ARC data file given the type.

    Each ARC split has the corresponding data located in one file.
    """
    assert(isinstance(arc_type, ARCType))
    data_dir = os.path.join(ARC_CACHE_DIR, "ARC-V1-Feb2018-2")
    split, category = tuple(arc_type.name.lower().split("_"))

    category = "ARC-{}".format(category.capitalize())
    split = "{}-{}".format(category, split.capitalize())
    basename = split + ".jsonl"

    return os.path.join(data_dir, category, basename)
