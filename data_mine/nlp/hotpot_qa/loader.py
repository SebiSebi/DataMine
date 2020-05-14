from data_mine import Collection
from data_mine.zookeeper import check_shallow_integrity, download_dataset
from .types import HotpotQAType


def HotpotQADataset(hotpot_qa_type):
    """
    TODO(sebisebi): add description
    """
    assert(isinstance(hotpot_qa_type, HotpotQAType))
    download_dataset(Collection.HOTPOT_QA, check_shallow_integrity)
    raise NotImplementedError("HOTPOT_QA loader not implemented.")
