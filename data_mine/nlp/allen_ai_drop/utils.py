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


def serialize_date(date):
    """
    Computes the string representation of a date object composed of "day",
    "month", and "year". The argument is a Python dictionary. Example:
    {
        "day": "24",
        "month": "September",
        "year" "1985"
    }
    This would lead to the following output: "24 September 1985".
    Empty fields (day, month or year) are ignored. The only allowed date
    fields are "day", "month" and "year".

    Returns the string representation of the date object.
    """
    assert(set(date.keys()) <= set(["day", "month", "year"]))
    date = date.items()
    date = filter(lambda item: item[1] is not None, date)
    date = filter(lambda item: len(str(item[1])) > 0, date)
    date = [str(item[1]) for item in sorted(date)]
    return " ".join(date)
