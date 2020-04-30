import data_mine as dm
import json
import jsonlines
import os
import pandas as pd
import sys
import unittest

from data_mine import Collection
from data_mine.nlp.CSQA import CSQAType
from data_mine.nlp.CSQA.utils import type_to_data_file
from data_mine.utils import datamine_cache_dir
from pyfakefs.fake_filesystem_unittest import TestCase
if sys.version_info >= (3, 3):
    from unittest.mock import ANY, patch
else:
    from mock import ANY, patch

# Regular format.
TRAIN_QUESTION1 = json.loads("""{
    "answerKey": "D",
    "id": "3e792834df2aa7ae2a9070b494e37c26",
    "question": {
        "question_concept": "steam",
        "choices": [
            {
                "label": "A",
                "text": "condensate"
            },
            {
                "label": "B",
                "text": "electric smoke"
            },
            {
                "label": "C",
                "text": "smoke"
            },
            {
                "label": "D",
                "text": "liquid water"
            },
            {
                "label": "E",
                "text": "cold air"
            }
        ],
        "stem": "John cooled the steam. What did the steam become?"
    }
}""")

# Answers not in normal order. Tests that choices are sorted.
TRAIN_QUESTION2 = json.loads("""{
    "answerKey": "A",
    "id": "6c84e79d0595efd99596faa07c4961d0",
    "question": {
        "question_concept": "climb",
        "choices": [
            {
                "label": "E",
                "text": "may fall"
            },
            {
                "label": "A",
                "text": "grab"
            },
            {
                "label": "D",
                "text": "falling"
            },
            {
                "label": "C",
                "text": "throw"
            },
            {
                "label": "B",
                "text": "look down"
            }
        ],
        "stem": "What would you do to a rock when climb up a cliff?"
    }
}""")

# The "answerKey" field is missing. Simulate real CSQA test data.
TEST_QUESTION = json.loads("""{
    "id": "9082b65f2bc5328ea991f734f930ddb5",
    "question": {
        "question_concept": "children",
        "choices": [
            {
                "label": "A",
                "text": "watch television"
            },
            {
                "label": "B",
                "text": "play basketball"
            },
            {
                "label": "C",
                "text": "cut and paste"
            },
            {
                "label": "D",
                "text": "swimming"
            },
            {
                "label": "E",
                "text": "reach over"
            }
        ],
        "stem": "If children were in a gym, would they be doing?"
    }
}""")

# Answer 'F' should not be accepted.
INVALID_CORRECT_ANSWER = json.loads("""{
    "answerKey": "F",
    "id": "aaaabbbbccccdddd2a9070b494e37373",
    "question": {
        "question_concept": "soccer",
        "choices": [
            {
                "label": "A",
                "text": "text A"
            },
            {
                "label": "B",
                "text": "text B"
            },
            {
                "label": "C",
                "text": "text C"
            },
            {
                "label": "D",
                "text": "text D"
            },
            {
                "label": "E",
                "text": "text E"
            }
        ],
        "stem": "Some question?"
    }
}""")


