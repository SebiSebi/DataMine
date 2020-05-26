import os
import unittest

from data_mine.nlp.allen_ai_arc import ARCType
from data_mine.nlp.allen_ai_arc.utils import type_to_data_file


class TestUtilFunctions(unittest.TestCase):

    def test_type_to_data_file(self):
        for arc_type in ARCType:
            path = type_to_data_file(arc_type)
            self.assertTrue(path.endswith(
                arc_type.name.lower().split("_")[0].capitalize() + ".jsonl"
            ))
            category = arc_type.name.lower().split("_")[1].capitalize()
            self.assertGreaterEqual(path.count(category), 2)

        def inner_path(path):
            path = filter(lambda x: len(x) > 0, path.split(os.sep))
            path = list(path)
            self.assertGreaterEqual(len(path), 3)
            self.assertEqual(path[-3], "ARC-V1-Feb2018-2")
            return "/".join(path[-2:])

        self.assertEqual(
            inner_path(type_to_data_file(ARCType.TRAIN_EASY)),
            "ARC-Easy/ARC-Easy-Train.jsonl"
        )
        self.assertEqual(
            inner_path(type_to_data_file(ARCType.DEV_EASY)),
            "ARC-Easy/ARC-Easy-Dev.jsonl"
        )
        self.assertEqual(
            inner_path(type_to_data_file(ARCType.TEST_EASY)),
            "ARC-Easy/ARC-Easy-Test.jsonl"
        )
        self.assertEqual(
            inner_path(type_to_data_file(ARCType.TRAIN_CHALLENGE)),
            "ARC-Challenge/ARC-Challenge-Train.jsonl"
        )
        self.assertEqual(
            inner_path(type_to_data_file(ARCType.DEV_CHALLENGE)),
            "ARC-Challenge/ARC-Challenge-Dev.jsonl"
        )
        self.assertEqual(
            inner_path(type_to_data_file(ARCType.TEST_CHALLENGE)),
            "ARC-Challenge/ARC-Challenge-Test.jsonl"
        )


if __name__ == '__main__':
    unittest.main()
