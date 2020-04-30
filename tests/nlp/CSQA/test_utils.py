import os
import unittest

from data_mine.nlp.CSQA import CSQAType
from data_mine.nlp.CSQA.utils import type_to_data_file


class TestUtilFunctions(unittest.TestCase):

    def test_type_to_data_file(self):
        for csqa_type in CSQAType:
            path = type_to_data_file(csqa_type)
            self.assertIn("CSQA", path)
            path = os.path.basename(path)
            self.assertIn(csqa_type.name.lower(), path)
            self.assertTrue(path.startswith("{}_rand_split".format(csqa_type.name.lower())))  # noqa: E501


if __name__ == '__main__':
    unittest.main()
