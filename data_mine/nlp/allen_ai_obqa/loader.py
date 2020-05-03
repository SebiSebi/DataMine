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


def OBQADataset(obqa_type):
    """
    Loads an OpenBookQA dataset given the type (see the OBQAType enum).
    Any error during reading will generate an exception.

    Returns a Pandas DataFrame with 4 columns:
    * 'id': string
    * 'question': string
    * 'answers': list[string], length = 4
    * 'correct': oneof('A', 'B', 'C', D')
    """
    assert(isinstance(obqa_type, OBQAType))
    download_dataset(Collection.ALLEN_AI_OBQA, check_shallow_integrity)
    all_data = []
    all_ids = set()
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
            all_data.append({
                "id": question_id,
                "question": question,
                "answers": answers,
                "correct": correct_answer
            })
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
            yield line.strip(string.whitespace + "\"")
