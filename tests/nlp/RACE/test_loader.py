import os
import pandas as pd
import random
import unittest

from data_mine import Collection
from data_mine.nlp.RACE import RACEDataset, RACEType
from data_mine.utils import datamine_cache_dir
from pyfakefs.fake_filesystem_unittest import TestCase

FAKE_FILES = [
        ("1125.json", """
        {
            "answers":[
                "D",
                "C",
                "B"
            ],
            "options":[
                [
                    "option-1",
                    "option-2",
                    "option-3",
                    "option-4"
                ],
                [
                    "option-1",
                    "option-2",
                    "option-3",
                    "option-4"
                ],
                [
                    "option-1",
                    "option-2",
                    "option-3",
                    "option-4"
                ]
            ],
            "questions":[
                "Question 1 - id1",
                "Question 2 - id1",
                "Question 3 - id1"
            ],
            "article":"article - id1",
            "id":"id1"
        }"""),

        ("24172.json", """
        {
            "answers":[
                "A"
            ],
            "options":[
                [
                    "option-1",
                    "option-2",
                    "option-3",
                    "option-4"
                ]
            ],
            "questions":[
                "Question 1 - id2"
            ],
            "article":"article - id2",
            "id":"id2"
        }""")
]


class TestRACEDatasetLoader(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

        dataset_dir = os.path.join(datamine_cache_dir(), Collection.RACE.name,
                                   "RACE", "train", "middle")
        os.makedirs(dataset_dir, mode=0o755)

        # Write the mock files.
        random.shuffle(FAKE_FILES)
        for path, contents in FAKE_FILES:
            with open(os.path.join(dataset_dir, path), "wt") as g:
                g.write(contents)
                g.flush()

    def test_parsing(self):
        data = RACEDataset(RACEType.TRAIN_MIDDLE)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 4)
        self.assertEqual(data.shape, (4, 5))

        index_count = {
            '1-id1': 0,
            '2-id1': 0,
            '3-id1': 0,
            '1-id2': 0
        }
        expected_correct_answers = {
            '1-id1': 'D',
            '2-id1': 'C',
            '3-id1': 'B',
            '1-id2': 'A'
        }
        expected_questions = {
            '1-id1': 'Question 1 - id1',
            '2-id1': 'Question 2 - id1',
            '3-id1': 'Question 3 - id1',
            '1-id2': 'Question 1 - id2'
        }
        for _, row in data.iterrows():
            q_id = row['id']
            self.assertIn(q_id, ["1-id1", "2-id1", "3-id1", "1-id2"])
            index_count[q_id] += 1
            self.assertEqual(
                    row['article'],
                    "article - {}".format(q_id[2:])
            )
            self.assertEqual(
                    row['question'],
                    expected_questions[q_id]
            )
            self.assertListEqual(
                    row['answers'],
                    ["option-1", "option-2", "option-3", "option-4"]
            )
            self.assertIn(row['correct'], ["A", "B", "C", "D"])
            self.assertEqual(
                    row['correct'],
                    expected_correct_answers[q_id]
            )
        self.assertEqual(len(index_count), 4)
        self.assertEqual(index_count['1-id1'], 1)
        self.assertEqual(index_count['2-id1'], 1)
        self.assertEqual(index_count['3-id1'], 1)
        self.assertEqual(index_count['1-id2'], 1)


if __name__ == '__main__':
    unittest.main()
