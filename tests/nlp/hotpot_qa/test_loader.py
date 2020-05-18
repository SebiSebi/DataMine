import data_mine as dm
import json
import os
import pandas as pd
import sys
import unittest

from copy import deepcopy
from data_mine import Collection
from data_mine.nlp.hotpot_qa import HotpotQAType
from data_mine.nlp.hotpot_qa.utils import type_to_data_file
from data_mine.utils import datamine_cache_dir
from pyfakefs.fake_filesystem_unittest import TestCase
if sys.version_info >= (3, 3):
    from unittest.mock import ANY, patch
else:
    from mock import ANY, patch

TRAIN_QUESTION = json.loads("""{
    "supporting_facts": [
        ["Limitless (EP)", 0],
        ["Crown the Empire", 0]
    ],
    "level": "medium",
    "question": "Some question",
    "context": [
        [
            "The Resistance: Rise of The Runaways",
            ["Sent 1", " Sent 2.", " Sent 3."]
        ],
        [
            "Reign of Terror (Capture the Crown album)",
            ["Sent 4."]
        ],
        [
            "Retrograde (Crown the Empire album)",
            ["Sent 5.", " Sent 6."]
        ],
        [
            "Roots (Sepultura album)",
            ["Sent 7.", " Sent 8.", " Sent 9."]
        ],
        [
            "Forest Stream",
            ["Sent 10.", " Sent 11.", " Sent 12.", " Sent 13.",
            " Sent 14.", " Sent 15."]
        ],
        [
            "The Crown (band)",
            ["Sent 16."]
        ],
        [
            "The Fallout (Crown the Empire album)",
            ["Sent 17.", " Sent 18."]
        ],
        [
            "Crown the Empire discography",
            [" Sent 19."]
        ],
        [
            "Crown the Empire",
            ["Sent good 1.", " Sent good 2."]
        ],
        [
            "Limitless (EP)",
            ["Sent good 3."]
        ]
    ],
    "answer": "Dallas",
    "_id": "5a899013554299515336131a",
    "type": "bridge"
}
""")

# Same as TRAIN QUESTION but some title from supporting facts in missing
# from the context to simulate imperfect document retrieval.
DEV_FULLWIKI_QUESTION = json.loads("""{
    "supporting_facts": [
        ["Limitless (EP)", 0],
        ["Crown the Empire", 0]
    ],
    "level": "medium",
    "question": "Some question",
    "context": [
        [
            "The Resistance: Rise of The Runaways",
            ["Sent 1", " Sent 2.", " Sent 3."]
        ],
        [
            "Reign of Terror (Capture the Crown album)",
            ["Sent 4."]
        ],
        [
            "Retrograde (Crown the Empire album)",
            ["Sent 5.", " Sent 6."]
        ],
        [
            "Roots (Sepultura album)",
            ["Sent 7.", " Sent 8.", " Sent 9."]
        ],
        [
            "Forest Stream",
            ["Sent 10.", " Sent 11.", " Sent 12.", " Sent 13.",
            " Sent 14.", " Sent 15."]
        ],
        [
            "The Crown (band)",
            ["Sent 16."]
        ],
        [
            "The Fallout (Crown the Empire album)",
            ["Sent 17.", " Sent 18."]
        ],
        [
            "Crown the Empire discography",
            [" Sent 19."]
        ],
        [
            "Crown the Empire - is missing",
            ["Sent good 1.", " Sent good 2."]
        ],
        [
            "Limitless (EP)",
            ["Sent good 3."]
        ]
    ],
    "answer": "Dallas",
    "_id": "5a899013554299515336131a",
    "type": "bridge"
}
""")

# Some fields are missing in the test split, such as `answer`.
TEST_FULLWIKI_QUESTION = json.loads("""{
    "_id":"5ab5072e5542990594ba9cda",
    "question":"Test question?",
    "context":[
        [
            "The Rolling Stone Album Guide",
            ["Sent 1.", " Sent 2."]
        ],
        [
            "Fear and Loathing at Rolling Stone",
            ["Sent 3."]
        ]
    ]
}""")


