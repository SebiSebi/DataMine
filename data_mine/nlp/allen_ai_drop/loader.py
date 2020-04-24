import json
import pandas as pd

from data_mine import Collection
from data_mine.zookeeper import check_shallow_integrity, download_dataset
from .types import DROPType
from .utils import type_to_data_file


def DROPDataset(drop_type):
    """
    TODO(sebisebi): add description
    """
    assert(isinstance(drop_type, DROPType))
    download_dataset(Collection.ALLEN_AI_DROP, check_shallow_integrity)

    def parse_answer(answer):
        """
        Answer format (sanitized of other unwanted fields):

        "answer": {
            "number": "3",
            "date": {
                "day": "",
                "month": "",
                "year": ""
            },
            "spans": [],
        }

        Returns the type and the answer as a string.

        The type can be:
            a) "number" (be aware that this can be integer or real).
            b) "date"
            c) "spans"
            d) None, some answer are completely empty.
        """
        assert(len(answer) == 3)
        assert(set(answer.keys()) == set(["number", "date", "spans"]))

        def is_number():
            return len(answer["number"]) > 0

        def is_date():
            date = answer["date"]
            if len(date) == 0:
                return False
            assert(set(date.keys()) == set(["day", "month", "year"]))
            return len(date["day"] + date["month"] + date["year"]) > 0

        def is_span():
            return len(answer["spans"]) > 0

        if is_number():
            assert(not is_date())
            assert(not is_span())
            float(answer["number"])
            return "number", str(answer["number"])

        if is_date():
            assert(not is_number())
            assert(not is_span())
            date = answer["date"].items()
            date = filter(lambda x: len(x[1]) > 0, date)
            date = [x[1] for x in sorted(date)]
            return "date", " ".join(date)

        if is_span():
            assert(not is_number())
            assert(not is_date())
            return "spans", ", ".join(answer["spans"])

        return None, None

    all_query_ids = set()
    all_questions = []
    data = json.load(open(type_to_data_file(drop_type), "rt"))
    # The Subject ID represents the context category. Examples include
    # history_4122, nfl_3073 or history_3259. It seems that all questions
    # target NFL or history subjects.
    for subject_id in data:
        entry = data[subject_id]
        assert(len(entry) == 3)  # passage, qa_pairs and wiki_url
        passage = entry["passage"]
        assert(isinstance(passage, str))
        """
        {
            "question": "How many points were scored first?",
            "answer": {
                "number": "3",
                "date": {
                    "day": "",
                    "month": "",
                    "year": ""
                },
                "spans": [],

                "hit_id": "",  # Not useful, always empty when present.
                "worker_id": ""  # Not useful, always empty when present.
            },
            "query_id": "33f9f7bd-518b-45ae-86d5-c1475167d54f",
            "highlights": [],  # Always empty or missing.
            "question_type": [],  # Always empty or missing.
            "validated_answers": [],  # Always empty or missing.
            "expert_answers": []  # Always empty or missing.
        }
        """
        for qa_pair in entry["qa_pairs"]:
            unwanted_fields = [
                "highlights",
                "question_type",
                "validated_answers",
                "expert_answers",
                "workerid",
                "workerscore",
                "incorrect_options",
                "ai_answer"
            ]
            for unwanted_field in unwanted_fields:
                if unwanted_field in qa_pair:
                    del qa_pair[unwanted_field]
            assert(len(qa_pair) == 3)

            question = qa_pair["question"]
            answer = qa_pair["answer"]
            query_id = qa_pair["query_id"]
            assert(isinstance(question, str))
            assert(isinstance(answer, dict))
            assert(isinstance(query_id, str))

            # This answer has 2 correct answers. Manually remove the false one.
            if query_id == "daf712ed-3849-48a1-b9b5-f7d21b0c0ab7":
                answer["number"] = ""

            # This is a duplicate query.
            if query_id == "28553293-d719-441b-8f00-ce3dc6df5398":
                if query_id in all_query_ids:
                    continue

            # Sanitize the answer object.
            unwanted_fields = [
                    "worker_id",
                    "hit_id"
            ]
            for unwanted_field in unwanted_fields:
                if unwanted_field in answer:
                    assert(len(answer[unwanted_field]) == 0)
                    del answer[unwanted_field]
            assert(len(answer) == 3)
            answer_type, parsed_answer = parse_answer(answer)
            if answer_type is None:
                continue
            assert(answer_type in ["number", "date", "spans"])
            assert(len(parsed_answer) >= 1)
            all_query_ids.add(str(query_id))
            all_questions.append({
                "query_id": query_id,
                "question": question,
                "answer_type": answer_type,
                "parsed_answer": parsed_answer,
                "original_answer": answer
            })
    assert(len(all_questions) == len(all_query_ids))

    df = pd.DataFrame(all_questions)
    return df
