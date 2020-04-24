import os
import unittest

from data_mine.nlp.allen_ai_drop import DROPType
from data_mine.nlp.allen_ai_drop.utils import type_to_data_file


class TestUtilFunctions(unittest.TestCase):

    def test_type_to_data_file(self):
        for drop_type in DROPType:
            path = type_to_data_file(drop_type)
            self.assertIn(drop_type.name.lower(), os.path.basename(path))
            self.assertTrue(path.endswith("{}.json".format(drop_type.name.lower())))  # noqa: E501

        self.assertTrue(type_to_data_file(DROPType.TRAIN).endswith("train.json"))  # noqa: E501
        self.assertTrue(type_to_data_file(DROPType.DEV).endswith("dev.json"))  # noqa: E501


if __name__ == '__main__':
    unittest.main()
