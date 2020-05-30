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
from data_mine.nlp.allen_ai_arc import ARCType
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
    questions = df["question"].tolist()
    questions = map(lambda q: q.replace("_", " "), questions)
    return list(questions)


def load_arc():
    df = pd.concat([
        dm.ALLEN_AI_ARC(ARCType.TRAIN_EASY),
        dm.ALLEN_AI_ARC(ARCType.DEV_EASY),
        dm.ALLEN_AI_ARC(ARCType.TEST_EASY),
        dm.ALLEN_AI_ARC(ARCType.TRAIN_CHALLENGE),
        dm.ALLEN_AI_ARC(ARCType.DEV_CHALLENGE),
        dm.ALLEN_AI_ARC(ARCType.TEST_CHALLENGE),
    ], ignore_index=True, sort=False)
    return df["question"].tolist()


def load_questions():
    return load_arc()


def extract_trigram_from_doc(doc):
    """
    The function receives a (parsed) spaCy document and is expected to return
    a tuple of tokens representing the first three tokens from the question.

    The function returns None if a trigram cannot be extracted (e.g. the
    question is too short. Some questions have multiple sentences from which
    only the last one is the actual sentence. We use that to extract trigrams.
    """
    if len(doc) < 3:
        return None
    sents = list(doc.sents)
    if len(sents) > 1:
        last_sent = sents[-1]
        if len(last_sent) < 3:
            return None
        doc = last_sent
    return tuple([token.lower_ for token in doc[:3]])


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
    compound_questions = 0
    skipped = 0
    tokens = []
    for doc in tqdm.tqdm(docs, total=len(questions), desc="Tokenizing"):
        trigram = extract_trigram_from_doc(doc)
        if trigram is None:
            skipped += 1
            continue
        tokens.append(trigram)
        if len(list(doc.sents)) > 1:
            compound_questions += 1
    if skipped > 0:
        print("Skipped {} questions as they are too short.".format(skipped))
    if compound_questions > 0:
        print("Found {} questions with multiple sentences.".format(compound_questions))  # noqa: E501
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
            ),
    )
    fig.update_traces(insidetextorientation="radial")
    fig.update_traces(textfont_size=36)
    fig.update_layout(title_text="ARC", title_x=0.5)
    fig.show()


if __name__ == "__main__":
    main()
