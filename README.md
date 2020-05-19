# Data Mine

<p align="center">
  <img width="42%" height="42%" src="https://github.com/SebiSebi/DataMine/blob/master/images/logo/goldmine_logo_v1.png">
</p>

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/SebiSebi/DataMine/blob/master/LICENSE)
[![Build Status](https://travis-ci.com/SebiSebi/DataMine.svg?branch=master)](https://travis-ci.com/github/SebiSebi/DataMine)
[![codecov](https://codecov.io/gh/SebiSebi/DataMine/branch/master/graph/badge.svg)](https://codecov.io/gh/SebiSebi/DataMine)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/95f452694b2644ca9f30f5d39379de91)](https://www.codacy.com/manual/SebiSebi/DataMine?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SebiSebi/DataMine&amp;utm_campaign=Badge_Grade)

[![Python Versions](https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue)](https://pypi.org/project/data-mine/)


Installation
------------

```bash
pip install data_mine
```


Example usage
-------------

```python
import data_mine as dm

from data_mine.nlp.RACE import RACEType


def main():
    # Load the dataset into a Pandas DataFrame.
    df = dm.RACE(RACEType.DEV_MIDDLE)
    print(df)  # Results in:
    """
                                                    article                                           question                                            answers correct                id
    0     Jess really felt very happy. When he arrived a...    What would happen if Cindy told Jess the truth?  [Jess would go on the camping trip himself., J...       C  1-middle2414.txt
    1     Jess really felt very happy. When he arrived a...       If Jess really bought a sleeping bag,   _  .  [everyone else would also buy one, He would ha...       B  2-middle2414.txt
    2     Jess really felt very happy. When he arrived a...                      From the story we know   _  .  [everybody would go camping in the class, Jess...       B  3-middle2414.txt
    3     Jess really felt very happy. When he arrived a...          Which is the best title for this passage?  [Jess and His School, Jess and His Friends, An...       C  4-middle2414.txt
    4     Have you felt annoyed when a cell phone  rings...   . Elizabeth Lorris Ritter is worried that   _  .  [students are not allowed to bring cellphones,...       A   1-middle758.txt
    ...                                                 ...                                                ...                                                ...     ...               ...
    """

if __name__ == "__main__":
    main()
```


Available datasets
------------------

| Dataset               | Keywords                   | Usage & Detailed Info                   | Example(s)                              |
| --------------------- | -------------------------- | --------------------------------------- | --------------------------------------- |
| `RACE`                | NLP, QA, Multiple Choice   | [Additional information][RACE-Home]     | [RACE Example][RACE-Example-1]          |
| `AllenAI OpenBookQA`  | NLP, QA, Multiple Choice   | [Additional information][OBQA-Home]     | [OBQA Example][OBQA-Example-1]          |
| `HotpotQA`            | NLP, QA, Multi-hop QA      | [Additional information][HotpotQA-Home] | [HotpotQA Example][HotpotQA-Example-1]  |
| `CosmosQA`            | NLP, QA, Multiple Choice   | [Additional information][CosmosQA-Home] | [CosmosQA Example][CosmosQA-Example-1]  |




[RACE-Home]: https://github.com/SebiSebi/DataMine/tree/master/data_mine/nlp/RACE
[RACE-Example-1]: https://github.com/SebiSebi/DataMine/blob/master/examples/nlp/RACE/simple.py
[OBQA-Home]: https://github.com/SebiSebi/DataMine/tree/master/data_mine/nlp/allen_ai_obqa
[OBQA-Example-1]: https://github.com/SebiSebi/DataMine/blob/master/examples/nlp/allen_ai_obqa/simple.py
[HotpotQA-Home]: https://github.com/SebiSebi/DataMine/tree/master/data_mine/nlp/hotpot_qa
[HotpotQA-Example-1]: https://github.com/SebiSebi/DataMine/blob/master/examples/nlp/hotpot_qa/simple.py
[CosmosQA-Home]: https://github.com/SebiSebi/DataMine/tree/master/data_mine/nlp/cosmos_qa
[CosmosQA-Example-1]: https://github.com/SebiSebi/DataMine/blob/master/examples/nlp/cosmos_qa/simple.py
