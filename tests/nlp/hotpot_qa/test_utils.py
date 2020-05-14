import os
import unittest

from data_mine.nlp.hotpot_qa import HotpotQAType
from data_mine.nlp.hotpot_qa.utils import type_to_data_file
from data_mine.utils import datamine_cache_dir


class TestUtilFunctions(unittest.TestCase):

    def test_type_to_data_file(self):
        cache_dir = datamine_cache_dir()
        for hotpot_qa_type in HotpotQAType:
            path = type_to_data_file(hotpot_qa_type)
            self.assertTrue(path.startswith(cache_dir))
            self.assertIn("HOTPOT_QA", path)
            path = os.path.basename(path)
            self.assertIn(hotpot_qa_type.name.lower(), path)


if __name__ == '__main__':
    unittest.main()
