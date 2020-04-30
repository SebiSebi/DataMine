from data_mine import Collection
from data_mine.zookeeper import check_shallow_integrity, download_dataset
from .types import CSQAType


def CSQADataset(csqa_type):
    """
    TODO(sebisebi): add description
    """
    assert(isinstance(csqa_type, CSQAType))
    download_dataset(Collection.CSQA, check_shallow_integrity)
    raise NotImplementedError("TODO(sebisebi): implement")
