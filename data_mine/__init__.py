from __future__ import absolute_import

__author__ = """Pirtoaca George-Sebastian (sebisebi)"""
__email__ = 'gpirtoaca@gmail.com'
__version__ = '0.0.1'


from .collection import Collection

# Quick dataset loader methods.
def RACE(*args, **kwargs):
    from data_mine.nlp.RACE import RACEDataset
    return RACEDataset(*args, **kwargs)
