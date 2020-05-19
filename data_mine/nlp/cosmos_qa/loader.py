import json
import pandas as pd

from data_mine import Collection
from data_mine.zookeeper import check_shallow_integrity, download_dataset
from six import string_types
from .types import CosmosQAType
from .utils import type_to_data_file


def CosmosQADataset(cosmos_qa_type):
    """
    Loads a Cosmos QA dataset given the split (see the CosmosQAType enum).
    Any error during reading will generate an exception.

    Returns a Pandas DataFrame with 5 columns:
    * 'id': string
    * 'question': string
    * 'context': string
    * 'answers': list[string], length = 4
    * 'correct': oneof('A', 'B', 'C', D') or None for the test split
    """
    assert(isinstance(cosmos_qa_type, CosmosQAType))
    download_dataset(Collection.COSMOS_QA, check_shallow_integrity)

    def extract_answers(entry):
        for i in range(0, 4):
            key = "answer{}".format(i)
            answer = entry[key]
            assert(isinstance(answer, string_types))
            yield answer
            del entry[key]

    all_ids = set()
    all_data = []
    with open(type_to_data_file(cosmos_qa_type), "rt") as f:
        for line in f:
            entry = json.loads(line)
            assert(isinstance(entry, dict))
            if cosmos_qa_type != CosmosQAType.TEST:
                assert(len(entry) == 8)
            else:
                assert(len(entry) == 7)

            # Extract data.
            question_id = entry["id"]
            question = entry["question"]
            context = entry["context"]
            answers = list(extract_answers(entry))
            label = entry.get("label", None)
            if label is not None:
                label = chr(ord('A') + int(label))

            # Validate data.
            assert(isinstance(question_id, string_types))
            assert(isinstance(question, string_types))
            assert(isinstance(context, string_types))
            assert(isinstance(answers, list) and len(answers) == 4)
            if cosmos_qa_type == CosmosQAType.TEST:
                assert(label is None)
            else:
                assert(label in ["A", "B", "C", "D"])

            assert(question_id not in all_ids)
            all_ids.add(question_id)
            all_data.append({
                "id": question_id,
                "question": question,
                "context": context,
                "answers": answers,
                "correct": label,
            })
    assert(len(all_data) == len(all_ids))
    df = pd.DataFrame(all_data)
    return df
