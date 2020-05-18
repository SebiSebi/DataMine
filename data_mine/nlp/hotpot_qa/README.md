# HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering


Dataset description
-------------------

`HotpotQA` is a question answering dataset featuring natural, multi-hop
questions, with strong supervision for supporting facts to enable more
explainable question answering systems. It is collected by a team of NLP
researchers at `Carnegie Mellon University`, `Stanford University`, and
`Université de Montréal`. `HotpotQA`, is a new dataset with 113k Wikipedia
based question-answer pairs with four key features:
1. The questions require finding and reasoning over **multiple supporting
documents** to answer;
2. The questions are **diverse** and not constrained to any pre-existing
knowledge bases or knowledge schemas;
3. Sentence-level supporting facts required for reasoning are provided,
allowing QA systems to reason with **strong supervision** and explain the
predictions;
4. A new type of **factoid comparison questions** are offered to test QA
systems’ ability to extract relevant facts and perform necessary comparison. 


* [Paper](https://arxiv.org/pdf/1809.09600.pdf)
* [HotpotQA baselines](https://github.com/hotpotqa/hotpot)
* [Leaderboard](https://hotpotqa.github.io/)


How to use
----------

```python
import data_mine as dm

from data_mine.nlp.hotpot_qa import HotpotQAType


def main():
    df = dm.HOTPOT_QA(HotpotQAType.DEV_DISTRACTOR)
    print(df)  # Shows something similar to the example below.


if __name__ == "__main__":
    main()
```

The following HotpotQA types are available:
1. `TRAIN`
2. `DEV_DISTRACTOR`
3. `DEV_FULLWIKI`
7. `TEST_FULLWIKI`


Scheme (HotpotQA DataFrame)
-----------------------

The loading function (`data_mine.nlp.hotpot_qa.HotpotQADataset` or `dm.HOTPOT_QA`)
returns a `Pandas DataFrame` with 8 columns:
* `id`: string, a unique id for the question;
* `question`: string;
* `answer`: string (this is `None` for the test split);
* `gold_paragraphs`: list[string], please read the notes on the gold paragraphs, below. For
the test split, the list is always empty;
* `supporting_facts`: list, where each entry is a list with two elements [`title`, `sent_id`].
The `title` component denotes the title of the paragraph, and `sent_id` denotes the
supporting fact's id (0-based) in this paragraph. For the test split, the list is always empty;
* `context`: list, each entry is a paragraph, which is represented as a list with two
elements [`title`, `sentences`], `sentences` being a list of strings;
* `question_type`: string, oneof(`comparison`, `bridge`) - see the paper for more details. This
is `None` for the test split;
* `question_level`: string, oneof(`easy`, `medium`, `hard`) - see the paper for more details. This
is `None` for the test split.

**Note**: The columns `supporting_facts` and `context` are passed through unaltered from the data
read in the `HotpotQA` files. The gold paragraphs are deduced from those columns but we include
all of them for completeness.

**Note**: You can find important information on the dataset's [webpage](https://github.com/hotpotqa/hotpot).

Example:
```
                            id                                           question                            answer  ...                                            context question_type question_level
0     5a8b57f25542995d1e6f1371  Were Scott Derrickson and Ed Wood of the same ...                               yes  ...  [[Adam Collis, [Adam Collis is an American fil...    comparison           hard
1     5a8c7595554299585d9e36b6  What government position was held by the woman...                 Chief of Protocol  ...  [[A Kiss for Corliss, [A Kiss for Corliss is a...        bridge           hard
2     5a85ea095542994775f606a8  What science fantasy young adult series, told ...                         Animorphs  ...  [[Animorphs, [Animorphs is a science fantasy s...        bridge           hard
3     5adbf0a255429947ff17385a  Are the Laleli Mosque and Esma Sultan Mansion ...                                no  ...  [[Esma Sultan, [Esma Sultan is the name of thr...    comparison           hard
4     5a8e3ea95542995a26add48d  The director of the romantic comedy "Big Stone...  Greenwich Village, New York City  ...  [[Great Eastern Conventions, [Great Eastern Co...        bridge           hard
...                        ...                                                ...                               ...  ...                                                ...           ...            ...
7400  5ab92307554299753720f72d  What Pakistani actor and writer from Islamabad...                     Yasir Hussain  ...  [[Baat Cheet, [Baat Cheet (Urdu: ‎ or French: ...        bridge           hard
7401  5abba3b1554299642a094aed  Are both Volvic and Canfield's Diet Chocolate ...                                no  ...  [[Fudge cookie, [A fudge cookie is a cookie th...    comparison           hard
7402  5a8173fa554299260e20a28e  Are Billy and Barak both breeds of scenthound?...                               yes  ...  [[The Livestock Conservancy, [The Livestock Co...    comparison           hard
7403  5a8caf1d554299585d9e3720  Were both of the following rock groups formed ...                               yes  ...  [[The Strapping Fieldhands, [The Strapping Fie...    comparison           hard
7404  5ac132a755429964131be17c  Blackfin is a family of processors developed b...            Norwood, Massachusetts  ...  [[Arm Holdings, [Arm Holdings (Arm) is a Briti...        bridge           hard

[7405 rows x 8 columns]
```


Note on the gold paragraphs column
----------------------------------

For the distractor setting, the authors of the dataset have retrieved 8
paragraphs from `Wikipedia` as distractors, using the question as the query.
Then, the 2 gold paragraphs (the ones used to collect the question and answer)
are mixed with the 8 distractors to construct the distractor context. The 2
gold paragraphs and the 8 distractors are shuffled before they are mixed
(the `context` column). The 2 gold paragraphs can be recovered by using
provided supporting facts. Each supporting fact is a tuple with two elements
`[title, sent_id]`, where `title` denotes the title of the paragraph, and
`sent_id` denotes the supporting fact's id (0-based) in this paragraph.
A paragraph is a gold paragraph if and only if its title is mentioned in the
supporting facts list (at least once). The other paragraphs are distractors.

**Note**: In the fullwiki setting, we cannot always deduce the gold paragraphs
because the information retrieval may not fetch those paragraphs. More exactly,
the supporting fact list mentions the title `Titanic`, but the `Titanic` paragraph
has not been retrieved by the IR engine.

**Note**: The `DEV_FULLWIKI` is just `DEV_DISTRACTOR` without the gold and distractor
paragraphs, but instead with the top 10 paragraphs obtained using our retrieval system.
Therefore, the only difference is in the `context` column. We cannot always deduce the
gold paragraphs because the IR system may not retrieve them.

:warning: **Warning**: For the `DEV_FULLWIKI` split, the `gold_paragraphs` column may
be incomplete (see the above notes).

:warning: **Warning**: For the `TEST_FILLWIKI` split, the `gold_paragraphs` is always
empty.

The number of gold paragraphs varies depending on the `HotpotQA` type:

* `TRAIN`: always 2 gold paragraphs;
* `DEV_DISTRACTOR`: always 2 gold paragraphs;
* `DEV_FULLWIKI`: between 0 and 2 gold paragraphs (in this case, please note that the
gold paragraph(s) may not be sufficient to answer the question at hand);
* `TEST_FULLWIKI`: no gold paragraph whatsoever; 

Please refer to the `Full example` section below for a concrete case of gold paragraph
extraction procedure.


Full example
------------

Please see this [example](https://pastebin.com/PwhjVLjD) of a question taken
directly from the `HoppotQA` dataset (distractor setting). In order to deduce the
gold paragraphs we can look at the supporting facts:

```json
"supporting_facts":[
    ["Nicholas Christopher", 0],
    ["Roger Ebert", 0]
]
```

They are specifying two supporting sentences: the first one (id 0) from the paragraph
with title "Nicholas Christopher" and the first one (id 0) from the "Roger Ebert"
paragraph. The aforementioned paragraphs are gold paragraphs and they can be used (alone)
to infer the correct answer. The other 8 paragraphs from the `context` array are
distractors. As a result, for the above example, the 2 gold paragraphs are:

```
Paragraph A) Nicholas Christopher (born 1951) is an American novelist, poet and critic,
the author of sixteen books: six novels, eight volumes of poetry, a critical study of film
noir, and a novel for children.
```

```
Paragraph B) Roger Joseph Ebert ( ; June 18, 1942 \u2013 April 4, 2013) was an American
film critic and historian, journalist, screenwriter, and author. He was a film critic for
the \"Chicago Sun-Times\" from 1967 until his death in 2013. In 1975, Ebert became the
first film critic to win the Pulitzer Prize for Criticism.
```
