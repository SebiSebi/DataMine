import json
import os
import pandas as pd

from data_mine import Collection
from data_mine.zookeeper import check_shallow_integrity, download_dataset
from six import string_types
from .types import RACEType
from .utils import next_question_id
from .utils import type_to_data_directory


def RACEDataset(race_type):
    """
    Loads a RACE dataset given the type (see the RACEType enum).
    Any error during reading will generate an exception.

    Returns a Pandas DataFrame with 5 columns:
    * 'article': string
    * 'question': string
    * 'answers': list[string], length = 4
    * 'correct': oneof('A', 'B', 'C', D')
    * 'id': string

    The returned IDs are unique and have this format: `index`-`passage_id`.
    Examples: 1-middle1548.txt, 2-middle1548.txt, etc. The `passage_id` is
    frequently the name of the file. All the questions related to the same
    passage are grouped in the same file in the RACE dataset (convention).
    Because in each RACE file  there are multiple questions, the counter is
    necessary in order to guarantee that IDs are unique (the file name is
    not sufficient). We translate the `passage_id` into the `question_id`
    using the per-passage-question counter.
    """
    assert(isinstance(race_type, RACEType))
    download_dataset(Collection.RACE, check_shallow_integrity)
    dirpath = type_to_data_directory(race_type)
    all_data = []
    q_ids = {}
    for path in os.listdir(dirpath):
        assert(os.path.isfile(os.path.join(dirpath, path)))
        with open(os.path.join(dirpath, path), 'rt') as f:
            entry = json.load(f)

            """
            Each passage is a JSON file. The JSON file contains these fields:

            1. article: A string, which is the passage.
            2. questions: A string list. Each string is a query. We have two
                          types of questions. First one is an interrogative
                          sentence. Another one has a placeholder, which is
                          represented by _.
            3. options: A list of the options list. Each options list contains
                        4 strings, which are the candidate option.
            4. answers: A list contains the golden label of each query.
            5. id: Each passage has an id in this dataset. Note: the ids are
                   not unique in the question set! Questions in the same file
                   have the same id (the name of the file). This id is more of
                   a passage id than a question id.
            """
            assert(len(entry) == 5)
            assert(set(entry.keys()) == {
                "article",
                "questions",
                "options",
                "answers",
                "id"
            })
            article = entry["article"]
            questions = entry["questions"]
            options = entry["options"]
            answers = entry["answers"]
            q_id = entry["id"]
            assert(isinstance(article, string_types))
            assert(isinstance(questions, list))
            assert(isinstance(options, list))
            assert(isinstance(answers, list))
            assert(isinstance(q_id, string_types))
            assert(len(questions) == len(options))
            assert(len(questions) == len(answers))
            for question, option, answer in zip(questions, options, answers):
                assert(isinstance(question, string_types))
                assert(isinstance(option, list) and len(option) == 4)
                assert(isinstance(answer, string_types))
                assert(answer in ["A", "B", "C", "D"])
                all_data.append({
                    'article': article,
                    'question': question,
                    'answers': option,
                    'correct': answer,
                    'id': next_question_id(q_ids, q_id)
                })
    df = pd.DataFrame(all_data)
    return df