class TestCSQADatasetLoader(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

        dataset_dir = os.path.join(datamine_cache_dir(), "CSQA")
        os.makedirs(dataset_dir, mode=0o755)

    def write_questions(self, csqa_type, question_list):
        datafile = type_to_data_file(csqa_type)
        with jsonlines.open(datafile, "w") as writer:
            writer.write_all(question_list)

    @patch('data_mine.nlp.CSQA.loader.download_dataset')
    def test_empty_dataset(self, mock_download_dataset):
        self.write_questions(CSQAType.TRAIN, [])
        df = dm.CSQA(CSQAType.TRAIN)
        mock_download_dataset.assert_called_once_with(Collection.CSQA, ANY)
        self.assertEqual(len(df), 0)

    @patch('data_mine.nlp.CSQA.loader.download_dataset')
    def test_load_in_train_and_dev_format(self, mock_download_dataset):
        self.write_questions(CSQAType.TRAIN, [
            TRAIN_QUESTION1, TRAIN_QUESTION2
        ])
        expected_df = pd.DataFrame(json.loads("""[
        {
            "id": "3e792834df2aa7ae2a9070b494e37c26",
            "question": "John cooled the steam. What did the steam become?",
            "answers": [
                "condensate",
                "electric smoke",
                "smoke",
                "liquid water",
                "cold air"
            ],
            "correct": "D",
            "question_concept": "steam"
        },
        {
            "id": "6c84e79d0595efd99596faa07c4961d0",
            "question": "What would you do to a rock when climb up a cliff?",
            "answers": [
                "grab",
                "look down",
                "throw",
                "falling",
                "may fall"
            ],
            "correct": "A",
            "question_concept": "climb"
        }
        ]"""))
        pd.testing.assert_frame_equal(dm.CSQA(CSQAType.TRAIN), expected_df)
        mock_download_dataset.assert_called_once_with(Collection.CSQA, ANY)

    @patch('data_mine.nlp.CSQA.loader.download_dataset')
    def test_load_in_test_format(self, mock_download_dataset):
        self.write_questions(CSQAType.TEST, [TEST_QUESTION])
        expected_df = pd.DataFrame(json.loads("""[
            {
                "id": "9082b65f2bc5328ea991f734f930ddb5",
                "question": "If children were in a gym, would they be doing?",
                "answers": [
                    "watch television",
                    "play basketball",
                    "cut and paste",
                    "swimming",
                    "reach over"
                ],
                "correct": null,
                "question_concept": "children"
            }
        ]"""))
        self.assertIsNone(next(expected_df.iterrows())[1].correct)
        pd.testing.assert_frame_equal(dm.CSQA(CSQAType.TEST), expected_df)
        mock_download_dataset.assert_called_once_with(Collection.CSQA, ANY)

    @patch('data_mine.nlp.CSQA.loader.download_dataset')
    def test_missing_correct_answer_on_train(self, mock_download_dataset):
        self.assertEqual(len(TEST_QUESTION), 2)
        self.assertNotIn("answerKey", TEST_QUESTION)
        self.write_questions(CSQAType.TRAIN, [TEST_QUESTION])
        with self.assertRaises(AssertionError):
            dm.CSQA(CSQAType.TRAIN)
        mock_download_dataset.assert_called_once_with(Collection.CSQA, ANY)

    @patch('data_mine.nlp.CSQA.loader.download_dataset')
    def test_missing_correct_answer_on_dev(self, mock_download_dataset):
        self.assertEqual(len(TEST_QUESTION), 2)
        self.assertNotIn("answerKey", TEST_QUESTION)
        self.write_questions(CSQAType.DEV, [TEST_QUESTION])
        with self.assertRaises(AssertionError):
            dm.CSQA(CSQAType.DEV)
        mock_download_dataset.assert_called_once_with(Collection.CSQA, ANY)

    @patch('data_mine.nlp.CSQA.loader.download_dataset')
    def test_has_correct_answer_on_test(self, mock_download_dataset):
        self.assertEqual(len(TRAIN_QUESTION1), 3)
        self.assertIn("answerKey", TRAIN_QUESTION1)
        self.write_questions(CSQAType.TEST, [TRAIN_QUESTION1])
        with self.assertRaises(AssertionError):
            dm.CSQA(CSQAType.TEST)
        mock_download_dataset.assert_called_once_with(Collection.CSQA, ANY)

    @patch('data_mine.nlp.CSQA.loader.download_dataset')
    def test_invalid_correct_answer(self, mock_download_dataset):
        self.write_questions(CSQAType.DEV, [
            TRAIN_QUESTION1, TRAIN_QUESTION2, INVALID_CORRECT_ANSWER
        ])
        with self.assertRaises(AssertionError):
            dm.CSQA(CSQAType.DEV)
        mock_download_dataset.assert_called_once_with(Collection.CSQA, ANY)


if __name__ == '__main__':
    unittest.main()
