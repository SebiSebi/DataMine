# AI2 Reasoning Challenge (ARC)


Dataset description
-------------------

The `ARC` dataset consists of 7787 science exam questions drawn from a variety
of sources, including science questions provided under license by a research
partner affiliated with AI2. These are text-only, English language exam
questions that span several grade levels as indicated in the files. Each
question has a multiple choice structure (typically 4 answer options). The
questions are sorted into a `Challenge` set of 2590 "hard" questions (those
that both a retrieval and a co-occurrence method fail to answer correctly) and
an `Easy` set of 5197 questions. Each are pre-split into train, development
and test sets.

* [Paper](https://arxiv.org/pdf/1803.05457.pdf)
* [ARC baselines](https://github.com/allenai/arc-solvers)
* [ARC Easy Leaderboard](https://leaderboard.allenai.org/arc_easy/submissions/public)
* [ARC Challenge Leaderboard](https://leaderboard.allenai.org/arc/submissions/public)


How to use
----------

```python
import data_mine as dm

from data_mine.nlp.allen_ai_arc import ARCType


def main():
    df = dm.ALLEN_AI_ARC(ARCType.TEST_EASY)
    print(df)  # Shows something similar to the example below.


if __name__ == "__main__":
    main()
```

The following ARC types (splits) are available:
1. `TRAIN_EASY`
2. `TRAIN_CHALLENGE`
3. `DEV_EASY`
4. `DEV_CHALLENGE`
5. `TEST_EASY`
6. `TEST_CHALLENGE`


Scheme (ARC DataFrame)
-----------------------

The loading function (`data_mine.nlp.allen_ai_arc.ARCDataset` or `dm.dm.ALLEN_AI_ARC`)
returns a `Pandas DataFrame` with the following columns:
* `id`: string (defined by the `ARC` dataset, passed through unmodified);
* `question`: string;
* `answers`: list[string], length between 3 and 5;
* `correct`: oneof('A', 'B', 'C', D', 'E', '1', '2', '3', '4')

Example:
```
                         id                                           question                                            answers correct
0            Mercury_417466  Which statement best explains why photosynthes...  [Sunlight is the source of energy for nearly a...       A
1           Mercury_7081673  Which piece of safety equipment is used to kee...  [safety goggles, breathing mask, rubber gloves...       B
2           Mercury_7239733  Meiosis is a type of cell division in which ge...  [brain cells, bone cells, muscle cells, ovary ...       D
3     NYSEDREGENTS_2015_4_8  Which characteristic describes the texture of ...                           [gray, warm, long, soft]       D
4           Mercury_7037258     Which best describes the structure of an atom?  [a lightweight core surrounded by neutral part...       B
...                     ...                                                ...                                                ...     ...
2371        Mercury_7083458  A cut to the skin is treated with antiseptic f...  [an immune response., a bacterial infection., ...       B
2372        Mercury_7030450  Which would be a safe practice to exercise dur...  [using open flames to heat all materials, keep...       C
2373     TIMSS_2003_8_pg101  The shape of the moon appears to change regula...  [The Earth turns on its axis., The Moon turns ...       C
2374        Mercury_7057960  How do the nutrients necessary for plant growt...  [The soil absorbs sunlight., Water filters thr...       C
2375        VASoL_2009_5_34  Which part of a sunflower plant absorbs water ...                    [Roots, Stems, Leaves, Flowers]       A
```