class TestHotpotQADatasetLoader(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

        dataset_dir = os.path.join(datamine_cache_dir(), "HOTPOT_QA")
        os.makedirs(dataset_dir, mode=0o755)

    def write_questions(self, hotpot_qa_type, question_list):
        datafile = type_to_data_file(hotpot_qa_type)
        question_list = json.dumps(question_list)
        with open(datafile, "wt") as g:
            g.write(question_list)
            g.flush()

    @patch('data_mine.nlp.hotpot_qa.loader.download_dataset')
    def test_empty_dataset(self, mock_download_dataset):
        self.write_questions(HotpotQAType.TRAIN, [])
        df = dm.HOTPOT_QA(HotpotQAType.TRAIN)
        mock_download_dataset.assert_called_once_with(Collection.HOTPOT_QA, ANY)  # noqa: E501
        self.assertEqual(len(df), 0)

    @patch('data_mine.nlp.hotpot_qa.loader.download_dataset')
    def test_load_multiple_questions(self, mock_download_dataset):
        similar_question = deepcopy(TRAIN_QUESTION)
        similar_question["_id"] = "aaaabbbbccccdddd!2"
        self.write_questions(HotpotQAType.TRAIN, [
            TRAIN_QUESTION, similar_question
        ])
        df = dm.HOTPOT_QA(HotpotQAType.TRAIN)
        mock_download_dataset.assert_called_once_with(Collection.HOTPOT_QA, ANY)  # noqa: E501
        self.assertEqual(len(df), 2)

    @patch('data_mine.nlp.hotpot_qa.loader.download_dataset')
    def test_load_in_train_format(self, mock_download_dataset):
        self.write_questions(HotpotQAType.TRAIN, [TRAIN_QUESTION])
        df = dm.HOTPOT_QA(HotpotQAType.TRAIN)
        expected_df = pd.DataFrame(json.loads("""[
            {
                "id": "5a899013554299515336131a",
                "question": "Some question",
                "answer": "Dallas",
                "gold_paragraphs": [
                    "Sent good 3.",
                    "Sent good 1.  Sent good 2."
                ],
                "supporting_facts": [
                    ["Limitless (EP)", 0],
                    ["Crown the Empire", 0]
                ],
                "context": [
                    [
                        "The Resistance: Rise of The Runaways",
                        ["Sent 1", " Sent 2.", " Sent 3."]
                    ],
                    [
                        "Reign of Terror (Capture the Crown album)",
                        ["Sent 4."]
                    ],
                    [
                        "Retrograde (Crown the Empire album)",
                        ["Sent 5.", " Sent 6."]
                    ],
                    [
                        "Roots (Sepultura album)",
                        ["Sent 7.", " Sent 8.", " Sent 9."]
                    ],
                    [
                        "Forest Stream",
                        ["Sent 10.", " Sent 11.", " Sent 12.", " Sent 13.",
                        " Sent 14.", " Sent 15."]
                    ],
                    [
                        "The Crown (band)",
                        ["Sent 16."]
                    ],
                    [
                        "The Fallout (Crown the Empire album)",
                        ["Sent 17.", " Sent 18."]
                    ],
                    [
                        "Crown the Empire discography",
                        [" Sent 19."]
                    ],
                    [
                        "Crown the Empire",
                        ["Sent good 1.", " Sent good 2."]
                    ],
                    [
                        "Limitless (EP)",
                        ["Sent good 3."]
                    ]
                ],
                "question_type": "bridge",
                "question_level": "medium"
            }
        ]"""))
        pd.testing.assert_frame_equal(df, expected_df)
        mock_download_dataset.assert_called_once_with(Collection.HOTPOT_QA, ANY)  # noqa: E501

    @patch('data_mine.nlp.hotpot_qa.loader.download_dataset')
    def test_load_in_dev_distractor_format(self, mock_download_dataset):
        # TRAIN and DEV_DISTRACTOR have the same format.
        self.write_questions(HotpotQAType.DEV_DISTRACTOR, [TRAIN_QUESTION])
        df = dm.HOTPOT_QA(HotpotQAType.DEV_DISTRACTOR)
        expected_df = pd.DataFrame(json.loads("""[
            {
                "id": "5a899013554299515336131a",
                "question": "Some question",
                "answer": "Dallas",
                "gold_paragraphs": [
                    "Sent good 3.",
                    "Sent good 1.  Sent good 2."
                ],
                "supporting_facts": [
                    ["Limitless (EP)", 0],
                    ["Crown the Empire", 0]
                ],
                "context": [
                    [
                        "The Resistance: Rise of The Runaways",
                        ["Sent 1", " Sent 2.", " Sent 3."]
                    ],
                    [
                        "Reign of Terror (Capture the Crown album)",
                        ["Sent 4."]
                    ],
                    [
                        "Retrograde (Crown the Empire album)",
                        ["Sent 5.", " Sent 6."]
                    ],
                    [
                        "Roots (Sepultura album)",
                        ["Sent 7.", " Sent 8.", " Sent 9."]
                    ],
                    [
                        "Forest Stream",
                        ["Sent 10.", " Sent 11.", " Sent 12.", " Sent 13.",
                        " Sent 14.", " Sent 15."]
                    ],
                    [
                        "The Crown (band)",
                        ["Sent 16."]
                    ],
                    [
                        "The Fallout (Crown the Empire album)",
                        ["Sent 17.", " Sent 18."]
                    ],
                    [
                        "Crown the Empire discography",
                        [" Sent 19."]
                    ],
                    [
                        "Crown the Empire",
                        ["Sent good 1.", " Sent good 2."]
                    ],
                    [
                        "Limitless (EP)",
                        ["Sent good 3."]
                    ]
                ],
                "question_type": "bridge",
                "question_level": "medium"
            }
        ]"""))
        pd.testing.assert_frame_equal(df, expected_df)
        mock_download_dataset.assert_called_once_with(Collection.HOTPOT_QA, ANY)  # noqa: E501

    @patch('data_mine.nlp.hotpot_qa.loader.download_dataset')
    def test_load_in_dev_fullwiki_format(self, mock_download_dataset):
        self.write_questions(HotpotQAType.DEV_FULLWIKI, [DEV_FULLWIKI_QUESTION])  # noqa: E501
        df = dm.HOTPOT_QA(HotpotQAType.DEV_FULLWIKI)
        expected_df = pd.DataFrame(json.loads("""[
            {
                "id": "5a899013554299515336131a",
                "question": "Some question",
                "answer": "Dallas",
                "gold_paragraphs": [
                    "Sent good 3."
                ],
                "supporting_facts": [
                    ["Limitless (EP)", 0],
                    ["Crown the Empire", 0]
                ],
                "context": [
                    [
                        "The Resistance: Rise of The Runaways",
                        ["Sent 1", " Sent 2.", " Sent 3."]
                    ],
                    [
                        "Reign of Terror (Capture the Crown album)",
                        ["Sent 4."]
                    ],
                    [
                        "Retrograde (Crown the Empire album)",
                        ["Sent 5.", " Sent 6."]
                    ],
                    [
                        "Roots (Sepultura album)",
                        ["Sent 7.", " Sent 8.", " Sent 9."]
                    ],
                    [
                        "Forest Stream",
                        ["Sent 10.", " Sent 11.", " Sent 12.", " Sent 13.",
                        " Sent 14.", " Sent 15."]
                    ],
                    [
                        "The Crown (band)",
                        ["Sent 16."]
                    ],
                    [
                        "The Fallout (Crown the Empire album)",
                        ["Sent 17.", " Sent 18."]
                    ],
                    [
                        "Crown the Empire discography",
                        [" Sent 19."]
                    ],
                    [
                        "Crown the Empire - is missing",
                        ["Sent good 1.", " Sent good 2."]
                    ],
                    [
                        "Limitless (EP)",
                        ["Sent good 3."]
                    ]
                ],
                "question_type": "bridge",
                "question_level": "medium"
            }
        ]"""))
        pd.testing.assert_frame_equal(df, expected_df)
        mock_download_dataset.assert_called_once_with(Collection.HOTPOT_QA, ANY)  # noqa: E501

    @patch('data_mine.nlp.hotpot_qa.loader.download_dataset')
    def test_load_in_test_fullwiki_format(self, mock_download_dataset):
        self.write_questions(HotpotQAType.TEST_FULLWIKI, [TEST_FULLWIKI_QUESTION])  # noqa: E501
        df = dm.HOTPOT_QA(HotpotQAType.TEST_FULLWIKI)
        expected_df = pd.DataFrame(json.loads("""[
            {
                "id": "5ab5072e5542990594ba9cda",
                "question": "Test question?",
                "answer": null,
                "gold_paragraphs": [],
                "supporting_facts": [],
                "context": [
                    [
                        "The Rolling Stone Album Guide",
                        ["Sent 1.", " Sent 2."]
                    ],
                    [
                        "Fear and Loathing at Rolling Stone",
                        ["Sent 3."]
                    ]
                ],
                "question_type": null,
                "question_level": null
            }
        ]"""))
        pd.testing.assert_frame_equal(df, expected_df)
        mock_download_dataset.assert_called_once_with(Collection.HOTPOT_QA, ANY)  # noqa: E501

    @patch('data_mine.nlp.hotpot_qa.loader.download_dataset')
    def test_duplicate_ids_not_allowed(self, mock_download_dataset):
        self.write_questions(HotpotQAType.TRAIN, [
            TRAIN_QUESTION, TRAIN_QUESTION
        ])
        with self.assertRaises(AssertionError):
            dm.HOTPOT_QA(HotpotQAType.TRAIN)
        mock_download_dataset.assert_called_once_with(Collection.HOTPOT_QA, ANY)  # noqa: E501


if __name__ == '__main__':
    unittest.main()
