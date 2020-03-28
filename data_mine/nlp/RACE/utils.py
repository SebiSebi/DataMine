import os

from .types import RACEType
from .constants import RACE_CACHE_DIR


def next_question_id(next_ids, id_base):
    """
    Incrementally fetches the next question ID based on the base passage ID.

    Some questions have the same ID in the RACE dataset (if they are
    in the same file). We try to make those unique by appending an
    index before the id. @q_ids is used to keep the counter for each
    question ID - it is essentially a map from the file name to the count.
    It will generate ids as follows:

    1) 1-middle1548.txt
    2) 2-middle1548.txt
    3) 3-middle1548.txt
    4) ...

    Use this function to get incremental question IDs.
    """
    index = next_ids.get(id_base, 1)
    next_ids[id_base] = index + 1
    return "{}-{}".format(index, id_base)


def type_to_data_directory(race_type):
    """
    Computes the path of the RACE data directory given the type.

    Each RACE type has a corresponding directory inside the main RACE
    cache directory. For example: DEV_HIGH files can be found under this
    directory: "RACE_CACHE_DIR/RACE/dev/high".
    """
    assert(isinstance(race_type, RACEType))
    path = str(race_type.name).lower().split('_')
    assert(len(path) == 2)
    return os.path.join(RACE_CACHE_DIR, "RACE", path[0], path[1])
