import os
import unittest

from data_mine.nlp.cosmos_qa import CosmosQAType
from data_mine.nlp.cosmos_qa.utils import type_to_data_file
from data_mine.utils import datamine_cache_dir


class TestUtilFunctions(unittest.TestCase):

    def test_type_to_data_file(self):
        expected_results = {
                CosmosQAType.TRAIN: "train.jsonl",
                CosmosQAType.DEV: "valid.jsonl",
                CosmosQAType.TEST: "test.jsonl"
        }
        cache_dir = datamine_cache_dir()
        for cosmos_qa_type in CosmosQAType:
            path = type_to_data_file(cosmos_qa_type)
            self.assertTrue(path.startswith(cache_dir))
            self.assertIn("COSMOS_QA", path)
            path = os.path.basename(path)
            self.assertEqual(path, expected_results[cosmos_qa_type])


if __name__ == '__main__':
    unittest.main()
