from data_mine import Collection
from data_mine.zookeeper import check_shallow_integrity, download_dataset
from .types import TriviaQAType


def TriviaQADataset(trivia_qa_type):
    """
    Loads a TriviaQA dataset given the split (see the TriviaQAType enum).
    Any error during reading will generate an exception.
    """
    assert(isinstance(trivia_qa_type, TriviaQAType))
    download_dataset(Collection.TRIVIA_QA, check_shallow_integrity)
    raise NotImplementedError("Implement TriviaQA")
