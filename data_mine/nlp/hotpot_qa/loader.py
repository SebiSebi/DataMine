import json
import more_itertools
import pandas as pd

from data_mine import Collection
from data_mine.zookeeper import check_shallow_integrity, download_dataset
from six import string_types
from .types import HotpotQAType
from .utils import type_to_data_file


def HotpotQADataset(hotpot_qa_type):
    """
    TODO(sebisebi): add description

    TOTO(sebisebi): in the dev full wiki some joins cannot be made.
    Titles are missing from the context. This does not happen in the
    test fullwiki because the set of supporting_facts is empty. Why
    is this happening in dev? Can we do anything?
    """
    assert(isinstance(hotpot_qa_type, HotpotQAType))
    download_dataset(Collection.HOTPOT_QA, check_shallow_integrity)
    data = json.load(open(type_to_data_file(hotpot_qa_type), "rt"))
    assert(isinstance(data, list))
    processed_data = []
    all_ids = set()
    for entry in data:
        assert(isinstance(entry, dict))
        if hotpot_qa_type != HotpotQAType.TEST_FULLWIKI:
            assert(len(entry) == 7)
        else:
            assert(len(entry) == 3)  # _id, question, context

        # Extract fields.
        question_id = entry["_id"]
        question = entry["question"]
        answer = entry.get("answer", None)
        supporting_facts = entry.get("supporting_facts", [])
        context = entry["context"]
        question_type = entry.get("type", None)
        question_level = entry.get("level", None)

        # Validate fields.
        assert(isinstance(question_id, string_types))
        assert(isinstance(question, string_types))
        assert(isinstance(supporting_facts, list))
        assert(isinstance(context, list))
        if hotpot_qa_type != HotpotQAType.TEST_FULLWIKI:
            assert(isinstance(answer, string_types))
            assert(len(supporting_facts) > 0)
            assert(question_type in ["comparison", "bridge"])
            assert(question_level in ["easy", "medium", "hard"])
        else:
            assert(answer is None)
            assert(len(supporting_facts) == 0)
            assert(question_type is None)
            assert(question_level is None)

        # Get the list of supporting sentences by joining the supporting
        # facts with the context by title. There can be duplicate titles
        # in the supporting facts.
        titles = [title for title, _ in supporting_facts]
        titles = list(more_itertools.unique_everseen(titles))
        title2contents = {title: sentences for title, sentences in context}
        assert(len(title2contents) == len(context))
        if hotpot_qa_type == HotpotQAType.DEV_FULLWIKI:
            titles = filter(lambda title: title in title2contents, titles)
        gold_paragraphs = [' '.join(title2contents[title]) for title in titles]
        for paragraph in gold_paragraphs:
            assert(isinstance(paragraph, string_types))
        if hotpot_qa_type == HotpotQAType.TRAIN:
            assert(len(gold_paragraphs) == 2)
        elif hotpot_qa_type == HotpotQAType.DEV_DISTRACTOR:
            assert(len(gold_paragraphs) == 2)
        elif hotpot_qa_type == HotpotQAType.DEV_FULLWIKI:
            assert(len(gold_paragraphs) <= 2)
        elif hotpot_qa_type == HotpotQAType.TEST_FULLWIKI:
            assert(len(gold_paragraphs) == 0)

        assert(question_id not in all_ids)
        all_ids.add(question_id)
        processed_data.append({
            "id": question_id,
            "question": question,
            "answer": answer,
            "gold_paragraphs": gold_paragraphs,
            "supporting_facts": supporting_facts,
            "context": context,
            "question_type": question_type,
            "question_level": question_level
        })
    assert(len(processed_data) == len(data))
    assert(len(data) == len(all_ids))
    df = pd.DataFrame(processed_data)
    return df
