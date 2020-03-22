import os
import sys
import unittest

from data_mine.utils import get_home_dir
from data_mine.utils import file_sha256
from faker import Faker
from tempfile import mkstemp
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

    def _test_file_sha256(self, file_contents, expected_sha256):
        fake = Faker()
        temp_file_path = None
        temp_fd = None
        try:
            fake_suffix = fake.pystr(min_chars=10, max_chars=20)
            temp_fd, temp_file_path = mkstemp(suffix=fake_suffix)
            del fake_suffix

            with open(temp_file_path, "wb") as g:
                g.write(file_contents)
                g.flush()

            self.assertEqual(file_sha256(temp_file_path), expected_sha256)
        finally:
            if temp_fd:
                os.close(temp_fd)
            if temp_file_path:
                os.remove(temp_file_path)

    def test_small_file_sha256(self):
        self._test_file_sha256(
                "I love pizza".encode(),
                "c4d9afc24a0f587b9f9855bc88f7c3aa31f811b1bfa465086cf72761ffaf303c"  # noqa: E501
        )

    def test_large_file_sha256(self):
        self._test_file_sha256(
                "x1x2x3".encode() * (175 * 1024 * 13),  # about 14MB
                "2d0e659219b13ba71536a47e966a8207d649e4fb72f4ede18ab1347ef953ccdd"  # noqa: E501
        )


if __name__ == '__main__':
    unittest.main()
