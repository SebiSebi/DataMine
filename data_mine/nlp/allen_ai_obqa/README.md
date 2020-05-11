# AllenAI OpenBookQA (OBQA)


Dataset description
-------------------

`OpenBookQA` is a new kind of question-answering dataset modeled after open
book exams for assessing human understanding of a subject. It consists of
5,957 multiple-choice elementary-level science questions (4,957 train,
500 dev, 500 test), which probe the understanding of a small "book" of
1,326 core science facts and the application of these facts to novel
situations. For training, the dataset includes a mapping from each
question to the core science fact it was designed to probe. Answering
`OpenBookQA` questions requires additional broad common knowledge, not
contained in the book. The questions, by design, are answered incorrectly
by both a retrieval-based algorithm and a word co-occurrence algorithm.
Strong neural baselines achieve around 50% on `OpenBookQA`, leaving a large
gap to the 92% accuracy of crowd-workers.

* [Paper](https://www.semanticscholar.org/paper/24c8adb9895b581c441b97e97d33227730ebfdab)
* [OBQA baselines](https://github.com/allenai/OpenBookQA)
* [Leaderboard](https://leaderboard.allenai.org/open_book_qa)


How to use
----------

```python
import data_mine as dm

from data_mine.nlp.allen_ai_obqa import OBQAFacts, OBQAType


def main():
    df = dm.ALLEN_AI_OBQA(OBQAType.TRAIN, with_retrieved_facts=True)
    print(df)  # Shows something similar to the example below.


if __name__ == "__main__":
    main()
```

The following OBQA types are available:
1. `TRAIN`
2. `DEV`
3. `TEST`

Scheme (OBQA DataFrame)
-----------------------

The loading function (`data_mine.nlp.allen_ai_obqa.OBQADataset` or `dm.dm.ALLEN_AI_OBQA`)
returns a `Pandas DataFrame` with the following columns:
* `id`: string (defined by the `OpenBookQA` dataset, passed through unmodified);
* `question`: string;
* `answers`: list[string], length is always 4;
* `correct`: oneof('A', 'B', 'C', D').
* `retrieved_facts`: list[dict], the column is present if and only if the loading
function is called with `with_retrieved_facts` set to `True`.

The `retrieved_facts` column is an array with 4 dictionaries each describing the
retrieved facts supporting the corresponding candidate answer. The retrieved facts
dict for a given answer has the following keys:
* `context`: string - a combination of token based and vector based facts (**recommended**);
* `token_based`: list[string]: a list of facts extracted with `Lucene` (at most 75);
* `vector_based`: list[string]: a list of facts extracted with embeddings (always 75).

The list of facts (both token and vector based) are sorted in decreasing
order of the relevance score (the first fact in the list is the most
relevant). We **recommend** the "context" field to be used. It is a carefully
constructed document concatenating the top 5 token facts, top 5 vector facts and
then interleaving the remaining facts (until about 512 tokens made up the
context). Facts are concatenated using " . " as a separator.

For example, if you want to train a classifier to predict the correct answer
you can use `retrieved_facts[answer_idx]["context"]` as the supporting context
for the answer with index `answer_idx` (0, 1, 2, 3).

Example:
```
           id                                           question                                            answers correct                                    retrieved_facts
0       7-980                         The sun is responsible for  [puppies learning new tricks, children growing...       D  [{'context': 'seasonal changes are made in res...
1       7-584       When standing miles away from Mount Rushmore  [the mountains seem very close, the mountains ...       D  [{'context': 'the stars in the night sky are v...
2       7-870                When food is reduced in the stomach  [the mind needs time to digest, take a second ...       C  [{'context': 'digestion is when stomach acid b...
3       7-321                                          Stars are  [warm lights that float, made out of nitrate, ...       C  [{'context': 'nuclear reactions in stars cause...
4       9-732                    You can make a telescope with a               [straw, Glass, Candle, mailing tube]       D  [{'context': 'Galileo Galilei made improvement...
...       ...                                                ...                                                ...     ...                                                ...
4952  14-1506                     A bulldozer alters the area of        [skyscrapers, the stock market, air, water]       A  [{'context': 'as the amount of rainfall increa...
4953  14-1509  An organism that can survive without the help ...                 [Brewer's yeast, air, sand, sugar]       A  [{'context': 'a single-cell organism can survi...
4954  14-1510  The nimbleness of this animal is a key adaptio...  [the praying mantis, the antelope, the butterf...       B  [{'context': 'some animals move quickly to esc...
4955  14-1511  Birds will have different kinds of beaks depen...  [organisms they hunt, computer, groceries, seven]       A  [{'context': 'birds with beaks of different sh...
4956  14-1512  Harriet wants to know the area of a rectangula...   [a ruler, a compass, a calculator, a protractor]       A  [{'context': 'a seismograph is a kind of tool ...
```

How were the facts retrieved?
-----------------------------

We have used two approaches:

1. **Token based**: we employed `Lucene` to index the set of 1326 facts
using the `EnglishAnalyzer`. Then, for each question and candidate answer
the top 75 facts are retrieved using the query: `question + " " + answer`.
Notice that in some cases, less than 75 facts are actually returned.

2. **Embedding (vector) based**: we used [Sentence Transformers](https://github.com/UKPLab/sentence-transformers)
to build an index of embeddings from the 1326 facts. Then, for each
question and candidate answer the closest 75 embeddings to `emb(question + " " + answer)`
are computed. The `roberta-large-nli-mean-tokens` model has been used
to encode the facts and the queries. Cosine distance has been employed
to measure distances between vectors in the embeddings space.

The code to reproduce the retrieval procedure can be found [here](https://github.com/SebiSebi/DataMine/tree/master/scripts/allen_ai_obqa/retrieval).
