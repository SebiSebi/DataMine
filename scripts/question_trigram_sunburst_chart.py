"""
Script for plotting the distribution of trigram prefixes of questions.

A sunburst chart is used for visualization.
"""
import data_mine as dm
import more_itertools
import multiprocessing
import pandas as pd
import plotly.express as px
import spacy
import tqdm

from collections import Counter
from data_mine.nlp.CSQA import CSQAType
from data_mine.nlp.RACE import RACEType
from data_mine.nlp.cosmos_qa import CosmosQAType
from data_mine.nlp.allen_ai_drop import DROPType
from data_mine.nlp.allen_ai_obqa import OBQAType


def load_cosmos_qa():
    df = pd.concat([
        dm.COSMOS_QA(CosmosQAType.TRAIN),
        dm.COSMOS_QA(CosmosQAType.DEV),
        dm.COSMOS_QA(CosmosQAType.TEST)
    ], ignore_index=True, sort=False)
    return df["question"].tolist()


def load_drop():
    df = pd.concat([
        dm.ALLEN_AI_DROP(DROPType.TRAIN),
        dm.ALLEN_AI_DROP(DROPType.DEV)
    ], ignore_index=True, sort=False)
    return df["question"].tolist()


def load_obqa():
    df = pd.concat([
        dm.ALLEN_AI_OBQA(OBQAType.TRAIN),
        dm.ALLEN_AI_OBQA(OBQAType.DEV),
        dm.ALLEN_AI_OBQA(OBQAType.TEST)
    ], ignore_index=True, sort=False)
    return df["question"].tolist()


def load_csqa():
    df = pd.concat([
        dm.CSQA(CSQAType.TRAIN),
        dm.CSQA(CSQAType.DEV),
        dm.CSQA(CSQAType.TEST),
    ], ignore_index=True, sort=False)
    return df["question"].tolist()


def load_race():
    df = pd.concat([
        dm.RACE(RACEType.TRAIN_MIDDLE),
        dm.RACE(RACEType.TRAIN_HIGH),
        dm.RACE(RACEType.DEV_MIDDLE),
        dm.RACE(RACEType.DEV_HIGH),
        dm.RACE(RACEType.TEST_MIDDLE),
        dm.RACE(RACEType.TEST_HIGH)
    ], ignore_index=True, sort=False)
    return df["question"].tolist()


def load_questions():
    return load_obqa()


def tokenize(questions):
    assert(isinstance(questions, list))
    num_cpus = multiprocessing.cpu_count() or 1
    print("Using {} processes.".format(num_cpus - 1))
    nlp = spacy.load("en_core_web_lg")
    docs = nlp.pipe(
            questions,
            batch_size=256,
            n_process=num_cpus - 1,
            disable=["ner", "tagger"]
    )
    skipped = 0
    tokens = []
    for doc in tqdm.tqdm(docs, total=len(questions), desc="Tokenizing"):
        if len(doc) < 3:
            skipped += 1
            continue
        tokens.append(tuple([token.lower_ for token in doc[:3]]))
    if skipped > 0:
        print("Skipped {} questions as they are too short.".format(skipped))
    tokens = list(Counter(tokens).items())
    tokens.sort(key=lambda x: x[1], reverse=True)
    return tokens


def main():
    questions = load_questions()
    print("Analysing {} questions.\n".format(len(questions)))
    trigrams = tokenize(questions)
    print("Found {} different trigrams.".format(len(trigrams)))

    print("\nTop 5 triples:")
    for i, (triple, count) in enumerate(trigrams[:5]):
        print("{}) {} - {} times".format(i + 1, triple, count))
    print("")

    trigrams = trigrams[:150]
    trigrams = filter(lambda x: x[1] >= 7, trigrams)
    trigrams = list(map(lambda x: (*x[0], x[1]), trigrams))
    df = pd.DataFrame(
            trigrams,
            columns=["First", "Second", "Third", "Count"]
    )
    print(df)
    fig = px.sunburst(
            df, path=["First", "Second", "Third"], values="Count",
            color_discrete_sequence=[
                "#f8cbad", "#c5e0b4", "#7fdbff", "#ffe698",
                "#d87eaa", "#0074D9"
            ] + list(more_itertools.interleave_longest(
                    list(px.colors.diverging.Spectral),
                    list(px.colors.diverging.Geyser))
            )
    )
    fig.update_traces(textfont_size=15)
    fig.show()


if __name__ == "__main__":
    main()
