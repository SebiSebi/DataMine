import json
import os
import pandas as pd
import string

from data_mine import Collection
from data_mine.zookeeper import check_shallow_integrity, download_dataset
from six import string_types
from .constants import OBQA_CACHE_DIR
from .types import OBQAType
from .utils import type_to_data_file


def OBQADataset(obqa_type, with_retrieved_facts=False):
    """
    Loads an OpenBookQA dataset given the type (see the OBQAType enum).
    Any error during reading will generate an exception.

    Returns a Pandas DataFrame with 4 columns:
    * 'id': string
    * 'question': string
    * 'answers': list[string], length = 4
    * 'correct': oneof('A', 'B', 'C', D')

    If `with_retrieved_facts` is True then a new column is added with
    the name `retrieved_facts`. This column is an array with 4 dictionaries
    each describing the retrieved facts supporting the corresponding candidate
    answer. The retrieved facts dict for a given answer has the following keys:
    * 'context': string - a string with multiple facts from the OBQA "book".
    * 'token_based': list[string]: a list of facts extracted with Lucene.
    * 'vector_based': list[string]: a list of facts extracted with embeddings.
    The list of facts (both token and vector based) are sorted in decreasing
    order of the relevance score (the first fact in the list is the most
    relevant). We recommend the "context" field to be used. It is a carefully
    constructed string using the top 5 token facts, top 5 vector facts and
    then interleaving the remaining facts (until about 500 tokens made up
    context). Facts are concatenated using " . " as a separator.
    """
    assert(isinstance(obqa_type, OBQAType))
    download_dataset(Collection.ALLEN_AI_OBQA, check_shallow_integrity)
    all_data = []
    all_ids = set()
    retrieved_facts = None
    if with_retrieved_facts:
        retrieved_facts = json.load(open(os.path.join(OBQA_CACHE_DIR, "extracted_facts.json")))  # noqa: E501
    with open(type_to_data_file(obqa_type), "rt") as f:
        for line in f:
            entry = json.loads(line)
            assert(len(entry) == 3)

            question_id = entry["id"]
            correct_answer = entry["answerKey"]
            assert(isinstance(question_id, string_types))
            assert(correct_answer in ["A", "B", "C", "D"])

            entry = entry["question"]
            assert(len(entry) == 2)
            question = entry["stem"]
            answers = [
                choice["text"]
                for choice in sorted(
                    entry["choices"],
                    key=lambda x: x["label"])
            ]
            assert(isinstance(question, string_types))
            assert(len(answers) == 4)
            for answer in answers:
                assert(isinstance(answer, string_types))
            assert(question_id not in all_ids)
            all_ids.add(question_id)
            new_row = {
                "id": question_id,
                "question": question,
                "answers": answers,
                "correct": correct_answer
            }
            if with_retrieved_facts:
                queries = [question + " " + answer for answer in answers]
                facts = [retrieved_facts[query] for query in queries]
                assert(len(facts) == 4)
                for fact in facts:
                    assert(len(fact) == 3)
                    assert(isinstance(fact, dict))
                    assert("context" in fact)
                    assert("token_based" in fact)
                    assert("vector_based" in fact)
                new_row["retrieved_facts"] = facts
            all_data.append(new_row)
    assert(len(all_data) == len(all_ids))
    df = pd.DataFrame(all_data)
    return df


def OBQAFacts():
    """
    Yields the 1326 core science facts from the OpenBook QA dataset.

    Examples:
        * wind causes erosion
        * wind is a renewable resource

    Returns a generator of facts (strings).
    """
    download_dataset(Collection.ALLEN_AI_OBQA, check_shallow_integrity)
    facts_file = os.path.join(
            OBQA_CACHE_DIR, "OpenBookQA-V1-Sep2018",
            "Data", "Main", "openbook.txt"
    )
    with open(facts_file, "rt") as f:
        for line in f:
            fact = line.strip(string.whitespace + "\"")
            if len(fact) > 0:
                yield fact
