# CosmosQA: Machine Reading Comprehension with Contextual Commonsense Reasoning


Dataset description
-------------------

`CosmosQA` is a large-scale dataset of 35.6K problems that require
commonsense-based reading comprehension, formulated as multiple-choice
questions. It focuses on reading between the lines over a diverse collection of
people's everyday narratives, asking questions concerning on the likely causes 
or effects of events that require reasoning beyond the exact text spans in
the context. In stark contrast to most existing reading comprehension datasets
where the questions focus on factual and literal understanding of the context
paragraph, `CosmosQA` focuses on reading between the lines, asking questions
such as `what might be the possible reason of ...?`, or `what would have
happened if ...` which require a different form of reasoning. 

Experimental results demonstrate a significant gap between machine (68.4%)
\- `BERT Large` \- and human performance (94%), pointing to avenues for future
research on commonsense machine comprehension.


* [Paper](https://arxiv.org/pdf/1909.00277.pdf)
* [Random baseline](https://github.com/allenai/mosaic-leaderboard/tree/master/cosmosqa/baselines/random-baseline)
* [Leaderboard](https://leaderboard.allenai.org/cosmosqa/submissions/public)


How to use
----------

```python
import data_mine as dm

from data_mine.nlp.cosmos_qa import CosmosQAType


def main():
    df = dm.COSMOS_QA(CosmosQAType.TRAIN)
    print(df)  # Shows something similar to the example below.


if __name__ == "__main__":
    main()
```

The following `CosmosQA` types (splits) are available:
1. `TRAIN`
2. `DEV`
3. `TEST`


Scheme (CosmosQA DataFrame)
-----------------------

The loading function (`data_mine.nlp.cosmos_qa.CosmosQADataset` or `dm.COSMOS_QA`)
returns a `Pandas DataFrame` with 5 columns: 
* `id`: string;
* `question`: string;
* `context`: string;
* `answers`: list[string], length is always 4;
* `correct`: oneof('A', 'B', 'C', D') or None for the test split.

Example:
```
                                                      id                                           question  ...                                            answers correct
0      3Q9SPIIRWJKVQ8244310E8TUS6YWAC##34V1S5K3GTZMDU...  In the future , will this person go to see oth...  ...  [None of the above choices ., This person like...       B
1      3E24UO25QZOMYXHZN4TEH9EMT9GO6L##3UN61F00HXNWYQ...  Why might have the temp agency tell me I am no...  ...  [The company hiring the temp workers might hav...       A
2      3M4KL7H8KVL125AYH2V35D1E0A016T##3SB5N7Y3O426ET...  What may have caused the radio to erupt with d...  ...  [My partner needed a medic unit ., Someone was...       D
3      3D5G8J4N5CI2K40F4RZLF9OG2L4VTJ##34MAJL3QP721EU...          Why did I chit chat with my old manager ?  ...  [Because my flight was at 1:30 ., Because I le...       D
4      3MQKOF1EE428I44N8B42W7P86DKDW4##3NJM2BJS4ZLBGN...                       Why did I burst into tears ?  ...  [Because Ms. Mumma was informative ., Because ...       B
...                                                  ...                                                ...  ...                                                ...     ...
25257  306W7JMRYYWPJHBECELQV3AESEYB8J##3OHYZ19UGD3Q7J...               What may be a fact about their dad ?  ...  [He 's a different person now ., He died ., No...       B
25258  3J94SKDEKK3E5LP3CAHT67CWNMZ5DD##36AHBNMV1URFUT...  Why might we have gone back to the same place ...  ...  [It 's a place I do n't have to be chatty beca...       C
25259  3AQN9REUTHUC79ZNNCMQH4AOHBODYN##3WYP994K1A6G9K...                  What is the narrator describing ?  ...  [They 're talking their cat ., None of the abo...       C
25260  3AQN9REUTHUC79ZNNCMQH4AOHBODYN##3WYP994K1A6G9K...                  What is the narrator describing ?  ...  [They 're talking their cat ., They 're talkin...       B
25261  3OLZC0DJ8JDXH1LXQHOH94YZY51IVS##3IO1LGZLKAVMZP...        What happened after Michael came to visit ?  ...  [We hung out the entire day ., We made sure to...       A

[25262 rows x 5 columns]
```
