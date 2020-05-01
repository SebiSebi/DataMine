from data_mine import Collection
from data_mine.zookeeper import check_shallow_integrity, download_dataset
from .types import OBQAType


def OBQADataset(obqa_type):
    """
    TODO(sebisebi): add description
    """
    assert(isinstance(obqa_type, OBQAType))
    download_dataset(Collection.ALLEN_AI_OBQA, check_shallow_integrity)
    raise NotImplementedError("TODO(sebisebi): implement")
