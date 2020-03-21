import os
import sys
import unittest

from data_mine.utils import get_home_dir
if sys.version_info >= (3, 3):
    from unittest.mock import patch
else:
    from mock import patch


class TestMiscUtils(unittest.TestCase):

    def test_get_home_dir(self):
        home_dir = get_home_dir()
        self.assertIsInstance(home_dir, str)
        self.assertTrue(os.path.isdir(home_dir))

        with patch('os.path.expanduser') as mock:
            mock.return_value = "fake home path"
            self.assertEqual(get_home_dir(), "fake home path")
        mock.assert_called_once_with('~')


if __name__ == '__main__':
    unittest.main()
