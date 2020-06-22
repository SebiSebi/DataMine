from enum import Enum, unique
from six import string_types


@unique
class Collection(Enum):
    RACE = 1
    ALLEN_AI_DROP = 2
    CSQA = 3  # https://www.tau-nlp.org/commonsenseqa
    ALLEN_AI_OBQA = 4  # https://github.com/allenai/OpenBookQA
    HOTPOT_QA = 5  # https://hotpotqa.github.io/
    COSMOS_QA = 6  # https://wilburone.github.io/cosmos/
    ALLEN_AI_ARC = 7  # https://allenai.org/data/arc
    TRIVIA_QA = 8  # https://nlp.cs.washington.edu/triviaqa/index.html

    @staticmethod
    def from_str(label):
        assert(isinstance(label, string_types))
        value = None
        try:
            value = Collection[label]
        except KeyError:
            pass

        if value is None:
            raise NotImplementedError(
                    "Dataset `{}` is not part of the collection.".format(label)
            )
        return value
