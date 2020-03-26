import os
import sys
import unittest

from data_mine.constants import DATAMINE_CACHE_DIR_ENV_VAR
from data_mine.utils import datamine_cache_dir
from data_mine.utils import file_sha256
from data_mine.utils import get_home_dir
from faker import Faker
from tempfile import mkstemp
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
if sys.version_info >= (3, 3):
    from unittest.mock import patch
else:
    from mock import patch


class TestMiscUtils(unittest.TestCase):

    #########################################################################
    #                               get_home_dir()                          #
    #########################################################################

    def test_get_home_dir(self):
        home_dir = get_home_dir()
        self.assertIsInstance(home_dir, str)
        self.assertTrue(os.path.isdir(home_dir))

        with patch('os.path.expanduser') as mock:
            mock.return_value = "fake home path"
            self.assertEqual(get_home_dir(), "fake home path")
        mock.assert_called_once_with('~')

    #########################################################################
    #                                file_sha256()                          #
    #########################################################################

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

    #########################################################################
    #                           datamine_cache_dir()                        #
    #########################################################################

    def test_datamine_cache_dir(self):
        # No env variable is present.
        if DATAMINE_CACHE_DIR_ENV_VAR in os.environ:
            del os.environ[DATAMINE_CACHE_DIR_ENV_VAR]
        with patch('os.path.isfile', return_value=False):
            with patch('os.path.isdir', return_value=True):
                self.assertEqual(
                        os.path.basename(datamine_cache_dir()),
                        ".datamine_cache_dir"
                )

        # Env variable is set.
        os.environ[DATAMINE_CACHE_DIR_ENV_VAR] = "my-fake-dir-for-testing"
        with patch('os.path.isfile', return_value=False):
            with patch('os.path.isdir', return_value=True):
                self.assertEqual(
                        os.path.basename(datamine_cache_dir()),
                        "my-fake-dir-for-testing"
                )

        # Env variable is set but empty. Fall back to the default dir.
        os.environ[DATAMINE_CACHE_DIR_ENV_VAR] = ""
        with patch('os.path.isfile', return_value=False):
            with patch('os.path.isdir', return_value=True):
                self.assertEqual(
                        os.path.basename(datamine_cache_dir()),
                        ".datamine_cache_dir"
                )

        # Directory is created if it does not exist.
        with patch('os.path.isfile', return_value=False):
            with patch('os.path.isdir', return_value=False):
                cache_dir = None
                with patch('os.makedirs') as makedirs_mock:
                    cache_dir = datamine_cache_dir()
                makedirs_mock.assert_called_once_with(cache_dir, mode=493)

        # Directory is not created if already exists.
        with patch('os.path.isfile', return_value=False):
            with patch('os.path.isdir', return_value=True):
                with patch('os.makedirs') as makedirs_mock:
                    datamine_cache_dir()
                makedirs_mock.assert_not_called()

        # Program exists if the cached directory is a file.
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('os.path.isfile', return_value=True):
                with self.assertRaises(SystemExit) as context:
                    datamine_cache_dir()
                self.assertEqual(context.exception.code, 1)
        self.assertIn("is a file.\n", mock_stdout.getvalue())

        # The function checks if the directory is a file before
        # creating a new directory (and the argument is correct).
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.return_value = False
            cache_dir = None
            with patch('os.path.isdir', return_value=True):
                cache_dir = datamine_cache_dir()
            mock_isfile.assert_called_once_with(cache_dir)


if __name__ == '__main__':
    unittest.main()
