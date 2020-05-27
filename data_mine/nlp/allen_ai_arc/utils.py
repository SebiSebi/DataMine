import os

from copy import deepcopy
from six import string_types
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


def valid_choices(labels):
    """
    Returns True/False depending on the labels associated
    with the correct answers. They must be either numerical
    or letters but not both digits and letters.
    """
    for label in labels:
        if not isinstance(label, string_types):
            return False
        if len(label) != 1:
            return False
    labels = tuple(sorted(deepcopy(labels)))
    if not (3 <= len(labels) <= 5):
        return False
    correct = set([
            ("A", "B", "C"),
            ("A", "B", "C", "D"),
            ("A", "B", "C", "D", "E"),
            ("1", "2", "3"),
            ("1", "2", "3", "4")
    ])
    return labels in correct
