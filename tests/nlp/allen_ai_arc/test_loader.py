import data_mine as dm
import json
import jsonlines
import os
import pandas as pd
import sys
import unittest

from data_mine import Collection
from data_mine.nlp.allen_ai_arc import ARCType
from data_mine.nlp.allen_ai_arc.utils import type_to_data_file
from pyfakefs.fake_filesystem_unittest import TestCase
if sys.version_info >= (3, 3):
    from unittest.mock import ANY, patch
else:
    from mock import ANY, patch


GOOD_QUESTION1 = json.loads("""{
    "id":"Mercury_7234185",
    "question":{
        "stem":"Which part of Earth's structure is composed ...?",
        "choices":[
            {
                "text":"the inner core",
                "label":"A"
            },
            {
                "text":"the outer core",
                "label":"B"
            },
            {
                "text":"the lithosphere",
                "label":"C"
            },
            {
                "text":"the asthenosphere",
                "label":"D"
            }
        ]
    },
    "answerKey":"A"
}""")

# Candidate answers not in the right order (of the labels).
GOOD_QUESTION2 = json.loads("""{
    "id":"Mercury_7074900",
    "question":{
        "stem":"In order for cells to grow at a normal rate",
        "choices":[
            {
                "text":"be of similar size.",
                "label":"D"
            },
            {
                "text":"take in nutrients.",
                "label":"C"
            },
            {
                "text":"none of the above.",
                "label":"E"
            },
            {
                "text":"take in light.",
                "label":"A"
            },
            {
                "text":"be specialized.",
                "label":"B"
            }
        ]
    },
    "answerKey":"C"
}""")

# Answer labels are integers, not letters.
GOOD_QUESTION3 = json.loads("""{
    "id":"NYSEDREGENTS_2015_8_24",
    "question":{
        "stem":"The length of one day on Earth is determined by",
        "choices":[
            {
                "text":"Earth to rotate once",
                "label":"3"
            },
            {
                "text":"the Moon to revolve once",
                "label":"1"
            },
            {
                "text":"the Moon to rotate once",
                "label":"2"
            }
        ]
    },
    "answerKey":"3"
}""")

# Mixed digits and letters for answer labels.
BAD_QUESTION1 = json.loads("""{
    "id":"NYSEDREGENTS_2015_8_24",
    "question":{
        "stem":"The length of one day on Earth",
        "choices":[
            {
                "text":"Earth to rotate",
                "label":"1"
            },
            {
                "text":"the Moon to revolve",
                "label":"B"
            },
            {
                "text":"the Moon to rotate",
                "label":"3"
            },
            {
                "text":"something else",
                "label":"D"
            }
        ]
    },
    "answerKey":"3"
}""")


class TestARCDatasetLoader(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def write_questions(self, arc_type, question_list):
        datafile = type_to_data_file(arc_type)
        pardir = os.path.abspath(os.path.join(datafile, os.pardir))
        if not os.path.exists(pardir):
            os.makedirs(pardir, mode=0o755)
        with jsonlines.open(datafile, "w") as writer:
            writer.write_all(question_list)

    @patch('data_mine.nlp.allen_ai_arc.loader.download_dataset')
    def test_empty_dataset(self, mock_download_dataset):
        self.write_questions(ARCType.DEV_CHALLENGE, [])
        df = dm.ALLEN_AI_ARC(ARCType.DEV_CHALLENGE)
        mock_download_dataset.assert_called_once_with(Collection.ALLEN_AI_ARC, ANY)  # noqa: E501
        self.assertEqual(len(df), 0)

    @patch('data_mine.nlp.allen_ai_arc.loader.download_dataset')
    def test_parsing_logic(self, mock_download_dataset):
        self.write_questions(ARCType.TRAIN_EASY, [
            GOOD_QUESTION1, GOOD_QUESTION2, GOOD_QUESTION3
        ])
        df = dm.ALLEN_AI_ARC(ARCType.TRAIN_EASY)
        self.assertEqual(len(df), 3)
        expected_df = pd.DataFrame(json.loads("""[
            {
                "id": "Mercury_7234185",
                "question": "Which part of Earth's structure is composed ...?",
                "answers": [
                    "the inner core",
                    "the outer core",
                    "the lithosphere",
                    "the asthenosphere"
                ],
                "correct": "A"
            },
            {
                "id": "Mercury_7074900",
                "question": "In order for cells to grow at a normal rate",
                "answers": [
                    "take in light.",
                    "be specialized.",
                    "take in nutrients.",
                    "be of similar size.",
                    "none of the above."
                ],
                "correct": "C"
            },
            {
                "id": "NYSEDREGENTS_2015_8_24",
                "question": "The length of one day on Earth is determined by",
                "answers": [
                    "the Moon to revolve once",
                    "the Moon to rotate once",
                    "Earth to rotate once"
                ],
                "correct": "3"
            }
        ]"""))
        pd.testing.assert_frame_equal(df, expected_df)
        mock_download_dataset.assert_called_once_with(Collection.ALLEN_AI_ARC, ANY)  # noqa: E501

    @patch('data_mine.nlp.allen_ai_arc.loader.download_dataset')
    def test_bad_answer_labels(self, mock_download_dataset):
        self.write_questions(ARCType.TEST_CHALLENGE, [BAD_QUESTION1])
        with self.assertRaises(AssertionError):
            dm.ALLEN_AI_ARC(ARCType.TEST_CHALLENGE)
        mock_download_dataset.assert_called_once_with(Collection.ALLEN_AI_ARC, ANY)  # noqa: E501


if __name__ == '__main__':
    unittest.main()
