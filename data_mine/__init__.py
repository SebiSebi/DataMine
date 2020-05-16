from __future__ import absolute_import

__author__ = """Pirtoaca George-Sebastian (sebisebi)"""
__email__ = 'gpirtoaca@gmail.com'
__version__ = '0.0.8'


from .collection import Collection

# Quick dataset loader methods.
def RACE(*args, **kwargs):
    from data_mine.nlp.RACE import RACEDataset
    return RACEDataset(*args, **kwargs)


def ALLEN_AI_DROP(*args, **kwargs):
    from data_mine.nlp.allen_ai_drop import DROPDataset
    return DROPDataset(*args, **kwargs)


def CSQA(*args, **kwargs):
    from data_mine.nlp.CSQA import CSQADataset
    return CSQADataset(*args, **kwargs)


def ALLEN_AI_OBQA(*args, **kwargs):
    from data_mine.nlp.allen_ai_obqa import OBQADataset
    return OBQADataset(*args, **kwargs)


def HOTPOT_QA(*args, **kwargs):
    from data_mine.nlp.hotpot_qa import HotpotQADataset
    return HotpotQADataset(*args, **kwargs)


def COSMOS_QA(*args, **kwargs):
    from data_mine.nlp.cosmos_qa import CosmosQADataset
    return CosmosQADataset(*args, **kwargs)
