import os
import unittest

from data_mine.nlp.allen_ai_obqa import OBQAType
from data_mine.nlp.allen_ai_obqa.utils import type_to_data_file


class TestUtilFunctions(unittest.TestCase):

    def test_type_to_data_file(self):
        for obqa_type in OBQAType:
            path = type_to_data_file(obqa_type)
            self.assertIn("OpenBookQA-V1-Sep2018", path)
            self.assertIn("Main", path)
            path = os.path.basename(path)
            self.assertEqual(path, "{}.jsonl".format(obqa_type.name.lower()))


if __name__ == '__main__':
    unittest.main()
