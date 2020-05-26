import json
import pandas as pd

from data_mine import Collection
from data_mine.zookeeper import check_shallow_integrity, download_dataset
from six import string_types
from .types import ARCType
from .utils import type_to_data_file


def ARCDataset(arc_type):
    """
    Loads an ARC dataset given the partition (see the ARCType enum).
    Any error during reading will generate an exception.

    Returns a Pandas DataFrame with 5 columns:
    * 'id': string
    * 'question': string
    * 'answers': list[string], 3 <= length <= 5
    * 'correct': oneof('A', 'B', 'C', D', 'E', '1', '2', '3', '4')
    """
    assert(isinstance(arc_type, ARCType))
    download_dataset(Collection.ALLEN_AI_ARC, check_shallow_integrity)
    all_data = []
    all_ids = set()
    with open(type_to_data_file(arc_type), "rt") as f:
        for line in f:
            entry = json.loads(line)
            assert(isinstance(entry, dict))
            assert(len(entry) == 3)

            # Extract fields.
            question_id = entry["id"]
            correct_answer = entry["answerKey"]
            entry = entry["question"]
            assert(len(entry) == 2)
            question = entry["stem"]
            for choice in entry["choices"]:
                assert(isinstance(choice["label"], string_types))
                assert(len(choice["label"]) == 1)
            answers = [
                choice["text"]
                for choice in sorted(
                    entry["choices"],
                    key=lambda x: x["label"])
            ]

            # Validate fields.
            assert(isinstance(question_id, string_types))
            assert(isinstance(correct_answer, string_types))
            assert(correct_answer in ["A", "B", "C", "D", "E", "1", "2", "3", "4"])  # noqa: E501
            assert(isinstance(question, string_types))
            assert(len(answers) in [3, 4, 5])
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
