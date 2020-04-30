import json
import pandas as pd

from data_mine import Collection
from data_mine.zookeeper import check_shallow_integrity, download_dataset
from six import string_types
from .types import CSQAType
from .utils import type_to_data_file


def CSQADataset(csqa_type):
    """
    TODO(sebisebi): add description
    """
    assert(isinstance(csqa_type, CSQAType))
    download_dataset(Collection.CSQA, check_shallow_integrity)
    all_data = []
    with open(type_to_data_file(csqa_type), "rt") as f:
        for line in f:
            entry = json.loads(line)
            assert(len(entry) == 2 if csqa_type == CSQAType.TEST else 3)
            question_id = entry["id"]
            correct_answer = entry.get("answerKey", None)
            entry = entry["question"]
            assert(isinstance(question_id, string_types))
            if csqa_type != CSQAType.TEST:
                assert(correct_answer in ["A", "B", "C", "D", "E"])
            else:
                assert(correct_answer is None)
            assert(len(entry) == 3)

            question = entry["stem"]
            question_concept = entry["question_concept"]
            answers = [
                choice["text"]
                for choice in sorted(
                    entry["choices"],
                    key=lambda x: x["label"])
            ]
            assert(isinstance(question, string_types))
            assert(isinstance(question_concept, string_types))
            assert(len(answers) == 5)
            for answer in answers:
                assert(isinstance(answer, string_types))
            all_data.append({
                "id": question_id,
                "question": question,
                "answers": answers,
                "correct": correct_answer,
                "question_concept": question_concept
            })
    df = pd.DataFrame(all_data)
    return df
