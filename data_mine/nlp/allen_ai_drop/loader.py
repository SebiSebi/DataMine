from data_mine import Collection
from data_mine.zookeeper import check_shallow_integrity, download_dataset

from .types import DROPType


def DROPDataset(drop_type):
    """
    TODO(sebisebi): add description
    """
    assert(isinstance(drop_type, DROPType))
    download_dataset(Collection.ALLEN_AI_DROP, check_shallow_integrity)
    raise NotImplementedError("TODO: parse and return a DF")
