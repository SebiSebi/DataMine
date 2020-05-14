import os

from .constants import HOTPOT_QA_CACHE_DIR
from .types import HotpotQAType


def type_to_data_file(hotpot_qa_type):
    """
    Computes the path of the Hotpot QA data file given the type.

    Each Hotpot QA type has the corresponding data located in one file.
    """
    assert(isinstance(hotpot_qa_type, HotpotQAType))
    data_dir = HOTPOT_QA_CACHE_DIR
    return {
            HotpotQAType.TRAIN: os.path.join(data_dir, "hotpot_train_v1.1.json"),  # noqa: E501
            HotpotQAType.DEV_DISTRACTOR: os.path.join(data_dir, "hotpot_dev_distractor_v1.json"),  # noqa: E501
            HotpotQAType.DEV_FULLWIKI: os.path.join(data_dir, "hotpot_dev_fullwiki_v1.json"),  # noqa: E501
            HotpotQAType.TEST_FULLWIKI: os.path.join(data_dir, "hotpot_test_fullwiki_v1.json")  # noqa: E501
    }[hotpot_qa_type]
