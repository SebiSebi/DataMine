import os
import unittest

from data_mine.nlp.RACE import RACEType
from data_mine.nlp.RACE.utils import next_question_id
from data_mine.nlp.RACE.utils import type_to_data_directory
from data_mine.utils import datamine_cache_dir


class TestUtilFunctions(unittest.TestCase):

    def test_next_question_id(self):
        ids = {}
        self.assertEqual(next_question_id(ids, "A"), "1-A")
        self.assertEqual(next_question_id(ids, "B"), "1-B")
        self.assertEqual(next_question_id(ids, "A"), "2-A")
        self.assertDictEqual(ids, {
            "A": 3,
            "B": 2,
        })
        self.assertEqual(next_question_id(ids, "A"), "3-A")
        self.assertEqual(next_question_id(ids, "B"), "2-B")
        self.assertEqual(next_question_id(ids, "car"), "1-car")
        self.assertDictEqual(ids, {
            "A": 4,
            "B": 3,
            "car": 2,
        })
        for i in range(1, 105):
            self.assertEqual(next_question_id(ids, "Q"), str(i) + "-Q")
        self.assertEqual(ids["Q"], 105)

        ids2 = {}
        self.assertEqual(next_question_id(ids2, "A"), "1-A")
        self.assertEqual(next_question_id(ids2, "B"), "1-B")
        self.assertEqual(next_question_id(ids, "A"), "4-A")
        self.assertEqual(next_question_id(ids, "B"), "3-B")

    def test_type_to_data_directory(self):
        DATA_DIR = os.path.join(datamine_cache_dir(), "RACE")
        self.assertEqual(
            type_to_data_directory(RACEType.TRAIN_MIDDLE),
            os.path.join(DATA_DIR, "RACE", "train", "middle")
        )
        self.assertEqual(
            type_to_data_directory(RACEType.DEV_MIDDLE),
            os.path.join(DATA_DIR, "RACE", "dev", "middle")
        )
        self.assertEqual(
            type_to_data_directory(RACEType.TEST_MIDDLE),
            os.path.join(DATA_DIR, "RACE", "test", "middle")
        )
        self.assertEqual(
            type_to_data_directory(RACEType.TRAIN_HIGH),
            os.path.join(DATA_DIR, "RACE", "train", "high")
        )
        self.assertEqual(
            type_to_data_directory(RACEType.DEV_HIGH),
            os.path.join(DATA_DIR, "RACE", "dev", "high")
        )
        self.assertEqual(
            type_to_data_directory(RACEType.TEST_HIGH),
            os.path.join(DATA_DIR, "RACE", "test", "high")
        )


if __name__ == '__main__':
    unittest.main()
