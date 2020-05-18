import os

from .constants import COSMOS_QA_CACHE_DIR
from .types import CosmosQAType


def type_to_data_file(cosmos_qa_type):
    """
    Computes the path of the Cosmos QA data file given the type.

    Each Cosmos QA type has the corresponding data located in one file.
    """
    assert(isinstance(cosmos_qa_type, CosmosQAType))
    data_dir = COSMOS_QA_CACHE_DIR
    return {
            CosmosQAType.TRAIN: os.path.join(data_dir, "train.jsonl"),
            CosmosQAType.DEV: os.path.join(data_dir, "valid.jsonl"),
            CosmosQAType.TEST: os.path.join(data_dir, "test.jsonl")
    }[cosmos_qa_type]
