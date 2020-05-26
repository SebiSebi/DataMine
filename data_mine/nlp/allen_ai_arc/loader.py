import json
import os
import pandas as pd

from data_mine import Collection
from data_mine.zookeeper import check_shallow_integrity, download_dataset
from six import string_types
from .types import ARCType


def ARCDataset(arc_type):
    """
    Loads an ARC dataset given the partition (see the ARCType enum).
    Any error during reading will generate an exception.

    Returns a Pandas DataFrame with 5 columns:
    * 'article': string
    * 'question': string
    * 'answers': list[string], length = 4
    * 'correct': oneof('A', 'B', 'C', D')
    * 'id': string

    TODO(sebisebi): verify
    """
    assert(isinstance(arc_type, ARCType))
    download_dataset(Collection.ALLEN_AI_ARC, check_shallow_integrity)
    raise NotImplementedError()
