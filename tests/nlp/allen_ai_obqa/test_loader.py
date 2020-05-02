import data_mine as dm
import json
import jsonlines
import os
import pandas as pd
import sys
import unittest

from data_mine import Collection
from data_mine.nlp.allen_ai_obqa import OBQAType
from data_mine.nlp.allen_ai_obqa.utils import type_to_data_file
from data_mine.utils import datamine_cache_dir
from pyfakefs.fake_filesystem_unittest import TestCase
if sys.version_info >= (3, 3):
    from unittest.mock import ANY, patch
else:
    from mock import ANY, patch


GOOD_QUESTION1 = json.loads("""{
    "id": "7-980",
    "question": {
        "stem": "The sun is responsible for",
        "choices": [
            {
                "text": "puppies learning new tricks",
                "label": "A"
            },
            {
                "text": "children growing up and getting old",
                "label": "B"
            },
            {
                "text": "flowers wilting in a vase",
                "label": "C"
            },
            {
                "text": "plants sprouting, blooming and wilting",
                "label": "D"
            }
        ]
    },
    "answerKey": "D"
}""")

GOOD_QUESTION2 = json.loads("""{
    "id": "1158",
    "question": {
        "stem": "Which product cannot convert energy into light?",
        "choices": [
            {
                "text": "floor lamp",
                "label": "C"
            },
            {
                "text": "charger",
                "label": "B"
            },
            {
                "text": "Christmas tree lights",
                "label": "D"
            },
            {
                "text": "chandelier",
                "label": "A"
            }
        ]
    },
    "answerKey": "B"
}""")

GOOD_QUESTION3 = json.loads("""{
    "id": "609",
    "question": {
        "stem": "What do cows eat?",
        "choices": [
            {
                "text": "Poultry",
                "label": "D"
            },
            {
                "text": "Steak",
                "label": "C"
            },
            {
                "text": "Chocolate",
                "label": "B"
            },
            {
                "text": "Chickpeas",
                "label": "A"
            }
        ]
    },
    "answerKey": "A"
}""")

INVALID_CORECT_ANSWER = json.loads("""{
    "id": "123456",
    "question": {
        "stem": "What do cows eat?",
        "choices": [
            {
                "text": "Poultry",
                "label": "D"
            },
            {
                "text": "Steak",
                "label": "C"
            },
            {
                "text": "Chocolate",
                "label": "B"
            },
            {
                "text": "Chickpeas",
                "label": "A"
            }
        ]
    },
    "answerKey": "E"
}""")


class TestOBQADatasetLoader(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

        dataset_dir = os.path.join(
                datamine_cache_dir(),
                "ALLEN_AI_OBQA", "OpenBookQA-V1-Sep2018",
                "Data", "Main"
        )
        os.makedirs(dataset_dir, mode=0o755)

    def write_questions(self, obqa_type, question_list):
        datafile = type_to_data_file(obqa_type)
        with jsonlines.open(datafile, "w") as writer:
            writer.write_all(question_list)

    @patch('data_mine.nlp.allen_ai_obqa.loader.download_dataset')
    def test_empty_dataset(self, mock_download_dataset):
        self.write_questions(OBQAType.DEV, [])
        df = dm.ALLEN_AI_OBQA(OBQAType.DEV)
        mock_download_dataset.assert_called_once_with(Collection.ALLEN_AI_OBQA, ANY)  # noqa: E501
        self.assertEqual(len(df), 0)

    @patch('data_mine.nlp.allen_ai_obqa.loader.download_dataset')
    def test_parsing_logic(self, mock_download_dataset):
        self.write_questions(OBQAType.TRAIN, [
                GOOD_QUESTION1, GOOD_QUESTION2, GOOD_QUESTION3
        ])
        df = dm.ALLEN_AI_OBQA(OBQAType.TRAIN)
        expected_df = pd.DataFrame(json.loads("""[
            {
                "id": "7-980",
                "question": "The sun is responsible for",
                "answers": [
                    "puppies learning new tricks",
                    "children growing up and getting old",
                    "flowers wilting in a vase",
                    "plants sprouting, blooming and wilting"
                ],
                "correct": "D"
            },
            {
                "id": "1158",
                "question": "Which product cannot convert energy into light?",
                "answers": [
                    "chandelier",
                    "charger",
                    "floor lamp",
                    "Christmas tree lights"
                ],
                "correct": "B"
            },
            {
                "id": "609",
                "question": "What do cows eat?",
                "answers": [
                    "Chickpeas",
                    "Chocolate",
                    "Steak",
                    "Poultry"
                ],
                "correct": "A"
            }
        ]"""))
        pd.testing.assert_frame_equal(df, expected_df)
        mock_download_dataset.assert_called_once_with(Collection.ALLEN_AI_OBQA, ANY)  # noqa: E501

    @patch('data_mine.nlp.allen_ai_obqa.loader.download_dataset')
    def test_invalid_correct_answer(self, mock_download_dataset):
        self.write_questions(OBQAType.TEST, [
            INVALID_CORECT_ANSWER
        ])
        with self.assertRaises(AssertionError):
            dm.ALLEN_AI_OBQA(OBQAType.TEST)
        mock_download_dataset.assert_called_once_with(Collection.ALLEN_AI_OBQA, ANY)  # noqa: E501

    @patch('data_mine.nlp.allen_ai_obqa.loader.download_dataset')
    def test_duplicate_ids(self, mock_download_dataset):
        self.write_questions(OBQAType.DEV, [
            GOOD_QUESTION1, GOOD_QUESTION1
        ])
        with self.assertRaises(AssertionError):
            dm.ALLEN_AI_OBQA(OBQAType.DEV)
        mock_download_dataset.assert_called_once_with(Collection.ALLEN_AI_OBQA, ANY)  # noqa: E501


if __name__ == '__main__':
    unittest.main()