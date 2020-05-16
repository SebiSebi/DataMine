from data_mine import Collection
from data_mine.zookeeper import check_shallow_integrity, download_dataset
from .types import CosmosQAType


def CosmosQADataset(cosmos_qa_type):
    """
    TODO(sebisebi): add description
    """
    assert(isinstance(cosmos_qa_type, CosmosQAType))
    download_dataset(Collection.COSMOS_QA, check_shallow_integrity)
    raise NotImplementedError("COSMOS QA not implemented yet.")
